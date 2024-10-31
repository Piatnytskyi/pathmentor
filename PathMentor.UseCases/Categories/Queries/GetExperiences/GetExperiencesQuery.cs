using MediatR;
using PathMentor.Core.Entities;

namespace PathMentor.UseCases.Categories.Queries.GetExperiences
{
    public record GetExperiencesQuery : IRequest<IEnumerable<Experience>>;
}
