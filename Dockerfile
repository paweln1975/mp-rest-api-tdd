FROM python:3.7-alpine
ENV PYTHONUNBUFFERED=1
ENV DEV_ENV=True
COPY ./requirements.txt /requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
