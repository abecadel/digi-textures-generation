FROM python:3.9
ENV DEBIAN_FRONTEND=noninteractive

ENV PORT 8000
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY digi_stylist digi_stylist
COPY .env* .
CMD gunicorn digi_stylist.api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
