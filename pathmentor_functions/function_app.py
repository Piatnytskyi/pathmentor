import logging
import azure.functions as func

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 2 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def pathmentor_stage_timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')


@app.queue_trigger(arg_name="azqueue", queue_name="pathmentor-stage-queue",
                               connection="AzureWebJobsStorage") 
def pathmentor_train_queue_trigger(azqueue: func.QueueMessage):
    logging.info('Python Queue trigger processed a message: %s',
                azqueue.get_body().decode('utf-8'))
    
    # sourcePath = tempfile.gettempdir()
    # connectionString = os.environ["ConnectionStrings__DefaultConnection"]
    # request = TrainModelCommand(sourcePath, connectionString)
    # _, error = mediator.send(request)

