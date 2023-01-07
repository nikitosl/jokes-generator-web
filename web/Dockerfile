FROM python:3.9-slim
COPY ./app.py /joke_gen/
COPY ./test_model_api.py /joke_gen/
COPY ./requirements.txt /joke_gen/
COPY ./static /joke_gen/static
COPY ./templates /joke_gen/templates

ENV PYTHONPATH=/joke_gen
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /joke_gen

RUN apt-get update && apt-get -y install pkg-config cmake
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 5555

CMD ["python", "app.py"]