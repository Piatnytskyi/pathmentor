using PathMentor.Infrastructure.Configurations;
using PathMentor.Infrastructure.Services.Abstractions;
using PathMentor.Infrastructure.Services.Implementations;
using PathMentor.Data;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using System.Text;
using PathMentor.Data.Entities;
using Microsoft.AspNetCore.Authorization;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddDbContext<PathMentorAuthDbContext>(options => {
    options.UseSqlServer(builder.Configuration["ConnectionStrings:PathMentorAuthConnection"]);
});

builder.Services.AddControllers();

IConfigurationSection authenticationConfigurationSection = builder.Configuration.GetSection("Authentication");
builder.Services.AddOptions<AuthenticationConfiguration>()
    .Bind(authenticationConfigurationSection)
    .ValidateDataAnnotations()
    .ValidateOnStart();

builder.Services.AddIdentityCore<User>()
    .AddEntityFrameworkStores<PathMentorAuthDbContext>();

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme).AddJwtBearer(options =>
{
    var authenticationConfiguration = authenticationConfigurationSection.Get<AuthenticationConfiguration>();

    options.TokenValidationParameters = new TokenValidationParameters()
    {
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(authenticationConfiguration.AccessToken.TokenSecret)),
        ValidIssuer = authenticationConfiguration.AccessToken.Issuer,
        ValidAudience = authenticationConfiguration.AccessToken.Audience,
        ValidateIssuerSigningKey = true,
        ValidateIssuer = true,
        ValidateAudience = true,
        ClockSkew = TimeSpan.Zero
    };
});

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo { Title = "PathMentor.Auth.API", Version = "v1" });

    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme()
    {
        Name = "Authorization",
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer",
        BearerFormat = "JWT",
        In = ParameterLocation.Header,
        Description = "JWT Authorization header using the Bearer scheme."
    });

    options.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type=ReferenceType.SecurityScheme,
                    Id="Bearer"
                }
            },
            new string[]{}
        }
    });
});

builder.Services.AddScoped<IRegistrationService, RegistrationService>();
builder.Services.AddScoped<ITokenGeneratorService, TokenGeneratorService>();
builder.Services.AddScoped<IRefreshTokenValidatorService, RefreshTokenValidatorService>();
builder.Services.AddScoped<ITokenManagerService, TokenManagerService>();
builder.Services.AddScoped<IDatabaseSeeder, DatabaseSeeder>();

builder.Services.AddScoped<IUserService, UserService>();

var allowedCrossOriginPolicyName = "AllowedCrossOrigin";
builder.Services.AddCors(options =>
{
    options.AddPolicy(
        allowedCrossOriginPolicyName,
        policy => policy.WithOrigins(
                builder.Configuration.GetSection("AllowedCrossOrigins").Get<string[]>())
            .AllowAnyHeader()
            .AllowAnyMethod());
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    using (IServiceScope scope = app.Services.CreateScope())
    {
        IServiceProvider serviceProvider = scope.ServiceProvider;

        PathMentorAuthDbContext pathmentorAuthDbContext =
            serviceProvider.GetService<PathMentorAuthDbContext>()!;
        pathmentorAuthDbContext.Database.Migrate();
        IDatabaseSeeder databaseSeeder =
            serviceProvider.GetService<IDatabaseSeeder>()!;
        await databaseSeeder.Seed();
    }

    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.UseCors(allowedCrossOriginPolicyName);

app.Run();
