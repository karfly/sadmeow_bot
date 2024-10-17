FROM python:3.11.7-slim-bookworm

RUN \
    set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
    python3-pip \
    build-essential \
    curl \
    ; \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install -U pip wheel setuptools
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && rm -r /tmp/requirements.txt

COPY . /code
WORKDIR /code

CMD ["bash"]
