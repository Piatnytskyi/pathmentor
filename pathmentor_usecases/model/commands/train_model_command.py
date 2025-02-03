from pathlib import Path

class TrainModelCommand():
    def __init__(self, connection_string: str, output_path: Path):
        self.connection_string = connection_string
        self.output_path = output_path
