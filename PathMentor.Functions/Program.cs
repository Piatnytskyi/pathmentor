using Azure.Storage.Blobs;
using Microsoft.Azure.Functions.Worker.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using PathMentor.Infrastructure.Configurations;
using PathMentor.Infrastructure.Services.Abstractions;
using PathMentor.Infrastructure.Services.Implementations;

var builder = FunctionsApplication.CreateBuilder(args);

builder.Services.Configure<AzureBatchOptions>(builder.Configuration.GetSection(nameof(AzureBatchOptions)));
builder.Services.AddScoped<IKaggleHttpClientFacade, KaggleHttpClientFacade>(s =>
    new KaggleHttpClientFacade(builder.Configuration["Kaggle:Username"]!, builder.Configuration["Kaggle:Key"]!));
builder.Services.AddScoped<IBlobContainerFacade, BlobContainerFacade>(s =>
    new BlobContainerFacade(new BlobContainerClient(builder.Configuration["AzureStorage:ConnectionString"], builder.Configuration["AzureStorage:ContainerName"])));

builder.ConfigureFunctionsWebApplication();

// Application Insights isn't enabled by default. See https://aka.ms/AAt8mw4.
// builder.Services
//     .AddApplicationInsightsTelemetryWorkerService()
//     .ConfigureFunctionsApplicationInsights();

builder.Build().Run();
