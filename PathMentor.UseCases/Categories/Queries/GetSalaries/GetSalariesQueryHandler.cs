using MediatR;
using Microsoft.EntityFrameworkCore;
using PathMentor.Core.Entities;
using PathMentor.Data;

namespace PathMentor.UseCases.Categories.Queries.GetSalaries
{
    public class GetSalariesQueryHandler : IRequestHandler<GetSalariesQuery, IEnumerable<Salary>>
    {
        private readonly PathMentorModelDbContext _pathMentorModelDbContext;

        public GetSalariesQueryHandler(PathMentorModelDbContext pathMentorModelDbContext)
        {
            _pathMentorModelDbContext = pathMentorModelDbContext;
        }

        public async Task<IEnumerable<Salary>> Handle(GetSalariesQuery request, CancellationToken cancellationToken)
        {
            return await _pathMentorModelDbContext.Salaries.ToListAsync(cancellationToken);
        }
    }
}
