FROM python:3.9-slim
COPY ./app.py /joke_gen/
COPY ./test_model_api.py /joke_gen/
COPY ./requirements.txt /joke_gen/

ENV PYTHONPATH=/joke_gen
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /joke_gen

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000

CMD ["python", "app.py"]