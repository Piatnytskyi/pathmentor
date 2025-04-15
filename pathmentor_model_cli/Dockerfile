
FROM tensorflow/tensorflow:latest AS base

FROM base AS publish
WORKDIR /app
COPY ["pathmentor_core", "pathmentor_core"]
COPY ["pathmentor_infrastructure", "pathmentor_infrastructure"]
COPY ["pathmentor_usecases", "pathmentor_usecases"]
COPY ["pathmentor_model_cli", "pathmentor_model_cli"]
RUN python -m pip install -r pathmentor_model_cli/requirements.txt

FROM publish AS train
WORKDIR /app
COPY --from=publish /app .

ENTRYPOINT python -m pathmentor_model_cli stage && \
    python -m pathmentor_model_cli train
