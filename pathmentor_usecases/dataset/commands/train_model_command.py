from pathlib import Path

class TrainModelCommand():
    def __init__(self, output_path: Path, connection_string: str):
        self.output_path = output_path
        self.connection_string = connection_string
