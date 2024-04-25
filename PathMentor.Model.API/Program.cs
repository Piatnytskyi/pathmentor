using Microsoft.EntityFrameworkCore;
using PathMentor.Data;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<PathMentorModelDbContext>(options =>
{
    options.UseNpgsql(builder.Configuration["ConnectionStrings:PathMentorModelConnection"]);
});

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
