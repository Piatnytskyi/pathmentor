from pathmentor_core.errors_constants import FILE_ERROR, DIR_ERROR
from pathmentor_infrastructure.pathmentor_dataset_builder import PathMentorDatasetBuilder
from pathmentor_usecases.dataset.commands.build_dataset_command import BuildDatasetCommand

class BuildDatasetCommandHandler():
    def handle(self, request: BuildDatasetCommand):
        pathmentor_dataset_builder = PathMentorDatasetBuilder()
        try:
            built_dataset_path = pathmentor_dataset_builder.build(request.output_path)
        except FileNotFoundError as e:
            return e.strerror, FILE_ERROR
        except PermissionError as e:
            return e.strerror, DIR_ERROR
        
        return built_dataset_path, None
