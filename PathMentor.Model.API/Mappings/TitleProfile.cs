using AutoMapper;
using PathMentor.Core.Entities;
using PathMentor.Contracts.Categories.Responses;

namespace PathMentor.Model.API.Profiles
{
    public class TitleProfile : Profile
    {
        public TitleProfile()
        {
            CreateMap<Title, TitleResponse>();
        }
    }
}
