FROM python:3.9-slim
COPY ./app.py /joke_gen/
COPY ./test_model_api.py /joke_gen/
COPY ./requirements.txt /joke_gen/
COPY ./static /joke_gen/static
COPY ./templates /joke_gen/templates

ENV PYTHONPATH=/joke_gen
WORKDIR /joke_gen

ARG MODEL_URL
ARG TZ
ARG FLASK_SECRET_KEY
ENV MODEL_URL=${MODEL_URL}
ENV TZ=${TZ}
ENV FLASK_SECRET_KEY=${FLASK_SECRET_KEY}

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080
CMD ["uwsgi", "--http", "0.0.0.0:8080", "--wsgi-file", "app.py", "--callable", "app"]
