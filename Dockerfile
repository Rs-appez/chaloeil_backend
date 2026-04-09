FROM python:3.13-slim

ENV TZ="Europe/Brussels"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir -p /code

WORKDIR /code

COPY pyproject.toml uv.lock /code/
RUN uv sync --frozen --no-dev --no-install-project

COPY . /code
RUN uv sync --frozen --no-dev

WORKDIR /code/chaloeil_backend

ENV DATABASE_URL ""
ENV SECRET_KEY "non-secret-key-for-building-purposes"
RUN uv run python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "../runserver.sh"]
