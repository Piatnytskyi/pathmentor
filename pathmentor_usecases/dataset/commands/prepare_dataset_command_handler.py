import sys

from pathmentor_core.errors_constants import FILE_ERROR
from pathmentor_usecases.dataset.commands.prepare_dataset_command import PrepareDatasetCommand

class PrepareDatasetCommandHandler():
    def handle(self, request: PrepareDatasetCommand):
        print("prepare")
        return None, None
