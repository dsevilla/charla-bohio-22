FROM python:3.7-slim

MAINTAINER Your Name "youremail@domain.tld"

COPY . /bohioControls

WORKDIR /bohioControls

RUN pip3 install -r requirements.txt

ENV FLASK_APP="app/app.py"
ENV FLASK_ENV="development"

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0" ]
