# syntax=docker/dockerfile:1.0.0-experimental
FROM python:3.8.2-slim-buster

RUN pip install seqtolang numpy

COPY docker_entrypoint.py docker_entrypoint.py

ENTRYPOINT ["python", "docker_entrypoint.py"]
