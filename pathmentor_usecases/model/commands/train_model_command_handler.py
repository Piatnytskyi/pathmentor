from pathmentor_core.errors_constants import MODEL_TRAIN_ERROR, SUCCESS
from pathmentor_infrastructure.pathmentor_model_trainer import PathMentorModelTrainer
from pathmentor_usecases.model.commands.train_model_command import TrainModelCommand

class TrainModelCommandHandler():
    def handle(self, request: TrainModelCommand):
        pathmentor_dataset_builder = PathMentorModelTrainer(request.connection_string)
        try:
            pathmentor_dataset_builder.train(request.output_path)
        except Exception as e:
            return e.strerror, MODEL_TRAIN_ERROR
        
        return SUCCESS, None
