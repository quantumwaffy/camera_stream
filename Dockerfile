FROM ubuntu:23.10

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN set -ex \
    && apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        libhdf5-103-1 libhdf5-dev \
        libopenblas0 libopenblas-dev \
        libprotobuf32 libprotobuf-dev \
        libjpeg8 libjpeg8-dev \
        libpng16-16 libpng-dev \
        libtiff6 libtiff-dev \
        libwebp7 libwebp-dev \
        libopenjp2-7 libopenjp2-7-dev \
        libtbb12 libtbb-dev \
        libeigen3-dev libgl1 \
        tesseract-ocr tesseract-ocr-por libtesseract-dev \
        python3 python3-pip python3-dev python3-tk \
        graphviz libhdf5-dev openmpi-bin

RUN pip install poetry --root-user-action=ignore --break-system-packages

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --only main --no-root

ENV QT_X11_NO_MITSHM=1