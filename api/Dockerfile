FROM python:3.9-slim

COPY ./app.py /joke_gen/
COPY ./model_utils.py /joke_gen/
COPY ./requirements.txt /joke_gen/
COPY ./model_weights_v2 /joke_gen/model_weights

ENV PYTHONPATH=/joke_gen
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /joke_gen

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8888

CMD ["python", "app.py"]