using System.Net;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Batch;
using Microsoft.Azure.Batch.Auth;
using Microsoft.Azure.Batch.Common;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using PathMentor.Infrastructure.Configurations;
using PathMentor.Infrastructure.Services.Abstractions;

namespace PathMentor.Functions
{
    public class PathMentorETLHttpTrigger
    {
        private readonly ILogger<PathMentorETLHttpTrigger> _logger;
        private readonly IKaggleHttpClientFacade _kaggleHttpClientFacade;
        private readonly IBlobContainerFacade _blobContainerFacade;
        private readonly IConfiguration _configuration;
        private readonly IOptions<AzureBatchOptions> _azureBatchOptions;

        public PathMentorETLHttpTrigger(
            ILogger<PathMentorETLHttpTrigger> logger,
            IKaggleHttpClientFacade kaggleHttpClientFacade,
            IBlobContainerFacade blobContainerFacade,
            IConfiguration configuration,
            IOptions<AzureBatchOptions> azureBatchOptions)
        {
            _logger = logger;
            _kaggleHttpClientFacade = kaggleHttpClientFacade;
            _blobContainerFacade = blobContainerFacade;
            _configuration = configuration;
            _azureBatchOptions = azureBatchOptions;
        }

        [Function("PathMentorETLHttpTrigger")]
        public async Task<IActionResult> Run([HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequest req)
        {
            await Task.WhenAll(
                _kaggleHttpClientFacade.DownloadDatasetFilesAsync("kaggle/kaggle-survey-2018", "./datasets", true),
                _kaggleHttpClientFacade.DownloadCompetitionFilesAsync("kaggle-survey-2020", "./datasets"),
                _kaggleHttpClientFacade.DownloadCompetitionFilesAsync("kaggle-survey-2021", "./datasets"),
                _kaggleHttpClientFacade.DownloadCompetitionFilesAsync("kaggle-survey-2022", "./datasets")
            );

            await _blobContainerFacade.UploadBlobAsync(
                "multipleChoiceResponses.csv",
                "./datasets/multipleChoiceResponses.csv",
                true);
            await _blobContainerFacade.UploadBlobAsync(
                "kaggle_survey_2020_responses.csv",
                "./datasets/kaggle_survey_2020_responses.csv",
                true);
            await _blobContainerFacade.UploadBlobAsync(
                "kaggle_survey_2021_responses.csv",
                "./datasets/kaggle_survey_2021_responses.csv",
                true);
            await _blobContainerFacade.UploadBlobAsync(
                "kaggle_survey_2022_responses.csv",
                "./datasets/kaggle_survey_2022_responses.csv",
                true);

            BatchSharedKeyCredentials batchSharedKeyCredentials = new BatchSharedKeyCredentials(
                _azureBatchOptions.Value.BaseUrl,
                _azureBatchOptions.Value.AccountName,
                _azureBatchOptions.Value.AccountKey);
            using (BatchClient batchClient = BatchClient.Open(batchSharedKeyCredentials))
            {
                string packagesInstallCommand = "/bin/bash -c \"sudo apt-get -y update && sudo dpkg --configure -a" +
                    " && sudo apt-get install -y python3-pip && pip3 install --upgrade pip" +
                    " && cd $AZ_BATCH_APP_PACKAGE_pathmentor_dataset_cli" +
                    " && pip3 install -r pathmentor_dataset_cli/requirements.txt";
                UserIdentity defaultUserIdentity = new UserIdentity(new AutoUserSpecification(AutoUserScope.Task, ElevationLevel.Admin));
                List<ApplicationPackageReference> applicationPackageReferences = new List<ApplicationPackageReference>
                {
                    new ApplicationPackageReference
                    {
                        ApplicationId = "pathmentor_dataset_cli"
                    }
                };
                List<CloudTask> tasks = new List<CloudTask>
                {
                    new CloudTask(
                        "build",
                        packagesInstallCommand +
                        " && python3 -m pathmentor_dataset_cli build $AZ_BATCH_TASK_WORKING_DIR/built_database.csv\"")
                    {
                        ResourceFiles = new List<ResourceFile>
                        {
                            ResourceFile.FromAutoStorageContainer(
                                _blobContainerFacade.Name,
                                blobPrefix: "multipleChoiceResponses.csv"),
                            ResourceFile.FromAutoStorageContainer(
                                _blobContainerFacade.Name,
                                blobPrefix: "kaggle_survey_2020_responses.csv"),
                            ResourceFile.FromAutoStorageContainer(
                                _blobContainerFacade.Name,
                                blobPrefix: "kaggle_survey_2021_responses.csv"),
                            ResourceFile.FromAutoStorageContainer(
                                _blobContainerFacade.Name,
                                blobPrefix: "kaggle_survey_2022_responses.csv")
                        },
                        UserIdentity = defaultUserIdentity,
                        ApplicationPackageReferences = applicationPackageReferences,
                        OutputFiles = new List<OutputFile>
                        {
                            new OutputFile(
                                "built_database.csv",
                                new OutputFileDestination(
                                    new OutputFileBlobContainerDestination(
                                        _blobContainerFacade.Uri.ToString(),
                                        new ComputeNodeIdentityReference(),
                                        "built_database.csv")),
                                new OutputFileUploadOptions(OutputFileUploadCondition.TaskSuccess))
                        }
                    },
                    new CloudTask(
                        "prepare",
                        packagesInstallCommand +
                        " && python3 -m pathmentor_dataset_cli prepare $AZ_BATCH_TASK_WORKING_DIR/built_database.csv $AZ_BATCH_TASK_WORKING_DIR/prepared_database.csv\"")
                    {
                        UserIdentity = defaultUserIdentity,
                        ApplicationPackageReferences = applicationPackageReferences,
                        DependsOn = TaskDependencies.OnId("build"),
                        ResourceFiles = new List<ResourceFile>
                        {
                            ResourceFile.FromAutoStorageContainer(
                                _blobContainerFacade.Name,
                                blobPrefix: "built_database.csv")
                        },
                        OutputFiles = new List<OutputFile>
                        {
                            new OutputFile(
                                "prepared_database.csv",
                                new OutputFileDestination(new OutputFileBlobContainerDestination(
                                    _blobContainerFacade.Uri.ToString(),
                                    new ComputeNodeIdentityReference(),
                                    "prepared_database.csv")),
                                new OutputFileUploadOptions(OutputFileUploadCondition.TaskSuccess))
                        }
                    },
                    new CloudTask(
                        "normalize",
                        packagesInstallCommand +
                        " && python3 -m pathmentor_dataset_cli normalize $AZ_BATCH_TASK_WORKING_DIR/prepared_database.csv\"")
                    {
                        UserIdentity = defaultUserIdentity,
                        ApplicationPackageReferences = applicationPackageReferences,
                        EnvironmentSettings = new List<EnvironmentSetting>
                        {
                            new EnvironmentSetting("ConnectionStrings__DefaultConnection", _configuration["ConnectionStrings:DefaultConnection"])
                        },
                        DependsOn = TaskDependencies.OnId("prepare"),
                        ResourceFiles = new List<ResourceFile>
                        {
                            ResourceFile.FromAutoStorageContainer(
                                _blobContainerFacade.Name,
                                blobPrefix: "prepared_database.csv")
                        },
                    }
                };

                foreach (CloudTask task in tasks)
                {
                    try
                    {                    
                        await batchClient.JobOperations.GetTaskAsync("pathmentor_dataset", task.Id);
                        await batchClient.JobOperations.DeleteTaskAsync("pathmentor_dataset", task.Id);
                    }
                    catch (BatchException ex) when (ex.RequestInformation.HttpStatusCode == HttpStatusCode.NotFound)
                    {
                        _logger.LogInformation("Task " + task.Id + " does not exist");
                    }
                }

                await batchClient.JobOperations.AddTaskAsync("pathmentor_dataset", tasks);
            }
            return new OkResult();
        }
    }
}
