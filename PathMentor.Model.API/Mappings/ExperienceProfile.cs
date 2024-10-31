using AutoMapper;
using PathMentor.Core.Entities;
using PathMentor.Contracts.Categories.Responses;

namespace PathMentor.Model.API.Profiles
{
    public class ExperienceProfile : Profile
    {
        public ExperienceProfile()
        {
            CreateMap<Experience, ExperienceResponse>();
        }
    }
}
