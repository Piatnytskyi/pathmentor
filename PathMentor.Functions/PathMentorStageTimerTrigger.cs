using System.Net;
using Microsoft.Azure.Batch;
using Microsoft.Azure.Batch.Auth;
using Microsoft.Azure.Batch.Common;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using PathMentor.Infrastructure.Configurations;

namespace PathMentor.Functions
{
    public class PathMentorStageTimerTrigger
    {
        private readonly ILogger _logger;
        private readonly IConfiguration _configuration;
        private readonly IOptions<AzureBatchOptions> _azureBatchOptions;

        public PathMentorStageTimerTrigger(
            ILoggerFactory loggerFactory,
            IConfiguration configuration,
            IOptions<AzureBatchOptions> azureBatchOptions)
        {
            _logger = loggerFactory.CreateLogger<PathMentorStageTimerTrigger>();
            _configuration = configuration;
            _azureBatchOptions = azureBatchOptions;
        }

        [Function(nameof(PathMentorStageTimerTrigger))]
        public async Task Run([TimerTrigger("0 0 2 * * *")] TimerInfo timerInfo)
        {
            BatchSharedKeyCredentials batchSharedKeyCredentials = new BatchSharedKeyCredentials(
                _azureBatchOptions.Value.BaseUrl,
                _azureBatchOptions.Value.AccountName,
                _azureBatchOptions.Value.AccountKey);
            using (BatchClient batchClient = BatchClient.Open(batchSharedKeyCredentials))
            {
                CloudTask task = new CloudTask(
                    "stage",
                    "/bin/bash -c \"sudo apt-get -y update && sudo dpkg --configure -a" +
                    " && sudo apt-get install -y python3-pip && pip3 install --upgrade pip" +
                    " && cd $AZ_BATCH_APP_PACKAGE_pathmentor_model_cli" +
                    " && pip3 install -r pathmentor_model_cli/requirements.txt" +
                    " && python3 -m pathmentor_model_cli stage\"")
                {
                    UserIdentity = new UserIdentity(new AutoUserSpecification(AutoUserScope.Task, ElevationLevel.Admin)),
                    ApplicationPackageReferences = new List<ApplicationPackageReference>
                    {
                        new ApplicationPackageReference
                        {
                            ApplicationId = "pathmentor_model_cli"
                        }
                    },
                    EnvironmentSettings = new List<EnvironmentSetting>
                    {
                        new EnvironmentSetting("ConnectionStrings__DefaultConnection", _configuration["ConnectionStrings:DefaultConnection"])
                    }
                };

                try
                {
                    await batchClient.JobOperations.GetTaskAsync("pathmentor_model", task.Id);
                    await batchClient.JobOperations.DeleteTaskAsync("pathmentor_model", task.Id);
                }
                catch (BatchException ex) when (ex.RequestInformation.HttpStatusCode == HttpStatusCode.NotFound)
                {
                    _logger.LogInformation("Task does not exist");
                }

                await batchClient.JobOperations.AddTaskAsync("pathmentor_model", task);
            }
        }
    }
}
