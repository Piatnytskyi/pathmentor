using PathMentor.Core.Requests;
using PathMentor.Infrastructure.Services.Abstractions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace PathMentor.Test.API.Controllers
{
    [Route("test")]
    [ApiController]
    public class TestController : ControllerBase
    {
        [HttpGet("test-auth")]
        [Authorize]
        public IActionResult TestAuth()
        {
            Guid id = Guid.Parse(HttpContext.User.FindFirstValue(ClaimTypes.NameIdentifier));
            return Ok($"Hello, it's {id}!"); 
        }

        [HttpGet("test")]
        public IActionResult Test()
        {
            return Ok($"Hello World!"); 
        }
    }
}
