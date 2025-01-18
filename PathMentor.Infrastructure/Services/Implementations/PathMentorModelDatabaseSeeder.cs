using PathMentor.Data;
using Microsoft.EntityFrameworkCore;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class PathMentorModelDatabaseSeeder
    {
        public static async Task EnsurePopulated(
            PathMentorModelDbContext context)
        {
            if (context.Database.GetPendingMigrations().Any())
            {
                context.Database.Migrate();
            }

            if (context.Interactions.Any())
            {
                return;
            }
        }
    }
}