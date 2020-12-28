FROM python:3.8-slim-buster
WORKDIR /src
ENV PYTHONPATH "${PYTHONPATH}:/src/"
ENV PATH "/src/scripts:${PATH}"
COPY . /src
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install
RUN chmod +x /src/scripts/*
ENTRYPOINT ["docker-entrypoint.sh"]