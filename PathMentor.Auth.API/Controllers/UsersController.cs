using PathMentor.Core.Requests;
using PathMentor.Core.Responses;
using PathMentor.Data.Entities;
using PathMentor.Infrastructure.Services.Abstractions;
using Mapster;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace PathMentor.Auth.API.Controllers
{
    [Route("users")]
    [ApiController]
    public class UsersController : ControllerBase
    {
        private readonly IUserService _userService;
        private readonly IRegistrationService _registrationService;
        private readonly IAuthorizationService _authorizationService;

        public UsersController(
            IRegistrationService registrationService,
            IAuthorizationService authorizationService,
            IUserService usersService)
        {
            _registrationService = registrationService;
            _authorizationService = authorizationService;
            _userService = usersService;
        }

        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] RegisterRequest registerRequest)
        {
            User? user = await _registrationService.Register(registerRequest);
            if (user is null)
                return Conflict(new ErrorResponse("Registration failed."));

            return Ok(user.Id);
        }

        [HttpGet("current")]
        [Authorize]
        public async Task<IActionResult> GetCurrentUser()
        {
            Guid id = Guid.Parse(HttpContext.User.FindFirstValue(ClaimTypes.NameIdentifier));
            User? user = await _userService.GetUserAsync(id);
            UserResponse? userResponse = user?.Adapt<UserResponse>();
            return Ok(userResponse);
        }
    }
}
