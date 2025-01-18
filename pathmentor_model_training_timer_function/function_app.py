import logging
import datetime
import azure.functions as func
from mediatr import Mediator 
from pathmentor_usecases.dataset.commands.train_model_command import TrainModelCommand

app = func.FunctionApp()
mediator = Mediator()

@app.timer_trigger(schedule="0 0 2 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def pathmentor_model_training_timer(myTimer: func.TimerRequest) -> None:
    utc_timestamp_start = datetime.datetime.now(datetime.timezone.utc).replace(
        tzinfo=datetime.timezone.utc).isoformat()
    if myTimer.past_due:
        logging.warning('The timer is past due!')

    # Lanch Azure Batch job to stage data and then train model if stage data is successful


    # sourcePath = tempfile.gettempdir()
    # connectionString = os.environ["ConnectionStrings__DefaultConnection"]
    # request = TrainModelCommand(sourcePath, connectionString)
    # _, error = mediator.send(request)

    utc_timestamp_end = datetime.datetime.now(datetime.timezone.utc).replace(
        tzinfo=datetime.timezone.utc).isoformat()

    logging.info('PathMentor model traning trigger function ran at %s and finished at %s', utc_timestamp_start, utc_timestamp_end)
