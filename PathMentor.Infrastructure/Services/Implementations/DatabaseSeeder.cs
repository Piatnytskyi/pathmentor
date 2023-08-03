using PathMentor.Infrastructure.Services.Abstractions;
using Microsoft.AspNetCore.Identity;
using PathMentor.Data.Entities;
using System.Security.Claims;
using System.Transactions;
using PathMentor.Data;
using Microsoft.EntityFrameworkCore;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class DatabaseSeeder : IDatabaseSeeder
    {
        private readonly PathMentorAuthDbContext _pathmentorAuthDbContext;
        private readonly UserManager<User> _userManager;

        public DatabaseSeeder(
            PathMentorAuthDbContext pathmentorAuthDbContext,
            UserManager<User> userManager)
        {
            _pathmentorAuthDbContext = pathmentorAuthDbContext;
            _userManager = userManager;
        }

        public async Task Seed()
        {
            if (_userManager.Users.FirstOrDefault() is not null)
                return;

            using (var scope = new TransactionScope(TransactionScopeAsyncFlowOption.Enabled))
            {
                try
                {
                    PasswordHasher<User> passwordHasher = new PasswordHasher<User>();

                    User test = new User()
                    {
                        Id = Guid.NewGuid(),
                        UserName = "Test",
                        NormalizedUserName = "TEST",
                        Email = "test@test.com",
                        NormalizedEmail = "TEST@TEST.COM",
                        LockoutEnabled = false,
                        PhoneNumber = "1234567890"
                    };

                    var results = new List<IdentityResult>();
                    results.Add(await _userManager.CreateAsync(test, "Password_123"));

                    results.Add(await _userManager.AddClaimsAsync(test, new[]
                    {
                        new Claim(ClaimTypes.NameIdentifier, test.Id.ToString()),
                        new Claim(ClaimTypes.Email, test.Email),
                        new Claim(ClaimTypes.Name, test.UserName)
                    }));

                    if (results.Any(r => !r.Succeeded))
                        throw new Exception(results.FirstOrDefault()?.Errors.FirstOrDefault()?.Description);

                    scope.Complete();
                }
                catch (Exception ex)
                {
                    throw;
                }
            }
        }
    }
}
