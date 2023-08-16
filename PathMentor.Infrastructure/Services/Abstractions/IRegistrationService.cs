using PathMentor.Core.Requests;
using PathMentor.Data.Entities;

namespace PathMentor.Infrastructure.Services.Abstractions
{
    public interface IRegistrationService
    {
        public Task<User?> Register(RegisterRequest registerRequest);
    }
}
