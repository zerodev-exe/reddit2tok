# syntax=docker/dockerfile:1

FROM python:3.12-alpine3.19

# Install dependencies
RUN apk add --no-cache ffmpeg
RUN apk add --no-cache git
RUN apk add --no-cache curl

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip3 install -r requirements.txt

COPY *.py /app/

CMD [ "python3", "main.py"]

