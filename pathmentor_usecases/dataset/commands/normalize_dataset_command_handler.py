import sys

from pathmentor_core.errors_constants import FILE_ERROR
from pathmentor_usecases.dataset.commands.normalize_dataset_command import NormalizeDatasetCommand

class NormalizeDatasetCommandHandler():
    def handle(self, request: NormalizeDatasetCommand):
        print("normalize")
        return None, None
