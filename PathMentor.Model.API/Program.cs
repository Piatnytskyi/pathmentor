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

using (var scope = app.Services.CreateScope())
{
    PathMentorModelDbContext pathMentorModelDbContext = scope.ServiceProvider.GetRequiredService<PathMentorModelDbContext>();
    pathMentorModelDbContext.Database.Migrate();
}

app.Run();
