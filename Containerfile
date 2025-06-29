ARG IMAGETAG=python:3.13.5-alpine3.22
FROM ${IMAGETAG}

WORKDIR /tmp/can-i-park

COPY pyproject.toml pyproject.toml
COPY src src

RUN pip install .

RUN adduser -S can-i-park
USER can-i-park

WORKDIR /

ENTRYPOINT [ "can-i-park" ]
