using System.IO.Compression;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using Microsoft.Extensions.Configuration;
using PathMentor.Contracts.Kaggle.Responses;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class KaggleHttpClientFacade
    {
        private readonly HttpClient _httpClient;
        private readonly string _baseApiUrl = "https://www.kaggle.com/api/v1/";

        public KaggleHttpClientFacade(IConfiguration configuration)
        {
            string? username = configuration["username"];
            string? key = configuration["key"];

            if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(key))
                throw new ArgumentException("Kaggle username and key must be provided in the configuration file.");

            _httpClient = new HttpClient();
            var authToken = Convert.ToBase64String(Encoding.ASCII.GetBytes($"{username + ":" + key}"));
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
                ZipFile.ExtractToDirectory(targetPath, targetDirectory);
        }

        public async Task DownloadCompetitionFilesAsync(string competitionName, string targetDirectory)
        {
            CompetitionsListResponse? competitionsList = await _httpClient.GetFromJsonAsync<CompetitionsListResponse>(_baseApiUrl + "competitions/data/list/" + competitionName);
            if (competitionsList == null)
                return;

            IEnumerable<Task> downloadTasks = competitionsList.Files.Select(async file =>
            {
                string friendlyFileName = Uri.EscapeDataString(file.Name);
                using (Stream responseStream = await _httpClient.GetStreamAsync(
                    _baseApiUrl + "competitions/data/download/" + competitionName + "/" + friendlyFileName))
                using (FileStream fileStream = new FileStream(
                    Path.Combine(targetDirectory, friendlyFileName),
                    FileMode.Create,
                    FileAccess.Write,
                    FileShare.None))
                {
                    await responseStream.CopyToAsync(fileStream);
                }
            });

            await Task.WhenAll(downloadTasks);
        }
    }
}
