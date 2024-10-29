using Microsoft.EntityFrameworkCore;
using PathMentor.Data;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<PathMentorModelDbContext>(options =>
{
    options.UseNpgsql(builder.Configuration["ConnectionStrings:DefaultConnection"]);
});

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddCors(builder =>
{
    builder.AddPolicy("WebClient", policyBuilder =>
    {
        policyBuilder.WithOrigins("https://localhost:5001", "http://localhost:5000");
        policyBuilder.AllowAnyMethod();
        policyBuilder.AllowAnyHeader();
        policyBuilder.AllowCredentials();
    });
});

builder.Services.AddHealthChecks();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.UseCors("WebClient");

app.MapControllers();

app.MapHealthChecks("/health");

await PathMentorModelDatabaseSeeder.EnsurePopulated(app);

app.Run();
