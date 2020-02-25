FROM python:latest

# RUN apk update
# RUN apk add make automake gcc g++

RUN mkdir app

COPY ./app.py ./app
COPY ./requirements.txt .
COPY ./data.csv ./app

RUN pip3 install -r requirements.txt

EXPOSE 8050

CMD ["python3", "./app/app.py"]