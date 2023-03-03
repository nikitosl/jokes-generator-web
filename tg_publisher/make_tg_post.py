import logging
import os
import sys
import time

import requests

logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
                    stream=sys.stdout,
                    level=logging.DEBUG)

previous_news_post_time = None

def wait_model_starting(model_url):
    while True:
        try:
            response = requests.get(model_url)
        except:
            pass
        else:
            if response.status_code == 200:
                return True
        time.sleep(60)


def get_news(api_token):
    response = requests.get(
        "https://newsapi.org/v2/everything",
        params={'apiKey': api_token,
                'language': 'ru',
                'sortBy': 'publishedAt',
                'page': 1,
                'page_size': 1,
                'domains': 'rbc.ru,Kommersant.ru,Cnews.ru,Forklog.com,3dnews.ru,Moslenta.ru,Kinoafisha.info'})

    if response.status_code == 200:
        headline = response.json()
        if headline['status'] == 'ok':
            title = headline['articles'][0]['title']
            time = headline['articles'][0]['publishedAt']
            source = headline['articles'][0]['source']['name']
            link = headline['articles'][0]['url']
            return title, time, source, link


def request_punch_mark(news, model_url, model_num_jokes_for_generation, model_temperature):
    """

    :param news:
    :return: Tuple[str, str]: punch, mark
    """
    response = requests.post(url=f'{model_url}/predict',
                             json={'setup': news,
                                   'inspiration': None,
                                   'num_return_sequences': model_num_jokes_for_generation,
                                   'temperature': model_temperature},
                             timeout=20 * 60)
    if response.status_code == 200:
        # Best punch -> first punch, sorted by mark and len of punch in descending order
        punches = response.json()
        logging.debug(f"Got from model: {punches}")
        return punches[0]['punch'], punches[0]['mark']


def make_tg_post(tg_api_token, title, punch, mark=0.0):
    post_text = f"""<strong>{title}</strong>\n{punch}"""

    response = requests.get(f"https://api.telegram.org/bot{tg_api_token}/sendMessage",
                            params={"chat_id": "@AIFunnyNews",
                                    "text": post_text,
                                    "parse_mode": "HTML"})
    if response.status_code == 200:
        return post_text


# def request_punch_mark_test(news):
#     response = [('Не Пугачева: дочь Галкина растет копией его любимой женщины - Экспресс газета', 'илон маск', 'Как тебе такое, Илон Маск, у которого есть педпед?', '1'), ('Не Пугачева: дочь Галкина растет копией его любимой женщины - Экспресс газета', 'поздравлять', 'Поздравляю, товарищи, что я за гей, то и говна!', '1'), ('Не Пугачева: дочь Галкина растет копией его любимой женщины - Экспресс газета', 'поздравлять', 'Поздравляю с Галкина, а не на что смотреть.', '1'), ('Не Пугачева: дочь Галкина растет копией его любимой женщины - Экспресс газета', 'поздравлять', 'Поздравляю, а кто же это "забыл" от вас?', '1'), ('Не Пугачева: дочь Галкина растет копией его любимой женщины - Экспресс газета', 'поздравлять', 'Поздравляю, я твоя мать - Алексей.', '1')]
#     punch_tuple = response[0]
#     return punch_tuple[2], punch_tuple[3]


def main(news_api_token, tg_api_token,
         model_url,
         model_num_jokes_for_generation,
         model_temperature):
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
    punch, mark = request_punch_mark(
        title,
        model_url,
        model_num_jokes_for_generation,
        model_temperature)

    mark = float(mark)
    logging.info('Got punch and mark for news')

    # Post news with punch to tg_publisher
    post_message = make_tg_post(tg_api_token, title, punch, mark)
    if post_message:
        logging.info(f'Successfully posted new joke: {post_message}')
        previous_news_post_time = time
    else:
        logging.error(f'Joke was not published!')


if __name__ == '__main__':
    news_api_token = os.getenv('NEWS_API_TOKEN')
    logging.debug(f'Got news_api_token from env: {news_api_token}')
    tg_api_token = os.getenv('TG_API_TOKEN')
    logging.debug(f'Got tg_api_token from env: {tg_api_token}')
    model_url = os.getenv("MODEL_URL")
    logging.debug(f'Got model_url from env: {model_url}')
    model_num_jokes_for_generation = os.environ.get("MODEL_NUM_JOKES_FOR_GENERATION", 5)
    logging.debug(f'model_num_jokes_for_generation: {model_num_jokes_for_generation}')
    model_temperature = os.environ.get("MODEL_TEMPERATURE", 1)
    logging.debug(f'model_temperature: {model_temperature}')

    # logging.info("Waiting model start")
    # wait_model_starting(model_url)
    # logging.info("Model started")

    # current_hour = datetime.datetime.now().hour
    # if (current_hour < 9) or (current_hour > 23):
    #     logging.info('Sleeping...')
    #     sys.exit(0)

    try:
        main(news_api_token, tg_api_token, model_url, model_num_jokes_for_generation, model_temperature)
    except Exception as e:
        logging.error(f'While running main function error raised: {e}')
        sys.exit(1)
    sys.exit(0)
