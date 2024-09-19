
ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG configuration=Release
WORKDIR /src
COPY ["PathMentor.Core/PathMentor.Core.csproj", "PathMentor.Core/"]
COPY ["PathMentor.Data/PathMentor.Data.csproj", "PathMentor.Data/"]
COPY ["PathMentor.Infrastructure/PathMentor.Infrastructure.csproj", "PathMentor.Infrastructure/"]
RUN dotnet restore "PathMentor.Infrastructure/PathMentor.Infrastructure.csproj"
COPY . .
WORKDIR "/src/PathMentor.Infrastructure"
RUN dotnet build "PathMentor.Infrastructure.csproj" -c $configuration -o /app/build

FROM build AS publish
ARG configuration=Release
RUN dotnet publish "PathMentor.Infrastructure.csproj" -c $configuration -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .

RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "pathmentor_dataset_cli/__main__.py"]
