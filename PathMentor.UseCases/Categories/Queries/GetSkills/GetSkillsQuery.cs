using MediatR;
using PathMentor.Core.Entities;

namespace PathMentor.UseCases.Categories.Queries.GetSkills
{
    public record GetSkillsQuery : IRequest<IEnumerable<Skill>>;
}
