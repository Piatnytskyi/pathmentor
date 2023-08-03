using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using PathMentor.Data.Entities;

//dotnet ef migrations add [MigrationName] --project PathMentor.Data --startup-project PathMentor.Test.API --context PathMentorTestDbContext

namespace PathMentor.Data
{
    public class PathMentorTestDbContext : DbContext
    {
        public PathMentorTestDbContext(DbContextOptions options) : base(options) { }
    }
}
