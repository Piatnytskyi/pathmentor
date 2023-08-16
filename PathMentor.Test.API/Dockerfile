#See https://aka.ms/containerfastmode to understand how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["PathMentor.Test.API/PathMentor.Test.API.csproj", "PathMentor.Test.API/"]
COPY ["PathMentor.Infrastructure/PathMentor.Infrastructure.csproj", "PathMentor.Infrastructure/"]
COPY ["PathMentor.Core/PathMentor.Core.csproj", "PathMentor.Core/"]
COPY ["PathMentor.Data/PathMentor.Data.csproj", "PathMentor.Data/"]
RUN dotnet restore "PathMentor.Test.API/PathMentor.Test.API.csproj"
COPY . .
WORKDIR "/src/PathMentor.Test.API"
RUN dotnet build "PathMentor.Test.API.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "PathMentor.Test.API.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "PathMentor.Test.API.dll"]