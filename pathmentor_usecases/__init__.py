from mediatr import Mediator

def register_dataset_handlers():
    from pathmentor_usecases.dataset.commands.build_dataset_command_handler import BuildDatasetCommandHandler
    from pathmentor_usecases.dataset.commands.prepare_dataset_command_handler import PrepareDatasetCommandHandler
    from pathmentor_usecases.dataset.commands.normalize_dataset_command_handler import NormalizeDatasetCommandHandler

    Mediator.register_handler(BuildDatasetCommandHandler)
    Mediator.register_handler(PrepareDatasetCommandHandler)
    Mediator.register_handler(NormalizeDatasetCommandHandler)

def register_model_handlers():
    from pathmentor_usecases.model.commands.stage_database_command_handler import StageDatabaseCommandHandler
    from pathmentor_usecases.model.commands.train_model_command_handler import TrainModelCommandHandler
    
    Mediator.register_handler(StageDatabaseCommandHandler)
    Mediator.register_handler(TrainModelCommandHandler)
