from pathmentor_core.errors_constants import DIR_ERROR, FILE_ERROR
from pathmentor_infrastructure.pathmentor_dataset_builder import PathMentorDatasetBuilder
from pathmentor_usecases.dataset.commands.prepare_dataset_command import PrepareDatasetCommand

class PrepareDatasetCommandHandler():
    def handle(self, request: PrepareDatasetCommand):
        pathmentor_dataset_builder = PathMentorDatasetBuilder()
        try:
            prepared_dataset_path = pathmentor_dataset_builder.prepare(request.built_dataset_path, request.output_path)
        except FileNotFoundError as e:
            return e.strerror, FILE_ERROR
        except PermissionError as e:
            return e.strerror, DIR_ERROR
        
        return prepared_dataset_path, None
