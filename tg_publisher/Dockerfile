FROM python:3.9-slim
COPY ./make_tg_post.py /tg_posts/
COPY ./requirements.txt /tg_posts/

ENV PYTHONPATH=/tg_posts
WORKDIR /tg_posts

ARG MODEL_URL
ARG TZ
ARG TG_API_TOKEN
ARG NEWS_API_TOKEN

ENV MODEL_URL=${MODEL_URL}
ENV TZ=${TZ}
ENV TG_API_TOKEN=${TG_API_TOKEN}
ENV NEWS_API_TOKEN=${NEWS_API_TOKEN}


RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "make_tg_post.py"]