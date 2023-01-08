from typing import List, Dict
from flask import Flask, request
from model_utils import T5GenerationModel
import logging
import sys
logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
                    stream=sys.stdout,
                    level=logging.DEBUG)
app = Flask(__name__)


@app.route('/')
def default_route():  # put application's code here
    logging.debug('Default route request')
    return 'Jokes generation model is ready!'


@app.route('/test_predict', methods=['POST'])
def get_test_prediction() -> List[Dict]:
    logging.debug('Test prediction function requested')
    # Works only for a single sample
    if request.method == 'POST':
        data = request.get_json()
        setup = data.get('setup')
        inspiration = data.get('inspiration', None)

        result_template = [{'setup': setup,
                            'inspiration': inspiration if inspiration else 'inspiration_template',
                            'punch': 'шаблон для панча на русском',
                            'mark': '0'}]

        return result_template


@app.route('/predict', methods=['POST'])
def get_prediction() -> List[Dict]:
    logging.debug('Prediction function requested')
    # Works only for a single sample
    if request.method == 'POST':
        data = request.get_json()

        setup = data.get('setup')
        inspiration = data.get('inspiration', None)
        num_return_sequences = int(data.get('num_return_sequences', 1))
        temperature = float(data.get('temperature', 1))

        logging.debug(f'setup={setup}; '
                      f'inspiration={inspiration}; '
                      f'num_return_sequences={num_return_sequences}; '
                      f'temperature={temperature}')
        prediction = model.inference(setup=setup,
                                     inspirations=[inspiration] if inspiration else None,
                                     num_return_sequences=num_return_sequences,
                                     temperature=temperature)
        logging.debug(f'Got prediction: {prediction}')
        prediction_dicts = [{'setup': t[0], 'inspiration': t[1], 'punch': t[2], 'mark': t[3]} for t in prediction]
        return prediction_dicts


if __name__ == '__main__':
    logging.debug('Starting downloading model')
    # model variable refers to the global variable
    model = T5GenerationModel()
    # model.load_model_from_file('model_weights/')

    model.load_model_from_hub(model_name="naltukhov/joke-generator-t5-rus-finetune",
                              model_type="flax",
                              revision="a001d2b3c44d193f489f2e3704ca13776a57a43b",
                              use_auth_token=False,
                              force_download=True)

    logging.debug('Model was successfully downloaded!')
    app.run(host='0.0.0.0', port=8888)
