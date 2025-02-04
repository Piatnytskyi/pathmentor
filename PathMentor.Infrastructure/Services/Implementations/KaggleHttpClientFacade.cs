using System.IO.Compression;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using PathMentor.Contracts.Kaggle.Responses;
using PathMentor.Infrastructure.Services.Abstractions;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class KaggleHttpClientFacade : IKaggleHttpClientFacade
    {
        private readonly HttpClient _httpClient;
        private readonly string _baseApiUrl = "https://www.kaggle.com/api/v1/";

        public KaggleHttpClientFacade(string username, string key)
        {
            _httpClient = new HttpClient();
            string authToken = Convert.ToBase64String(Encoding.ASCII.GetBytes($"{username + ":" + key}"));
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", authToken);
        }

        public async Task DownloadDatasetFilesAsync(string datasetName, string targetDirectory, bool unzip = false)
        {
            string targetPath = Path.Combine(targetDirectory, datasetName);
            
            if (Path.GetDirectoryName(targetPath) is string actualTargetDirectory)
                Directory.CreateDirectory(actualTargetDirectory);
            using (Stream responseStream = await _httpClient.GetStreamAsync(_baseApiUrl + "datasets/download/" + datasetName))
            using (FileStream fileStream = new FileStream(targetPath, FileMode.Create, FileAccess.Write, FileShare.None))
                await responseStream.CopyToAsync(fileStream);
            
            if (unzip)
                ZipFile.ExtractToDirectory(targetPath, targetDirectory, true);
        }

        public async Task DownloadCompetitionFilesAsync(string competitionName, string targetDirectory)
        {
            CompetitionsListResponse? competitionsList = await _httpClient.GetFromJsonAsync<CompetitionsListResponse>(_baseApiUrl + "competitions/data/list/" + competitionName);
            if (competitionsList == null)
                return;

            IEnumerable<Task> downloadTasks = competitionsList.Files.Select(async file =>
            {
                string filePath = Path.Combine(targetDirectory, file.Name + ".zip");
                string? fileDirectory = Path.GetDirectoryName(filePath);
                if (fileDirectory != null)
                    Directory.CreateDirectory(fileDirectory);
                using (Stream responseStream = await _httpClient.GetStreamAsync(
                    _baseApiUrl + "competitions/data/download/" + competitionName + "/" + Uri.EscapeDataString(file.Name)))
                using (FileStream fileStream = new FileStream(filePath, FileMode.Create, FileAccess.Write, FileShare.None))
                    await responseStream.CopyToAsync(fileStream);

                ZipFile.ExtractToDirectory(filePath, targetDirectory, true);
            });

            await Task.WhenAll(downloadTasks);
        }
    }
}