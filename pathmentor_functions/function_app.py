import os
import sys
import azure.functions as func
import logging
from mediatr import Mediator

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pathmentor_core.errors_constants import ERRORS
from pathmentor_usecases import register_prediction_handlers
from pathmentor_usecases.model.queries.skills_prediction_query import SkillsPredictionQuery

register_prediction_handlers()
mediator = Mediator()

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="pathmentor_model_http_trigger", methods=['get'])
def pathmentor_model_http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        query = SkillsPredictionQuery(
            skills=req.params.get('skills', '').split(','),
            title=req.params.get('title', ''),
            experience=req.params.get('experience', ''),
            salary=req.params.get('salary', ''),
            count=int(req.params.get('count', 10))
        )
        result, error = mediator.send(query)
    except ValueError:
        pass

    if error:
        return func.HttpResponse(
            f'"{ERRORS[error]}": {result}',
            status_code=500
        )
    else:
        return func.HttpResponse(status_code=200)
    