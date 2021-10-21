FROM python:3.9-alpine as bigimage

COPY requirements.txt /

RUN apk add --update python3 py-pip python3-dev make cmake gcc g++ openssl-dev build-base
RUN pip wheel --wheel-dir=/tmp/wheels -r /requirements.txt



FROM python:3.9-alpine as smallimage

COPY --from=bigimage /tmp/wheels /tmp/wheels
COPY requirements.txt /

RUN pip install --no-index --find-links=/tmp/wheels -r /requirements.txt
RUN rm -rf /tmp/*

COPY src/ /app
WORKDIR /app

CMD ["python", "./recv_async.py"]

#docker PAT f23d19ec-e26e-4e1f-91fd-5da7eac3ff21