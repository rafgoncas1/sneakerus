FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

ARG port=8000
EXPOSE ${port}
ENV DEFAULT_PORT=${port}

ARG email=superuser@sneakerus.com
ENV DJANGO_SUPERUSER_EMAIL=${email}

ARG password=superuser
ENV DJANGO_SUPERUSER_PASSWORD=${password}

RUN python3 ./manage.py migrate

RUN python3 ./manage.py populate

RUN python3 ./manage.py createsuperuser --noinput

ENTRYPOINT python3 ./manage.py runserver 0:${DEFAULT_PORT}