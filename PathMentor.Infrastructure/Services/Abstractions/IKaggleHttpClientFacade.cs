using PathMentor.Contracts.Kaggle.Responses;

namespace PathMentor.Infrastructure.Services.Abstractions
{
    public interface IKaggleHttpClientFacade
    {
        Task DownloadDatasetFilesAsync(string datasetName, string targetDirectory, bool unzip = false);
        Task DownloadCompetitionFilesAsync(string competitionName, string targetDirectory);
    }
}