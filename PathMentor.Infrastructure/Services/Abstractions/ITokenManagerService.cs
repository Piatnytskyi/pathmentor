using PathMentor.Core.Responses;
using PathMentor.Data.Entities;

namespace PathMentor.Infrastructure.Services.Abstractions
{
    public interface ITokenManagerService
    {
        public Task<AuthenticationTokensResponse> GetTokens(User user);
    }
}
