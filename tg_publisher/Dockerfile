FROM python:3.9-slim
COPY ./make_tg_post.py /tg_posts/
COPY ./requirements.txt /tg_posts/

ENV PYTHONPATH=/tg_posts
WORKDIR /tg_posts

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "make_tg_post.py"]