import requests


def test_model_api(url):
    print(f'Get response to {url}')
    get_response = requests.get(url)
    print(f'Response code: {get_response.status_code}; response content: {get_response.text}')

    post_url = url + 'test_predict'
    print(f'Post response to {post_url}')

    post_response = requests.post(post_url, json={'setup': 'начало шутки',
                                                  'inspiration': 'вдохновение',
                                                  'num_return_sequences': 'num_return_sequences',
                                                  'temperature': 'temperature'})
    print(f'Response code: {post_response.status_code}; response content: {post_response.json()}')

    return (post_response.status_code == 200) & (get_response.status_code == 200)


if __name__ == '__main__':
    test_model_api('http://127.0.0.1:8888/')