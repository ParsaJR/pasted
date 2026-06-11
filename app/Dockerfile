FROM python:3.14-slim

WORKDIR /app


COPY ./requirements.txt /app/requirements.txt

# System dependencies for psycopg2 package. Such a weird design by the author.
# I need to to everything in one overlay so the image size will be more optimal..
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

CMD ["fastapi", "run", "/app/main.py", "--port", "80"]
