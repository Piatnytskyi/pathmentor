using Microsoft.AspNetCore.Mvc;

namespace PathMentor.Model.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ExperienciesController : ControllerBase
    {
        // GET: api/experiencies/all
        [HttpGet]
        [Route("all")]
        public ActionResult<IEnumerable<string>> Get()
        {
            List<string> experiencies = new List<string> { "Junior", "Mid", "Senior" };
            return Ok(experiencies);
        }
    }
}
