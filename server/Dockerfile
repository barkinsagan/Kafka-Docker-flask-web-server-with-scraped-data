FROM python:3.11

ENV PYTHONUNBUFFERED=1
WORKDIR /app


RUN pip install flask 
RUN pip install requests

COPY . /app/

CMD ["python", "app.py"]
