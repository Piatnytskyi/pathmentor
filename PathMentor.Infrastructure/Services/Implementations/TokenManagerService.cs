using PathMentor.Data.Models;
using PathMentor.Core.Responses;
using PathMentor.Infrastructure.Configurations;
using PathMentor.Infrastructure.Services.Abstractions;
using PathMentor.Data;
using Mapster;
using Microsoft.Extensions.Options;
using System.Security.Claims;
using Microsoft.AspNetCore.Identity;
using PathMentor.Data.Entities;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class TokenManagerService : ITokenManagerService
    {
        private readonly AuthenticationConfiguration _authenticationConfiguration;
        private readonly ITokenGeneratorService _tokenGeneratorService;
        private readonly UserManager<User> _userManager;
        private readonly PathMentorAuthDbContext _pathmentorAuthDbContext;

        public TokenManagerService(
            PathMentorAuthDbContext pathmentorAuthDbContext,
            IOptions<AuthenticationConfiguration> authenticationConfiguration,
            ITokenGeneratorService tokenGeneratorService,
            UserManager<User> userManager)
        {
            _pathmentorAuthDbContext = pathmentorAuthDbContext;
            _authenticationConfiguration = authenticationConfiguration.Value;
            _tokenGeneratorService = tokenGeneratorService;
            _userManager = userManager;
        }

        public async Task<AuthenticationTokensResponse> GetTokens(User user)
        {
            IList<Claim> claims = await _userManager.GetClaimsAsync(user);
            SerializedJWTToken serializedAccessJWTToken = _tokenGeneratorService.GenerateToken(_authenticationConfiguration.AccessToken, claims);
            SerializedRefreshJWTToken serializedRefreshJWTToken = _tokenGeneratorService.GenerateToken(_authenticationConfiguration.RefreshToken).Adapt<SerializedRefreshJWTToken>();
            serializedRefreshJWTToken.UserId = user.Id;
            
            IQueryable<SerializedRefreshJWTToken> oldSerializedRefreshJWTTokens =
                _pathmentorAuthDbContext.SerializedRefreshJWTTokens.Where(srjt => srjt.UserId == user.Id);
            _pathmentorAuthDbContext.SerializedRefreshJWTTokens.RemoveRange(oldSerializedRefreshJWTTokens);

            await _pathmentorAuthDbContext.SerializedRefreshJWTTokens.AddAsync(serializedRefreshJWTToken);
            await _pathmentorAuthDbContext.SaveChangesAsync();

            return new AuthenticationTokensResponse()
            {
                AccessToken = serializedAccessJWTToken,
                RefreshToken = serializedRefreshJWTToken
            };
        }
    }
}
