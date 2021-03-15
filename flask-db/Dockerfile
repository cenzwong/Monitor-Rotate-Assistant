# docker build . --tag flask-tempdb
# docker run -p 8888:5000 flask-tempdb

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
