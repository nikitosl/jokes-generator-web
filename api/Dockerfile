FROM python:3.9-slim
COPY ./app.py /joke_gen/
COPY ./model_utils.py /joke_gen/
COPY ./requirements.txt /joke_gen/

ENV PYTHONPATH=/joke_gen

ARG MODEL_NAME
ARG MODEL_REVISION
ARG TZ
ARG PORT
ENV MODEL_NAME=${MODEL_NAME}
ENV MODEL_REVISION=${MODEL_REVISION}
ENV TZ=${TZ}
ENV PORT=${PORT}

WORKDIR /joke_gen

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE ${PORT}
CMD ["python", "app.py"]