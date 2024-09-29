FROM duffn/python-poetry:3.12-slim


COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev


RUN sh resources/download-models.sh


CMD ["python", "-m", "wiki_helper"]