import tensorflow as tf

class QueryModel(tf.keras.Model):

  def __init__(self, embedding_dimension, unique_user_skills, unique_user_titles, unique_user_experience, unique_user_salary):
    super().__init__()

    self.user_skills_embedding = tf.keras.Sequential([
      tf.keras.layers.StringLookup(
          vocabulary=unique_user_skills, mask_token=None),
      tf.keras.layers.Embedding(len(unique_user_skills) + 1, embedding_dimension), 
      tf.keras.layers.GRU(embedding_dimension),
    ])

    self.user_titles_embedding = tf.keras.Sequential([
      tf.keras.layers.StringLookup(
          vocabulary=unique_user_titles, mask_token=None),
      tf.keras.layers.Embedding(len(unique_user_titles) + 1, embedding_dimension),
      tf.keras.layers.GRU(embedding_dimension),
    ])

    self.user_experience_embedding = tf.keras.Sequential([
      tf.keras.layers.StringLookup(
          vocabulary=unique_user_experience, mask_token=None),
      tf.keras.layers.Embedding(len(unique_user_experience) + 1, embedding_dimension),
      tf.keras.layers.GRU(embedding_dimension),
    ])

    self.user_salary_embedding = tf.keras.Sequential([
      tf.keras.layers.StringLookup(
          vocabulary=unique_user_salary, mask_token=None),
      tf.keras.layers.Embedding(len(unique_user_salary) + 1, embedding_dimension),
      tf.keras.layers.GRU(embedding_dimension),
    ])

  def call(self, inputs):
    return tf.concat([
        self.user_skills_embedding(inputs["skills"]),
        self.user_titles_embedding(inputs["title"]),
        self.user_experience_embedding(inputs["experience"]),
        self.user_salary_embedding(inputs["salary"]),
    ], axis=1)
