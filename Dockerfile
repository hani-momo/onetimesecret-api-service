FROM python:3.11-alpine

LABEL maintainer="hani"

WORKDIR /app

ENV PYTHONNUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./secret_manager/entrypoint.sh ./
RUN chmod +x ./entrypoint.sh

COPY . .

ENTRYPOINT ["./secret_manager/entrypoint.sh"]
