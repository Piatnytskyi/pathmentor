using Microsoft.Azure.Functions.Worker.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using PathMentor.Infrastructure.Configurations;

var builder = FunctionsApplication.CreateBuilder(args);

builder.Services.Configure<AzureBatchOptions>(builder.Configuration.GetSection(nameof(AzureBatchOptions)));

builder.ConfigureFunctionsWebApplication();

// Application Insights isn't enabled by default. See https://aka.ms/AAt8mw4.
// builder.Services
//     .AddApplicationInsightsTelemetryWorkerService()
//     .ConfigureFunctionsApplicationInsights();

builder.Build().Run();
