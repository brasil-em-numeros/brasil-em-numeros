FROM python:latest

# RUN apk update
# RUN apk add make automake gcc g++

RUN mkdir dashboard

COPY ./dashboard ./dashboard
COPY ./requirements.txt .
COPY ./dash.py .

RUN pip3 install -r requirements.txt

EXPOSE 5000

# CMD ["bash"]
CMD ["python3", "./dash.py"]