FROM python:3.11-slim

WORKDIR /app

COPY . ./

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/app"

COPY entry-point.sh /app/entry-point.sh
RUN chmod +x /app/entry-point.sh

ENTRYPOINT ["/app/entry-point.sh"]