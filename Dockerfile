FROM python:3-alpine

RUN mkdir /app
ADD walkoff-webhook.py /app/run.py

ADD requirements.txt /app
WORKDIR /app

RUN pip3 install -r requirements.txt 

EXPOSE 9091 

CMD ["python3", "run.py"]
