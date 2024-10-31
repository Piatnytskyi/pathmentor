using MediatR;
using PathMentor.Core.Entities;

namespace PathMentor.UseCases.Categories.Queries.GetSalaries
{
    public record GetSalariesQuery : IRequest<IEnumerable<Salary>>;
}

