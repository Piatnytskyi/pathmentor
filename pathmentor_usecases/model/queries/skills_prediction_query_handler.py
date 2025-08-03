from pathmentor_core.errors_constants import MODEL_TRAIN_ERROR, SUCCESS
from pathmentor_usecases.model.queries.skills_prediction_query import SkillsPredictionQuery

class SkillsPredictionQueryHandler():
    def handle(self, query: SkillsPredictionQuery):
        query = query
        try:
            print(query)
        except Exception as e:
            return e, MODEL_TRAIN_ERROR
        
        return SUCCESS, None
