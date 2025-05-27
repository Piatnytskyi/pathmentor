using PathMentor.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public static class PathMentorModelDatabaseSeeder
    {
        public static async Task EnsurePopulated(
            PathMentorModelDbContext context,
            IConfiguration configuration,
            ILogger logger)
        {
            if (context.Database.GetPendingMigrations().Any())
                context.Database.Migrate();

            if (context.Interactions.Any())
                return;
           
            using (HttpClient client = new HttpClient())
            {
                try
                {
                    (await client
                        .SendAsync(
                            new HttpRequestMessage(
                                HttpMethod.Post,
                                new Uri(configuration["AzureFunctions:PathMentorETLHttpTriggerUrl"]!))))
                        .EnsureSuccessStatusCode();

                    logger.LogInformation("ETL function launched successfully!");
                }
                catch (Exception e)
                {
                    logger.LogError(e, "Error launching ETL function!");
                    return;
                }
            }
        }
    }
}