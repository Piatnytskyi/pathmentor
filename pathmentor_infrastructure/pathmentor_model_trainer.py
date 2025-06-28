from pathlib import Path
import pprint
import numpy as np

import psycopg
import tensorflow as tf
import tensorflow_recommenders as tfrs

from pathmentor_core.models.query_model import QueryModel
from pathmentor_core.models.candidate_model import CandidateModel
from pathmentor_core.models.pathmentor_model import PahtmentorModel

class PathMentorModelTrainer:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def _generate_interactions_from(self, table: str):
        with psycopg.connect(self._connection_string) as connection:
            with connection.cursor(name='interactions_cursor') as cursor:
                cursor.execute(f"""
                    SELECT t."Name" as context_user_title, 
                        e."Range" as context_user_experience, 
                        s."Range" as context_user_salary,
                        sk."Name" as label_skill,
                        array_agg(cs."Name") as context_skill
                    FROM staging.{table} i
                    JOIN "Titles" t ON i."TitleId" = t."Id"
                    JOIN "Experiences" e ON i."ExperienceId" = e."Id"
                    JOIN "Salaries" s ON i."SalaryId" = s."Id"
                    JOIN "Skills" sk ON i."LabelSkillId" = sk."Id"
                    LEFT JOIN staging.{table}skill ints ON i."Id" = ints."ContextInteractionsId"
                    LEFT JOIN "Skills" cs ON ints."ContextSkillsId" = cs."Id"
                    GROUP BY i."Id", t."Id", e."Id", s."Id", sk."Id"
                """)
                for row in cursor:
                    yield [str(row[0])], [str(row[1])], [str(row[2])], [str(row[3])], row[4]

    def _generate_skills_from(self):
        with psycopg.connect(self._connection_string) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT "Name" FROM "Skills";""")
                for row in cursor:
                    yield row[0]

    def train(self, output_path: Path) -> None:
        interactions_output_signature = (
            tf.TensorSpec(shape=(1, ), dtype=tf.string, name="context_user_title"),
            tf.TensorSpec(shape=(1, ), dtype=tf.string, name="context_user_experience"),
            tf.TensorSpec(shape=(1, ), dtype=tf.string, name="context_user_salary"),
            tf.TensorSpec(shape=(1, ), dtype=tf.string, name="label_skill"),
            tf.TensorSpec(shape=(None, ), dtype=tf.string, name="context_skill")
        )

        train = tf.data.Dataset.from_generator(
            lambda: self._generate_interactions_from("train_interactions"),
            output_signature=interactions_output_signature)
        test = tf.data.Dataset.from_generator(
            lambda: self._generate_interactions_from("test_interactions"),
            output_signature=interactions_output_signature)

        interactions_map_lambda = lambda context_user_title, context_user_experience, context_user_salary, label_skill, context_skill: {
            "context_user_title": tf.strings.as_string(context_user_title),
            "context_user_experience": tf.strings.as_string(context_user_experience),
            "context_user_salary": tf.strings.as_string(context_user_salary),
            "label_skill": tf.strings.as_string(label_skill),
            "context_skill": tf.strings.as_string(context_skill)
        }

        train_ds = train.map(interactions_map_lambda)
        test_ds = test.map(interactions_map_lambda)

        for x in train_ds.take(1).as_numpy_iterator():
            pprint.pprint(x)

        skills = tf.data.Dataset.from_generator(
            lambda: self._generate_skills_from(),
            output_signature=(
                tf.TensorSpec(shape=(), dtype=tf.string, name="skill")
            ))

        skills_ds = skills.map(lambda skill: tf.strings.as_string(skill))

        for x in skills_ds.take(5).as_numpy_iterator():
            pprint.pprint(x)

        unique_user_titles = np.unique(np.concatenate(list(train_ds.padded_batch(1000).map(lambda x: x["context_user_title"]))))
        unique_user_experience = np.unique(np.concatenate(list(train_ds.padded_batch(1000).map(lambda x: x["context_user_experience"]))))
        unique_user_salary = np.unique(np.concatenate(list(train_ds.padded_batch(1000).map(lambda x: x["context_user_salary"]))))
        unique_user_skills = np.unique(np.concatenate(list(skills_ds.batch(1000))))

        embedding_dimension = 32

        query_model = tf.keras.Sequential([
            QueryModel(embedding_dimension, unique_user_skills, unique_user_titles, unique_user_experience, unique_user_salary),
            tf.keras.layers.Dense(32)
        ])
        candidate_model = tf.keras.Sequential([
            CandidateModel(embedding_dimension, unique_user_skills),
            tf.keras.layers.Dense(32)
        ])
        model = PahtmentorModel(
            query_model,
            candidate_model,
            metrics=tfrs.metrics.FactorizedTopK(
                candidates=skills_ds.batch(128).map(candidate_model),
            ))
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.1))

        cached_train = train_ds.shuffle(10_000).padded_batch(6400).cache()
        cached_test = test_ds.padded_batch(2560).cache()

        model.fit(cached_train, epochs=3)

        model.evaluate(cached_test, return_dict=True)

        index = tfrs.layers.factorized_top_k.BruteForce(model._query_model)
        index.index_from_dataset(
            tf.data.Dataset.zip((skills_ds.batch(100), skills_ds.batch(100).map(model._candidate_model)))
        )

        _, skills = index({
            "skills": tf.constant([["AWS Lambda", "R", "TensorFlow"]]),
            "title": tf.constant([["Data Scientist"]]),
            "experience": tf.constant([["1-3 years"]]),
            "salary": tf.constant([["1500-2000"]]),
        }, k=30)
        print(f"Recommendations: {skills}")

        tf.saved_model.save(index, output_path)
        print(f"Model saved to {output_path}")
