using PathMentor.Data;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.EntityFrameworkCore;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class PathMentorModelDatabaseSeeder
    {
        public static async Task EnsurePopulated(IApplicationBuilder app)
        {
            using (var scope = app.ApplicationServices.CreateScope())
            {
                PathMentorModelDbContext context = scope.ServiceProvider.GetRequiredService<PathMentorModelDbContext>();   
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
}