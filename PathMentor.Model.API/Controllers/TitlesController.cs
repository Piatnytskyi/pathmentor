using Microsoft.AspNetCore.Mvc;

namespace PathMentor.Model.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TitlesController : ControllerBase
    {
        // GET: api/titles/all
        [HttpGet]
        [Route("all")]
        public ActionResult<IEnumerable<string>> Get()
        {
            List<string> titles = new List<string> { "Software Engineer", "Data Scientist", "Product Manager" };
            return Ok(titles);
        }
    }
}
