from pathlib import Path

class BuildDatasetCommand():
    def __init__(self, source_path: Path, output_path: Path):
        self.source_path = source_path
        self.output_path = output_path
