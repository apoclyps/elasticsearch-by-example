FROM python:3.9.7-alpine

RUN apk update && apk add build-base libffi-dev linux-headers gcc musl-dev openssl-dev cargo

# skip the rust installation when installing cryptography
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# do not cache pipenv dependencies
ENV PIP_NO_CACHE_DIR=false

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

WORKDIR /usr/src/app

ENV FLASK_APP=web:app
ENV PYTHONPATH=.

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "web:app"]
