using MediatR;
using Microsoft.EntityFrameworkCore;
using PathMentor.Core.Entities;
using PathMentor.Data;

namespace PathMentor.UseCases.Categories.Queries.GetSkills
{
    public class GetSkillsQueryHandler : IRequestHandler<GetSkillsQuery, IEnumerable<Skill>>
    {
        private readonly PathMentorModelDbContext _pathMentorModelDbContext;

        public GetSkillsQueryHandler(PathMentorModelDbContext pathMentorModelDbContext)
        {
            _pathMentorModelDbContext = pathMentorModelDbContext;
        }

        public async Task<IEnumerable<Skill>> Handle(GetSkillsQuery request, CancellationToken cancellationToken)
        {
            return await _pathMentorModelDbContext.Skills.ToListAsync(cancellationToken);
        }
    }
}