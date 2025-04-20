FROM python:3.11-slim

WORKDIR /app

COPY . ./

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.3
RUN poetry install

ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV GOOGLE_SDK_PYTHON_LOGGING_SCOPE=google
ENV GOOGLE_SDK_PYTHON_LOGGING_SCOPE=google.cloud.library_v1

COPY entry-point.sh /app/entry-point.sh
RUN chmod +x /app/entry-point.sh

ENTRYPOINT ["/app/entry-point.sh"]