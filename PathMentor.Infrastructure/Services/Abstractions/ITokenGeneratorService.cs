using PathMentor.Data.Models;
using PathMentor.Infrastructure.Configurations;
using System.Security.Claims;

namespace PathMentor.Infrastructure.Services.Abstractions
{
    public interface ITokenGeneratorService
    {
        public SerializedJWTToken GenerateToken(TokenConfiguration tokenConfiguration, IEnumerable<Claim> claims = null);
    }
}
