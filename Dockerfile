FROM python:3.7-slim-buster

RUN DEBIAN_FRONTEND=noninteractive apt update \
 && DEBIAN_FRONTEND=noninteractive apt install \
    -y --no-install-recommends vlc

WORKDIR /app
COPY requirements.txt   .
RUN pip3 install -r requirements.txt
COPY .  .

ENTRYPOINT [ "/app/start.sh" ]