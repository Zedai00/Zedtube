FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5500

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg

CMD ["python", "app.py"]


