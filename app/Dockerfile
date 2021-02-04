# Base Image
FROM python:3.8.3-alpine

ENV PATH="/scripts:${PATH}"

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
  && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev dcron \
  && rm -rf /var/cache/apk/*

RUN mkdir -p /var/log/cron && mkdir -m 0644 -p /var/spool/cron/crontabs \
    && touch /var/log/cron/cron.log && mkdir -m 0644 -p /etc/cron.d

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY ./apps ./apps
COPY ./bop ./bop
COPY ./static ./static
COPY ./templates ./templates
COPY ./manage.py .

COPY ./scripts /scripts
RUN chmod +x /scripts/*

ENTRYPOINT ["entrypoint.sh"]
