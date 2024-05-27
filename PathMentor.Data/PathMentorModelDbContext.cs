using System.Reflection;
using Microsoft.EntityFrameworkCore;
using PathMentor.Core.Entities;

//dotnet ef migrations add [MigrationName] --project PathMentor.Data --startup-project PathMentor.Model.API --context PathMentorModelDbContext
namespace PathMentor.Data
{
    public class PathMentorModelDbContext : DbContext
    {
        public DbSet<Title> Titles { get; set; }
        public DbSet<Experience> Experiences { get; set; }
        public DbSet<Salary> Salaries { get; set; }
        public DbSet<Skill> Skills { get; set; }
        public DbSet<Interaction> Interactions { get; set; }
        
        public PathMentorModelDbContext(DbContextOptions<PathMentorModelDbContext> options) : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
        }
    }
}
