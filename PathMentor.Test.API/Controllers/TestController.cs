using PathMentor.Core.Requests;
using PathMentor.Infrastructure.Services.Abstractions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace PathMentor.Test.API.Controllers
{
    [Route("test")]
    [ApiController]
    [Authorize]
    public class TestController : ControllerBase
    {
        [HttpGet("test")]
        public async Task<IActionResult> Test()
        {
            Guid id = Guid.Parse(HttpContext.User.FindFirstValue(ClaimTypes.NameIdentifier));
            return Ok($"Hello, it's {id}!"); 
        }
    }
}
