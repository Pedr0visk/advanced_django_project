# Base Image
FROM python:3.8.3-alpine

ENV PATH="/scripts:${PATH}"

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY apps .
COPY bop .
COPY templates .
COPY static .
COPY manage.py .

COPY scripts /scripts
RUN chmod +x /scripts/*

ENTRYPOINT ["entrypoint.sh"]
