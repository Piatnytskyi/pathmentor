FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER root
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["PathMentor.Model.API/PathMentor.Model.API.csproj", "PathMentor.Model.API/"]
COPY ["PathMentor.Data/PathMentor.Data.csproj", "PathMentor.Data/"]
RUN dotnet restore "PathMentor.Model.API/PathMentor.Model.API.csproj"
COPY . .
WORKDIR "/src/PathMentor.Model.API"
RUN dotnet build "PathMentor.Model.API.csproj" -c Debug -o /app/build

FROM build AS publish
RUN dotnet publish "PathMentor.Model.API.csproj" -c Debug -o /app/publish

FROM base AS final
RUN apt-get update && apt-get install -y curl
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "PathMentor.Model.API.dll"]
