from pathlib import Path
import pprint
import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs
import tensorflow_io as tfio

from pathmentor_core.models.query_model import QueryModel
from pathmentor_core.models.candidate_model import CandidateModel
from pathmentor_core.models.pathmentor_model import PahtmentorModel

class PathMentorModelTrainer:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def train(self, output_path: Path) -> None:
        train = tfio.experimental.IODataset.from_sql(
            query="""
                SELECT i.*, 
                    t.Name as context_user_title, 
                    e.Range as context_user_experience, 
                    s.Range as context_user_salary, 
                    sk.Name as label_skill,
                    ARRAY_AGG(isk.Name) as context_skill
                FROM train_interactions i
                JOIN title t ON i.TitleId = t.Id
                JOIN experience e ON i.ExperienceId = e.Id
                JOIN salary s ON i.SalaryId = s.Id
                JOIN skill sk ON i.LabelSkillId = sk.Id
                LEFT JOIN InteractionSkills isk ON i.Id = isk.InteractionId
                GROUP BY i.Id, t.Name, e.Range, s.Range, sk.Name
            """,
            endpoint=self._connection_string)
        
        test = tfio.experimental.IODataset.from_sql(
            query="""
                SELECT i.*, 
                    t.Name as context_user_title, 
                    e.Range as context_user_experience, 
                    s.Range as context_user_salary, 
                    sk.Name as label_skill,
                    ARRAY_AGG(isk.Name) as context_skill
                FROM test_interactions i
                JOIN title t ON i.TitleId = t.Id
                JOIN experience e ON i.ExperienceId = e.Id
                JOIN salary s ON i.SalaryId = s.Id
                JOIN skill sk ON i.LabelSkillId = sk.Id
                LEFT JOIN InteractionSkills isk ON i.Id = isk.InteractionId
                GROUP BY i.Id, t.Name, e.Range, s.Range, sk.Name
            """,
            endpoint=self._connection_string)

        # interactions_specs = {
        #     'context_user_title': tf.io.FixedLenFeature([1], tf.string),
        #     'context_user_experience': tf.io.FixedLenFeature([1], tf.string),
        #     'context_user_salary': tf.io.FixedLenFeature([1], tf.string),
        #     'context_skill': tf.io.FixedLenSequenceFeature([], tf.string, allow_missing=True),
        #     'label_skill': tf.io.FixedLenFeature([1], tf.string)
        # }

        # def _parse_function(example_proto):
        #     return tf.io.parse_single_example(example_proto, interactions_specs)

        train_ds = train.map(lambda x: {
            "context_user_title": tf.strings.as_string(x["context_user_title"]),
            "context_user_experience": tf.strings.as_string(x["context_user_experience"]),
            "context_user_salary": tf.strings.as_string(x["context_user_salary"]),
            "context_skill": tf.strings.as_string(x["context_skill"]),
            "label_skill": tf.strings.as_string(x["label_skill"])
        })

        test_ds = test.map(lambda x: {
            "context_user_title": tf.strings.as_string(x["context_user_title"]),
            "context_user_experience": tf.strings.as_string(x["context_user_experience"]),
            "context_user_salary": tf.strings.as_string(x["context_user_salary"]),
            "context_skill": tf.strings.as_string(x["context_skill"]),
            "label_skill": tf.strings.as_string(x["label_skill"])
        })

        for x in train_ds.take(1).as_numpy_iterator():
            pprint.pprint(x)

        unique_user_titles = np.unique(np.concatenate(list(train_ds.padded_batch(1000).map(lambda x: x["context_user_title"]))))
        unique_user_experience = np.unique(np.concatenate(list(train_ds.padded_batch(1000).map(lambda x: x["context_user_experience"]))))
        unique_user_salary = np.unique(np.concatenate(list(train_ds.padded_batch(1000).map(lambda x: x["context_user_salary"]))))

        skills = tfio.experimental.IODataset.from_sql(
            query="SELECT co, pt08s1 FROM AirQualityUCI;",
            endpoint=self._connection_string)

        skills_ds = skills.map(lambda x: tf.strings.as_string(x["skill"]))

        for x in skills_ds.take(5).as_numpy_iterator():
            pprint.pprint(x)

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
