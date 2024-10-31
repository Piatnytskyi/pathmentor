FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER root
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG configuration=Release
WORKDIR /src
COPY ["PathMentor.Core/PathMentor.Core.csproj", "PathMentor.Core/"]
COPY ["PathMentor.Data/PathMentor.Data.csproj", "PathMentor.Data/"]
COPY ["PathMentor.Infrastructure/PathMentor.Infrastructure.csproj", "PathMentor.Infrastructure/"]
COPY ["PathMentor.Contracts/PathMentor.Contracts.csproj", "PathMentor.Contracts/"]
COPY ["PathMentor.Model.API/PathMentor.Model.API.csproj", "PathMentor.Model.API/"]
RUN dotnet restore "PathMentor.Model.API/PathMentor.Model.API.csproj"
COPY . .
WORKDIR "/src/PathMentor.Model.API"
RUN dotnet build "PathMentor.Model.API.csproj" -c $configuration -o /app/build

FROM build AS publish
ARG configuration=Release
RUN dotnet publish "PathMentor.Model.API.csproj" -c $configuration -o /app/publish

FROM base AS final
RUN apt-get update && apt-get install -y curl
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "PathMentor.Model.API.dll"]
