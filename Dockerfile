FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /tasktracez-backend

COPY requirements.txt /tasktracez-backend/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /tasktracez-backend/