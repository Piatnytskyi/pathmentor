import json
import os
import pprint
from dotenv import dotenv_values
import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs
import tensorflow_io as tfio

from model.query_model import QueryModel
from model.candidate_model import CandidateModel
from model.pathmentor_model import PahtmentorModel

environment = os.getenv('ENVIRONMENT', 'dev')
configuration_files_names = {
    'dev': 'config_dev.json',
    'test': 'config_test.json',
    'prod': 'config_prod.json'
}

configuration_file = configuration_files_names.get(environment)
configuration = None
with open(configuration_file) as file:
    configuration = json.load(file)

secrets = dotenv_values(".env")

skills_ds = tfio.experimental.mongodb.MongoDBIODataset(
    uri=secrets['SRV_URI'], database=configuration['database'], collection=configuration['skills_collection']
)

skills_specs = {
    "_id": {
        "$oid": tf.TensorSpec(tf.TensorShape([None]), tf.string, name="$oid")
    },
    "skill": tf.TensorSpec(tf.TensorShape([None]), tf.string, name="skill")
}

skills_ds = skills_ds.map(lambda x: tf.strings.as_string(tfio.experimental.serialization.decode_json(x, specs=skills_specs)["skill"]))
  
unique_user_skills = np.unique(np.concatenate(list(skills_ds.batch(1000))))

train_ds = tfio.experimental.mongodb.MongoDBIODataset(
    uri=secrets['SRV_URI'], database=configuration['staging_database'], collection=configuration['interactions_train_collection']
)
test_ds = tfio.experimental.mongodb.MongoDBIODataset(
    uri=secrets['SRV_URI'], database=configuration['staging_database'], collection=configuration['interactions_test_collection']
)

interactions_specs = {
    "context_user_title": tf.TensorSpec(tf.TensorShape([None]), tf.string, name="context_user_title"),
    "context_user_experience": tf.TensorSpec(tf.TensorShape([None]), tf.string, name="context_user_experience"),
    "context_user_salary": tf.TensorSpec(tf.TensorShape([None]), tf.string, name="context_user_salary"),
    "context_skill": tf.RaggedTensorSpec(tf.TensorShape([None]), tf.string),
    "label_skill": tf.TensorSpec(tf.TensorShape([None]), tf.string, name="label_skill")
}

train_ds = train_ds.map(lambda x: tfio.experimental.serialization.decode_json(x, specs=interactions_specs))
test_ds = test_ds.map(lambda x: tfio.experimental.serialization.decode_json(x, specs=interactions_specs))

train_ds = train_ds.map(lambda x: {
    "context_user_title": tf.strings.as_string(x["context_user_title"]),
    "context_user_experience": tf.strings.as_string(x["context_user_experience"]),
    "context_user_salary": tf.strings.as_string(x["context_user_salary"]),
    "context_skill": tf.strings.as_string(x["context_skill"]),
    "label_skill": tf.strings.as_string(x["label_skill"])
})

test_ds = test_ds.map(lambda x: {
    "context_user_title": tf.strings.as_string(x["context_user_title"]),
    "context_user_experience": tf.strings.as_string(x["context_user_experience"]),
    "context_user_salary": tf.strings.as_string(x["context_user_salary"]),
    "context_skill": tf.strings.as_string(x["context_skill"]),
    "label_skill": tf.strings.as_string(x["label_skill"])
})

unique_user_titles = np.unique(np.concatenate(list(train_ds.padded_batch(1000).map(lambda x: x["context_user_title"]))))
unique_user_experience = np.unique(np.concatenate(list(train_ds.padded_batch(1000).map(lambda x: x["context_user_experience"]))))
unique_user_salary = np.unique(np.concatenate(list(train_ds.padded_batch(1000).map(lambda x: x["context_user_salary"]))))

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

tf.saved_model.save(index, "../bin/model/1")
