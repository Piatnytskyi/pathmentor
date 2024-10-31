using MediatR;
using PathMentor.Core.Entities;

namespace PathMentor.UseCases.Categories.Queries.GetTitles
{
    public record GetTitlesQuery : IRequest<IEnumerable<Title>>;
}
