from pathlib import Path

class NormalizeDatasetCommand():
    def __init__(self, prepared_dataset_path: Path, connection_string: str, force: bool):
        self.prepared_dataset_path = prepared_dataset_path
        self.connection_string = connection_string
        self.force = force
