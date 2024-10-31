
using Microsoft.Extensions.DependencyInjection;
using FluentValidation;

namespace PathMentor.UseCases
{
    public static class IServiceCollectionExtensions
    {
        public static IServiceCollection AddUseCases(this IServiceCollection services)
        {
            services.AddMediatR(options =>
            {
                options.RegisterServicesFromAssembly(typeof(IServiceCollectionExtensions).Assembly);

                // options.AddOpenBehavior(typeof(AuthorizationBehavior<,>));
                // options.AddOpenBehavior(typeof(ValidationBehavior<,>));
            });

            services.AddValidatorsFromAssemblyContaining(typeof(IServiceCollectionExtensions));
            return services;
        }
    }
}