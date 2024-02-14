import pprint
import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs

from model.query_model import QueryModel
from model.candidate_model import CandidateModel
from model.pathmentor_model import PahtmentorModel

train = tf.data.TFRecordDataset("../bin/interactions_train.tfrecord")
test = tf.data.TFRecordDataset("../bin/interactions_test.tfrecord")

feature_description = {
    'context_user_title': tf.io.FixedLenFeature([1], tf.string),
    'context_user_experience': tf.io.FixedLenFeature([1], tf.string),
    'context_user_salary': tf.io.FixedLenFeature([1], tf.string),
    'context_skill': tf.io.FixedLenSequenceFeature([], tf.string, allow_missing=True),
    'label_skill': tf.io.FixedLenFeature([1], tf.string)
}

def _parse_function(example_proto):
  return tf.io.parse_single_example(example_proto, feature_description)

train_ds = train.map(_parse_function).map(lambda x: {
    "context_user_title": tf.strings.as_string(x["context_user_title"]),
    "context_user_experience": tf.strings.as_string(x["context_user_experience"]),
    "context_user_salary": tf.strings.as_string(x["context_user_salary"]),
    "context_skill": tf.strings.as_string(x["context_skill"]),
    "label_skill": tf.strings.as_string(x["label_skill"])
})

test_ds = test.map(_parse_function).map(lambda x: {
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

skills = tf.data.TFRecordDataset("../bin/skills.tfrecord")

feature_description = {
    'skill': tf.io.FixedLenFeature({}, tf.string)
}

skills_ds = skills.map(_parse_function).map(lambda x: tf.strings.as_string(x["skill"]))

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

tf.saved_model.save(index, "../bin/model/1")
