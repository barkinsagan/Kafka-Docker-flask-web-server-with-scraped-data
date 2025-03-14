FROM python:3.11


WORKDIR /app


RUN pip install confluent-kafka
RUN pip install requests

COPY . /app/

CMD ["python","-u", "./consume.py"]
