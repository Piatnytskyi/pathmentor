import tensorflow_recommenders as tfrs

class PahtmentorModel(tfrs.Model):

    def __init__(self, query_model, candidate_model, metrics):
        super().__init__()

        self._query_model = query_model
        self._candidate_model = candidate_model

        self._task = tfrs.tasks.Retrieval(
            metrics=metrics
        )

    def compute_loss(self, features, training=False):
        query_embedding = self._query_model({
          "skills": features["context_skill"],
          "title": features["context_user_title"],
          "experience": features["context_user_experience"],
          "salary": features["context_user_salary"],
        })       
        candidate_embedding = self._candidate_model(features["label_skill"])

        return self._task(query_embedding, candidate_embedding, compute_metrics=not training)