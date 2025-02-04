import psycopg
from pathmentor_core.errors_constants import DB_READ_ERROR, DB_WRITE_ERROR, FILE_ERROR, SUCCESS
from pathmentor_infrastructure.pathmentor_dataset_builder import PathMentorDatasetBuilder
from pathmentor_usecases.dataset.commands.normalize_dataset_command import NormalizeDatasetCommand

class NormalizeDatasetCommandHandler():
    def handle(self, request: NormalizeDatasetCommand):
        pathmentor_dataset_builder = PathMentorDatasetBuilder()
        try:
            pathmentor_dataset_builder.normalize(request.prepared_dataset_path, request.connection_string, request.force)
        except FileNotFoundError as e:
            return e.strerror, FILE_ERROR
        except psycopg.OperationalError as e:
            return e.strerror, DB_READ_ERROR 
        except psycopg.Error as e:
            return e.strerror, DB_WRITE_ERROR
        
        return SUCCESS, None
