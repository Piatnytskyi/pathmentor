import sys

from pathmentor_core.errors_constants import FILE_ERROR
from pathmentor_usecases.dataset.commands.build_dataset_command import BuildDatasetCommand

class BuildDatasetCommandHandler():
    def handle(self, request: BuildDatasetCommand):
        print("build")
        return None, None
