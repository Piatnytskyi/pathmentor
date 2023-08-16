using PathMentor.Data.Models;
using PathMentor.Infrastructure.Configurations;
using PathMentor.Infrastructure.Services.Abstractions;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Text;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class RefreshTokenValidatorService : IRefreshTokenValidatorService
    {
        private readonly AuthenticationConfiguration _authenticationConfiguration;

        public RefreshTokenValidatorService(IOptions<AuthenticationConfiguration> authenticationConfiguration)
        {
            _authenticationConfiguration = authenticationConfiguration.Value;
        }

        public bool Validate(SerializedJWTToken refreshToken)
        {
            TokenValidationParameters validationParameters = new TokenValidationParameters()
            {
                IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_authenticationConfiguration.RefreshToken.TokenSecret)),
                ValidIssuer = _authenticationConfiguration.RefreshToken.Issuer,
                ValidAudience = _authenticationConfiguration.RefreshToken.Audience,
                ValidateIssuerSigningKey = true,
                ValidateIssuer = true,
                ValidateAudience = true,
                ClockSkew = TimeSpan.Zero
            };

            JwtSecurityTokenHandler tokenHandler = new JwtSecurityTokenHandler();

            try
            {
                tokenHandler.ValidateToken(refreshToken.Value, validationParameters, out SecurityToken validatedToken);
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }
    }
}
