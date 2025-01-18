using System.Reflection;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Npgsql.EntityFrameworkCore.PostgreSQL.Infrastructure.Internal;
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
        
        private readonly string _connectionString;

        public PathMentorModelDbContext(string connectionString)
        {
            _connectionString = connectionString;
        }

        public PathMentorModelDbContext(DbContextOptions<PathMentorModelDbContext> options, IConfiguration configuration) : base(options)
        {
            _connectionString = configuration["ConnectionStrings:DefaultConnection"]!;
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseNpgsql(_connectionString);
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            modelBuilder.ApplyConfigurationsFromAssembly(typeof(PathMentorModelDbContext).Assembly);
        }
    }
}
