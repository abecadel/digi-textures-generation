FROM python:3.10
ENV DEBIAN_FRONTEND=noninteractive

ENV PORT 8000
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src src
COPY .env* .
CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
