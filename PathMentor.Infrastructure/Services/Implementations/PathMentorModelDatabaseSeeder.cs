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
           
            HttpClient client = new HttpClient();
            client.BaseAddress = new Uri(configuration["AzureFunctions:PathmentorETLHttpTriggerUrl"]!);

            try
            {
                (await client.PostAsync("", new StringContent(""))).EnsureSuccessStatusCode();
            }
            catch (Exception e)
            {
                logger.LogError(e, "Error launching ETL function!");
                return;
            }
        }
    }
}