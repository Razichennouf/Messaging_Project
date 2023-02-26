FROM python:3.8-alpine

MAINTAINER TEST "test.prompt@tek-up.de" # Change the name and email address
LABEL description="Simple flask messaging app"
LABEL version="1.0"
LABEL name="flask_web-app"


WORKDIR /website

COPY .  /website
RUN apk update && apk add python3  && pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 5000
#RUN pip install flask pytest flake8  # This downloads all the dependencies
#RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
