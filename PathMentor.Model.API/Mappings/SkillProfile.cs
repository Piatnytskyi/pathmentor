using AutoMapper;
using PathMentor.Core.Entities;
using PathMentor.Contracts.Categories.Responses;

namespace PathMentor.Model.API.Profiles
{
    public class SkillProfile : Profile
    {
        public SkillProfile()
        {
            CreateMap<Skill, SkillResponse>();
        }
    }
}
