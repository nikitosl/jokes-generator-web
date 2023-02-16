FROM python:3.9-slim
COPY ./make_tg_post.py /tg_posts/
COPY ./requirements.txt /tg_posts/

ENV PYTHONPATH=/tg_posts
WORKDIR /tg_posts

ARG MODEL_URL
ARG TZ
ARG TG_API_TOKEN
ARG NEWS_API_TOKEN

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "make_tg_post.py"]