
ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install kaggle
RUN apt-get update && apt-get install -y unzip

FROM base AS publish
WORKDIR /app
COPY ["pathmentor_core", "pathmentor_core"]
COPY ["pathmentor_infrastructure", "pathmentor_infrastructure"]
COPY ["pathmentor_usecases", "pathmentor_usecases"]
COPY ["pathmentor_dataset_cli", "pathmentor_dataset_cli"]
RUN python -m pip install -r pathmentor_dataset_cli/requirements.txt

FROM publish AS etl
WORKDIR /app
COPY --from=publish /app .

ENTRYPOINT kaggle datasets download -d kaggle/kaggle-survey-2018 -p pathmentor_dataset_cli/bin && \
    unzip pathmentor_dataset_cli/bin/kaggle-survey-2018.zip -d pathmentor_dataset_cli/bin && \
    rm pathmentor_dataset_cli/bin/kaggle-survey-2018.zip && \
    kaggle competitions download -c kaggle-survey-2020 -p pathmentor_dataset_cli/bin && \
    unzip pathmentor_dataset_cli/bin/kaggle-survey-2020.zip -d pathmentor_dataset_cli/bin && \
    rm pathmentor_dataset_cli/bin/kaggle-survey-2020.zip && \
    kaggle competitions download -c kaggle-survey-2021 -p pathmentor_dataset_cli/bin && \
    unzip pathmentor_dataset_cli/bin/kaggle-survey-2021.zip -d pathmentor_dataset_cli/bin && \
    rm pathmentor_dataset_cli/bin/kaggle-survey-2021.zip && \
    kaggle competitions download -c kaggle-survey-2022 -p pathmentor_dataset_cli/bin && \
    unzip pathmentor_dataset_cli/bin/kaggle-survey-2022.zip -d pathmentor_dataset_cli/bin && \
    rm pathmentor_dataset_cli/bin/kaggle-survey-2022.zip && \
    python -m pathmentor_dataset_cli build pathmentor_dataset_cli/bin/built_database.csv && \
    python -m pathmentor_dataset_cli prepare pathmentor_dataset_cli/bin/built_database.csv pathmentor_dataset_cli/bin/prepared_database.csv && \
    python -m pathmentor_dataset_cli normalize pathmentor_dataset_cli/bin/prepared_database.csv
