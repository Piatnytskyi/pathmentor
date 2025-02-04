from pathmentor_core.errors_constants import DB_READ_ERROR, SUCCESS
from pathmentor_infrastructure.pathmentor_model_trainer import PathMentorModelTrainer
from pathmentor_usecases.dataset.commands.train_model_command import TrainModelCommand

class TrainModelCommandHandler():
    def handle(self, request: TrainModelCommand):
        pathmentor_model_trainer = PathMentorModelTrainer(request.connection_string)
        try:
            pathmentor_model_trainer.train(request.output_path)
        except Exception as e:
            return e.strerror, DB_READ_ERROR
        
        return SUCCESS, None

