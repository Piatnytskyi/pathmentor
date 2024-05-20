using PathMentor.Data;
using PathMentor.Data.Entities;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.EntityFrameworkCore;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class PathMentorModelDatabaseSeeder
    {
        public static void EnsurePopulated(IApplicationBuilder app)
        {
            

            using (var scope = app.ApplicationServices.CreateScope())
            {
                PathMentorModelDbContext context = scope.ServiceProvider.GetRequiredService<PathMentorModelDbContext>();
                    
                if (context.Database.GetPendingMigrations().Any())
                {
                    context.Database.Migrate();
                }
            }
        }
    }
}