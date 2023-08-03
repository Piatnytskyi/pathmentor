using PathMentor.Core.Requests;
using PathMentor.Data.Entities;
using PathMentor.Infrastructure.Services.Abstractions;
using Mapster;
using Microsoft.AspNetCore.Identity;
using System.Security.Claims;
using System.Transactions;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class RegistrationService : IRegistrationService
    {
        private readonly UserManager<User> _userManager;

        public RegistrationService(UserManager<User> userManager)
        {
            _userManager = userManager;
        }

        public async Task<User?> Register(RegisterRequest registerRequest)
        {
            User user = registerRequest.Adapt<User>();

            using (var scope = new TransactionScope(TransactionScopeAsyncFlowOption.Enabled))
            {
                try
                {
                    List<IdentityResult> results = new List<IdentityResult>();

                    results.Add(await _userManager.CreateAsync(user, registerRequest.Password));

                    List<Claim> claims = new List<Claim>();
                    claims.Add(new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()));
                    claims.Add(new Claim(ClaimTypes.Name, registerRequest.UserName));
                    claims.Add(new Claim(ClaimTypes.Email, registerRequest.Email));

                    results.Add(await _userManager.AddClaimsAsync(user, claims));

                    if (results.Any(r => !r.Succeeded))
                        throw new Exception(results.FirstOrDefault(r => !r.Succeeded)?.Errors.FirstOrDefault()?.Description);

                    //TODO: Add mail conformation.

                    scope.Complete();
                }
                catch (Exception ex)
                {
                    scope.Dispose();
                    return null;
                }
            }

            return user;
        }
    }
}
