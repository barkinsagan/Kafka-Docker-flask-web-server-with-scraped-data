FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN apt-get update -y
RUN apt-get install -y iputils-ping

COPY . /app/

CMD ["python","-u" ,"./scrape.py"]
