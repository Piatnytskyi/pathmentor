using Microsoft.AspNetCore.Mvc;

namespace PathMentor.Model.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SkillsController : ControllerBase
    {
        // GET: api/skills/all
        [HttpGet]
        [Route("all")]
        public ActionResult<IEnumerable<string>> Get()
        {
            var skills = new List<string> { "C#", "Java", "Python" };
            return Ok(skills);
        }
    }
}