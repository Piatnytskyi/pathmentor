using AutoMapper;
using MediatR;
using Microsoft.AspNetCore.Mvc;
using PathMentor.Contracts.Categories.Responses;
using PathMentor.Core.Entities;
using PathMentor.UseCases.Categories.Queries.GetExperiences;
using PathMentor.UseCases.Categories.Queries.GetSalaries;
using PathMentor.UseCases.Categories.Queries.GetSkills;
using PathMentor.UseCases.Categories.Queries.GetTitles;

namespace PathMentor.Model.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class CategoriesController : ControllerBase
    {
        private readonly IMediator _mediator;
        private readonly IMapper _mapper;

        public CategoriesController(IMediator mediator, IMapper mapper)
        {
            _mediator = mediator;
            _mapper = mapper;
        }

        // GET: api/categories/salaries/all
        [HttpGet]
        [Route("salaries/all")]
        public async Task<ActionResult<IEnumerable<SalaryResponse>>> GetSalariesAsync(CancellationToken cancellationToken)
        {
            IEnumerable<Salary> salaries = await _mediator.Send(new GetSalariesQuery(), cancellationToken);
            return Ok(_mapper.Map<IEnumerable<SalaryResponse>>(salaries));
        }

        // GET: api/categories/experiencies/all
        [HttpGet]
        [Route("experiencies/all")]
        public async Task<ActionResult<IEnumerable<ExperienceResponse>>> GetExperienciesAsync(CancellationToken cancellationToken)
        {
            IEnumerable<Experience> experiencies = await _mediator.Send(new GetExperiencesQuery(), cancellationToken);
            return Ok(_mapper.Map<IEnumerable<ExperienceResponse>>(experiencies));
        }

        // GET: api/categories/titles/all
        [HttpGet]
        [Route("titles/all")]
        public async Task<ActionResult<IEnumerable<TitleResponse>>> GetTitlesAsync(CancellationToken cancellationToken)
        {
            IEnumerable<Title> titles = await _mediator.Send(new GetTitlesQuery(), cancellationToken);
            return Ok(_mapper.Map<IEnumerable<TitleResponse>>(titles));
        }

        // GET: api/categories/skills/all
        [HttpGet]
        [Route("skills/all")]
        public async Task<ActionResult<IEnumerable<SkillResponse>>> GetSkillsAsync(CancellationToken cancellationToken)
        {
            IEnumerable<Skill> skills = await _mediator.Send(new GetSkillsQuery(), cancellationToken);
            return Ok(_mapper.Map<IEnumerable<SkillResponse>>(skills));
        }
    }
}
