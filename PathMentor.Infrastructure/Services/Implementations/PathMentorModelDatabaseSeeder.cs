using PathMentor.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public static class PathMentorModelDatabaseSeeder
    {
        public static async Task EnsurePopulated(
            PathMentorModelDbContext context,
            IConfiguration configuration)
        {
            if (context.Database.GetPendingMigrations().Any())
                context.Database.Migrate();

            if (context.Interactions.Any())
                return;
           
            HttpClient client = new HttpClient();
            client.BaseAddress = new Uri(configuration["AzureFunctions:PathmentorETLHttpTriggerUrl"]!);
            (await client.PostAsync("", new StringContent(""))).EnsureSuccessStatusCode();
        }
    }
}