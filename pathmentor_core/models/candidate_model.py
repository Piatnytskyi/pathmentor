import tensorflow as tf

class CandidateModel(tf.keras.Model):

  def __init__(self, embedding_dimension, unique_user_skills):
    super().__init__()

    self.user_skills_embedding = tf.keras.Sequential([
      tf.keras.layers.StringLookup(
          vocabulary=unique_user_skills, mask_token=None),
      tf.keras.layers.Embedding(len(unique_user_skills) + 1, embedding_dimension),
    ])

  def call(self, skills):
    return self.user_skills_embedding(skills)
