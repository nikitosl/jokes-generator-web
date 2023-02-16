FROM python:3.9-slim
COPY ./app.py /joke_gen/
COPY ./model_utils.py /joke_gen/
COPY ./requirements.txt /joke_gen/

ENV PYTHONPATH=/joke_gen

ARG MODEL_NAME
ARG MODEL_REVISION
ARG TZ

WORKDIR /joke_gen

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8888

CMD ["python", "app.py"]