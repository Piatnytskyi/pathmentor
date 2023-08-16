using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using PathMentor.Data.Entities;

//dotnet ef migrations add [MigrationName] --project PathMentor.Data --startup-project PathMentor.Auth.API --context PathMentorAuthDbContext

namespace PathMentor.Data
{
    public class PathMentorAuthDbContext : IdentityDbContext<User, IdentityRole<Guid>, Guid>
    {
        public PathMentorAuthDbContext(DbContextOptions options) : base(options) { }

        public override DbSet<User> Users { get; set; }
        public DbSet<SerializedRefreshJWTToken> SerializedRefreshJWTTokens { get; set; }
    }
}
