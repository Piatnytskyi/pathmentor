using MediatR;
using Microsoft.EntityFrameworkCore;
using PathMentor.Core.Entities;
using PathMentor.Data;

namespace PathMentor.UseCases.Categories.Queries.GetTitles
{
    public class GetTitlesQueryHandler : IRequestHandler<GetTitlesQuery, IEnumerable<Title>>
    {
        private readonly PathMentorModelDbContext _pathMentorModelDbContext;

        public GetTitlesQueryHandler(PathMentorModelDbContext pathMentorModelDbContext)
        {
            _pathMentorModelDbContext = pathMentorModelDbContext;
        }

        public async Task<IEnumerable<Title>> Handle(GetTitlesQuery request, CancellationToken cancellationToken)
        {
            return await _pathMentorModelDbContext.Titles.ToListAsync(cancellationToken);
        }
    }
}
