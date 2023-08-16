using PathMentor.Data.Models;

namespace PathMentor.Infrastructure.Services.Abstractions
{
    public interface IRefreshTokenValidatorService
    {
        public bool Validate(SerializedJWTToken refreshToken);
    }
}
