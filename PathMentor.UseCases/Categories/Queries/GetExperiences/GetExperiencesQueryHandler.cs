using MediatR;
using Microsoft.EntityFrameworkCore;
using PathMentor.Core.Entities;
using PathMentor.Data;

namespace PathMentor.UseCases.Categories.Queries.GetExperiences
{
    public class GetExperiencesQueryHandler : IRequestHandler<GetExperiencesQuery, IEnumerable<Experience>>
    {
        private readonly PathMentorModelDbContext _pathMentorModelDbContext;

        public GetExperiencesQueryHandler(PathMentorModelDbContext pathMentorModelDbContext)
        {
            _pathMentorModelDbContext = pathMentorModelDbContext;
        }

        public async Task<IEnumerable<Experience>> Handle(GetExperiencesQuery request, CancellationToken cancellationToken)
        {
            return await _pathMentorModelDbContext.Experiences.ToListAsync(cancellationToken);
        }
    }
}
