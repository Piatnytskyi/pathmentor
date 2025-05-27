import psycopg
from pathmentor_core.errors_constants import DB_READ_ERROR, DB_WRITE_ERROR, SUCCESS
from pathmentor_infrastructure.pathmentor_database_stager import PathMentorDatabaseStager
from pathmentor_usecases.model.commands.stage_database_command import StageDatabaseCommand

class StageDatabaseCommandHandler():
    def handle(self, request: StageDatabaseCommand):
        pathmentor_dataset_stager = PathMentorDatabaseStager()
        try:
            pathmentor_dataset_stager.stage(request.connection_string)
        except psycopg.OperationalError as e:
            return e.pgresult.error_message, DB_READ_ERROR 
        except psycopg.Error as e:
            return e.pgresult.error_message, DB_WRITE_ERROR
        
        return SUCCESS, None
