using Microsoft.AspNetCore.Mvc;
using PathMentor.Contracts.Skills.Responses;

namespace PathMentor.Model.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SkillsController : ControllerBase
    {
        // GET: api/skills/all
        [HttpGet]
        [Route("all")]
        public async Task<ActionResult<IEnumerable<SkillResponse>>> GetAsync()
        {
            List<string> skills = new List<string> { "C#", "Java", "Python" };
            return Ok(skills);
        }
    }
}