using PathMentor.Data.Models;
using PathMentor.Infrastructure.Configurations;
using PathMentor.Infrastructure.Services.Abstractions;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class TokenGeneratorService : ITokenGeneratorService
    {
        public SerializedJWTToken GenerateToken(TokenConfiguration tokenConfiguration, IEnumerable<Claim> claims = null)
        {
            SecurityKey key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(tokenConfiguration.TokenSecret));
            SigningCredentials credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
            DateTime expirationTime = DateTime.UtcNow.AddMinutes(tokenConfiguration.TokenExpirationMinutes);

            JwtSecurityToken token = new JwtSecurityToken(
                tokenConfiguration.Issuer,
                tokenConfiguration.Audience,
                claims,
                DateTime.UtcNow,
                expirationTime,
                credentials);

            return new SerializedJWTToken() { Value = new JwtSecurityTokenHandler().WriteToken(token), ExpirationTime = expirationTime };
        }
    }
}
