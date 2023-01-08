FROM python:3.9

COPY ./app.py /joke_gen/
COPY ./model_utils.py /joke_gen/
COPY ./requirements.txt /joke_gen/
COPY ./model_weights_v2 /joke_gen/model_weights

ENV PYTHONPATH=/joke_gen
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /joke_gen

RUN apt-get update && apt-get -y install pkg-config cmake curl
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8888