from newsapi import NewsApiClient
import requests
import os
import telegram
import logging
import sys
import time
import json

logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
                    stream=sys.stdout,
                    level=logging.DEBUG)

# Init
model_url = 'http://genapi:8888/'
previous_news_post_time = None


def get_news(api_token):
    response = requests.get("https://newsapi.org/v2/top-headlines",
                            params={'apiKey': api_token,
                                    'language': 'ru',
                                    'country': 'ru',
                                    'page': 1,
                                    'page_size': 1})

    if response.status_code == 200:
        headline = response.json()
        if headline['status'] == 'ok':
            title = headline['articles'][0]['title']
            time = headline['articles'][0]['publishedAt']
            source = headline['articles'][0]['source']['name']
            link = headline['articles'][0]['url']
            return title, time, source, link


def make_tg_post(tg_api_token, title, punch, mark=0):
    post_text = f"""<strong>{title}</strong>\n{punch}"""

    response = requests.get(f"https://api.telegram.org/bot{tg_api_token}/sendMessage",
                            params={"chat_id": "@AIFunnyNews",
                                    "text": post_text,
                                    "parse_mode": "HTML"})
    if response.status_code == 200:
        return post_text


def wait_model_starting():
    while True:
        try:
            response = requests.get(model_url)
        except:
            pass
        else:
            if response.status_code == 200:
                return True
        time.sleep(60)


def request_punch_mark(nes):
    response = [('Не Пугачева: дочь Галкина растет копией его любимой женщины - Экспресс газета', 'илон маск', 'Как тебе такое, Илон Маск, у которого есть педпед?', '1'), ('Не Пугачева: дочь Галкина растет копией его любимой женщины - Экспресс газета', 'поздравлять', 'Поздравляю, товарищи, что я за гей, то и говна!', '1'), ('Не Пугачева: дочь Галкина растет копией его любимой женщины - Экспресс газета', 'поздравлять', 'Поздравляю с Галкина, а не на что смотреть.', '1'), ('Не Пугачева: дочь Галкина растет копией его любимой женщины - Экспресс газета', 'поздравлять', 'Поздравляю, а кто же это "забыл" от вас?', '1'), ('Не Пугачева: дочь Галкина растет копией его любимой женщины - Экспресс газета', 'поздравлять', 'Поздравляю, я твоя мать - Алексей.', '1')]
    punch_tuple = response[0]
    return punch_tuple[2], punch_tuple[3]


def request_punch_mark_t(news):
    """

    :param news:
    :return: Tuple[str, str]: punch, mark
    """
    response = requests.post(url=f'{model_url}predict',
                             json={'setup': news,
                                   'inspiration': None,
                                   'num_return_sequences': 5,
                                   'temperature': 1},
                             timeout=4 * 60)
    if response.status_code == 200:
        # Best punch -> first punch, sorted by mark and len of punch in descending order
        punches = response.json()
        logging.debug(f"Got from model: {punches}")
        return punches[0]['punch'], punches[0]['mark']


def main(news_api_token, tg_api_token):
    # Get last news
    news = get_news(news_api_token)
    if not news:
        logging.error('No news found!')
        return 0
    logging.info('Got news')
    title, time, source, link = news

    # Check last post time. If same -> post already exists
    global previous_news_post_time
    if previous_news_post_time == time:
        logging.error('Found news which already posted!')
        return 0
    logging.info('Checked news publish time is not equal to previous publish time')

    # Get punch
    punch, mark = request_punch_mark(title)
    mark = int(mark)
    logging.info('Got punch and mark for news')

    # Post news with punch to tg
    post_message = make_tg_post(tg_api_token, title, punch, mark)
    if post_message:
        logging.info(f'Successfully posted new joke: {post_message}')
        previous_news_post_time = time
    else:
        logging.error(f'Joke was not published!')


if __name__ == '__main__':
    news_api_token = os.getenv('NEWS_API_TOKEN')
    logging.debug(f'Got {news_api_token} as token for news api')
    tg_api_token = os.getenv('TG_API_TOKEN')
    logging.debug(f'Got {tg_api_token} as token for tg api')

    logging.info("Waiting model start")
    # wait_model_starting()
    logging.info("Model started")

    runs_counter = 0
    while True:
        logging.debug(f'----------- Run #{runs_counter} -----------')
        try:
            main(news_api_token, tg_api_token)
        except Exception as e:
            logging.error(f'While running main function error raised: {e}')

        time.sleep(5 * 60)  # Sleep time in seconds
        runs_counter += 1
