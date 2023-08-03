using PathMentor.Core.Requests;
using PathMentor.Data.Entities;

namespace PathMentor.Infrastructure.Services.Abstractions
{
    public interface IUserService
    {
        Task<User?> GetUserAsync(Guid id);
        Task<IEnumerable<User>> GetUsersAsync(PaginationRequest paginationRequest, FilterRequest filterRequest);
    }
}
