using PathMentor.Core.Requests;
using PathMentor.Data;
using PathMentor.Data.Entities;
using PathMentor.Infrastructure.Services.Abstractions;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

namespace PathMentor.Infrastructure.Services.Implementations
{
    public class UserService : IUserService
    {
        private readonly UserManager<User> _userManager;
        private readonly PathMentorAuthDbContext _pathmentorAuthDbContext;

        public UserService(
            UserManager<User> userManager, 
            PathMentorAuthDbContext pathmentorAuthDbContext)
        {
            _userManager = userManager;
            _pathmentorAuthDbContext = pathmentorAuthDbContext;
        }

        public async Task<User?> GetUserAsync(Guid id)
        {
            User? user = await _userManager.Users
                .FirstOrDefaultAsync(u => u.Id == id);
            return user;
        }

        public async Task<IEnumerable<User>> GetUsersAsync(PaginationRequest paginationRequest, FilterRequest filterRequest)
        {
            int count = await _userManager.Users.CountAsync();
            IEnumerable<User> users = await _pathmentorAuthDbContext.Users
                .Skip((paginationRequest.Page - 1) * paginationRequest.Count)
                .Take(paginationRequest.Count)
                .ToListAsync();

            return users;
        }
    }
}
