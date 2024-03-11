FROM python:3.10

COPY src/ /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install -r gunicorn

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
