using Microsoft.AspNetCore.Mvc;

namespace PathMentor.Model.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SalariesController : ControllerBase
    {
        // GET: api/salaries/all
        [HttpGet]
        [Route("all")]
        public ActionResult<IEnumerable<string>> Get()
        {
            List<string> salaries = new List<string> { "100000", "120000", "150000" };
            return Ok(salaries);
        }
    }
}
