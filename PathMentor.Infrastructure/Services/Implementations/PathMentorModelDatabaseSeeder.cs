using PathMentor.Data;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class PathMentorModelDatabaseSeeder
    {
        public static async Task EnsurePopulated(IApplicationBuilder app)
        {
            using (var scope = app.ApplicationServices.CreateScope())
            {
                KaggleHttpClientFacade kaggleHttpClientFacade = new KaggleHttpClientFacade(scope.ServiceProvider.GetRequiredService<IConfiguration>());
                await Task.WhenAll(
                    kaggleHttpClientFacade.DownloadDatasetFilesAsync("kaggle/kaggle-survey-2018", "datasets", true),
                    kaggleHttpClientFacade.DownloadCompetitionFilesAsync("kaggle-survey-2020", "datasets"),
                    kaggleHttpClientFacade.DownloadCompetitionFilesAsync("kaggle-survey-2021", "datasets"),
                    kaggleHttpClientFacade.DownloadCompetitionFilesAsync("kaggle-survey-2022", "datasets")
                );

                PathMentorModelDbContext context = scope.ServiceProvider.GetRequiredService<PathMentorModelDbContext>();
                    
                if (context.Database.GetPendingMigrations().Any())
                {
                    context.Database.Migrate();
                }
            }
        }
    }
}