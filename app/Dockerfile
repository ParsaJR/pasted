FROM python:3.14-slim

## Installing uv
COPY --from=ghcr.io/astral-sh/uv:0.11.15 /uv /uvx /bin/

WORKDIR /app


## Uv's dependency system
COPY pyproject.toml uv.lock ./

# System dependencies for psycopg2 package. Such a weird design by the author.
# I need to to everything in one overlay so the image size will be more optimal..
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && uv sync --frozen --no-dev \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

CMD ["uv", "run", "fastapi", "run", "/app/main.py", "--port", "80"]
