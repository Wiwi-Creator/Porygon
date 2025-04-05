FROM apache/airflow:2.10.2

ARG AIRFLOW_VERSION=2.10.2

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends lftp jq curl unzip \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /

# Install Package
USER airflow
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
