using AutoMapper;
using PathMentor.Core.Entities;
using PathMentor.Contracts.Categories.Responses;

namespace PathMentor.Model.API.Profiles
{
    public class SalaryProfile : Profile
    {
        public SalaryProfile()
        {
            CreateMap<Salary, SalaryResponse>();
        }
    }
}
