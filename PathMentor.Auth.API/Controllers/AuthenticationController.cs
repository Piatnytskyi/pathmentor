using PathMentor.Data.Models;
using PathMentor.Core.Requests;
using PathMentor.Core.Responses;
using PathMentor.Infrastructure.Services.Abstractions;
using PathMentor.Data;
using Mapster;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Security.Claims;
using PathMentor.Data.Entities;

namespace PathMentor.Auth.API.Controllers
{
    [ApiController]
    [Route("authentication")]
    public class AuthenticationController : ControllerBase
    {
        private readonly PathMentorAuthDbContext _pathmentorAuthDbContext;
        private readonly ITokenManagerService _tokenManagerService;
        private readonly IRefreshTokenValidatorService _refreshTokenValidatorService;
        private readonly UserManager<User> _userManager;
        private readonly ILogger<AuthenticationController> _logger;

        public AuthenticationController(
            PathMentorAuthDbContext pathmentorAuthDbContext,
            ITokenManagerService tokenManagerService,
            IRefreshTokenValidatorService refreshTokenValidatorService,
            UserManager<User> userManager,
            ILogger<AuthenticationController> logger)
        {
            _pathmentorAuthDbContext = pathmentorAuthDbContext;
            _tokenManagerService = tokenManagerService;
            _refreshTokenValidatorService = refreshTokenValidatorService;
            _userManager = userManager;
            _logger = logger;
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginRequest loginRequest)
        {
            User user = await _userManager.FindByNameAsync(loginRequest.Username);
            if (user is null)
                return Unauthorized();

            bool isCorrectPassword = await _userManager.CheckPasswordAsync(user, loginRequest.Password);
            if (!isCorrectPassword)
                return Unauthorized();

            return Ok(await _tokenManagerService.GetTokens(user));
        }

        [HttpPost("refresh-token")]
        public async Task<IActionResult> RefreshToken([FromBody] RefreshTokenRequest refreshRequest)
        {
            SerializedJWTToken serializedJWTToken = refreshRequest.Adapt<SerializedJWTToken>();

            bool isRefreshTokenValid = _refreshTokenValidatorService.Validate(serializedJWTToken);
            if (!isRefreshTokenValid)
                return BadRequest(new ErrorResponse("Invalid refresh token."));

            SerializedRefreshJWTToken? serializedRefreshJWTToken =
                _pathmentorAuthDbContext.SerializedRefreshJWTTokens
                    .SingleOrDefault(srkt => srkt.Value == refreshRequest.Value);
            if (serializedRefreshJWTToken is null)
                return NotFound(new ErrorResponse("Invalid refresh token."));

            User user = await _userManager.FindByIdAsync(serializedRefreshJWTToken.UserId.ToString());
            return Ok(
                await _tokenManagerService.GetTokens(user));
        }

        [Authorize]
        [HttpDelete("logout")]
        public async Task<IActionResult> Logout()
        {
            string rawUserId = HttpContext.User.FindFirstValue(ClaimTypes.NameIdentifier);

            if (!Guid.TryParse(rawUserId, out Guid userId))
                return Unauthorized();

            IEnumerable<SerializedRefreshJWTToken> refreshTokens =
                await _pathmentorAuthDbContext.SerializedRefreshJWTTokens.Where(srjt => srjt.UserId == userId).ToListAsync();
            _pathmentorAuthDbContext.SerializedRefreshJWTTokens.RemoveRange(refreshTokens);
            await _pathmentorAuthDbContext.SaveChangesAsync();

            return Ok(userId);
        }
    }
}