FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get -y install build-essential\
    python3-dev \
    libpq-dev

# Install Python dependencies
WORKDIR /tmp
COPY ["requirements.txt", "./"]
RUN pip install --upgrade pip
RUN pip install --ignore-installed --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /tmp

WORKDIR /app

COPY mastermind mastermind

CMD ["gunicorn", "--preload", "--bind=0.0.0.0:5000", "--workers=1", "--threads=1", "-t 150", "--worker-class=uvicorn.workers.UvicornWorker", "mastermind.entrypoints.fastapi:app"]
