from pathlib import Path

class PrepareDatasetCommand():
    def __init__(self, built_dataset_path: Path, output_path: Path):
        self.built_dataset_path = built_dataset_path
        self.output_path = output_path
