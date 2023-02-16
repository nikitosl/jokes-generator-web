import logging
import os
import sys

import requests
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators

logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
                    stream=sys.stdout,
                    level=logging.DEBUG)

secret_key = os.getenv("FLASK_SECRET_KEY")
logging.debug(f'Got flask_secret_key from env: {secret_key}')
model_url = os.getenv("MODEL_URL")
logging.debug(f'Got model_url from env: {model_url}')

app = Flask(__name__)
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = secret_key
# Flask-Bootstrap requires this line
Bootstrap(app)


def request_punches(setup, inspiration, num_return_sequences, temperature):
    response = requests.post(url=f'{model_url}/predict',
                             json={'setup': setup,
                                   'inspiration': inspiration,
                                   'num_return_sequences': num_return_sequences,
                                   'temperature': temperature},
                             timeout=4 * 60)
    if response.status_code == 200:
        return response.json()


class InputForm(FlaskForm):
    setup = StringField(
        'Setup',
        validators=[validators.DataRequired(), validators.length(min=5)],
        description='The beginning of your joke',
        default='Мальчик так долго плакал, что')

    inspiration = StringField(
        'Inspiration',
        description='Inspiration for punch in form of few words',
        default='море')

    punch = StringField(
        'Punch',
        description='Generated punch',
        render_kw={'readonly': True})

    mark = StringField(
        'Mark',
        description='Generated mark for pair setup + punch',
        render_kw={'readonly': True, 'data-size': 'mini'})

    submit = SubmitField('Generate')


@app.route('/', methods=('GET', 'POST'))
def index():
    form = InputForm()
    error_message = ""

    if form.validate_on_submit():
        setup = form.setup.data
        inspiration = form.inspiration.data
        inspiration = inspiration if len(inspiration) > 0 else None

        try:
            result = request_punches(setup, inspiration, num_return_sequences=1, temperature=0.9)
            if len(form.inspiration.data) == 0:
                form.inspiration.data = result[0]['inspiration']
            form.punch.data = result[0]['punch']
            form.mark.data = result[0]['mark']
        except (requests.exceptions.ConnectionError,
                requests.exceptions.InvalidSchema) as e:
            logging.error('Got error when trying to get predictions')
            logging.error(e)
            error_message = 'Sorry, model is not available now. Try again later'
            del form.punch
            del form.mark
        return render_template('index.html', form=form, error_message=error_message)

    del form.punch
    del form.mark
    return render_template('index.html', form=form, error_message=error_message)


if __name__ == '__main__':
    # Port for gcp healthcheck
    port = os.getenv("PORT")
    logging.debug(f'Got port from env: {port}')

    # # Wait model_api to start
    # wait_model_starting(model_url)
    # # Test model api
    # try:
    #     if not test_model_api(model_url):
    #         logging.warning('Check model api, it doesnt pass tests')
    # except:
    #     logging.warning('Check model api it raised error when request')

    app.run(host='0.0.0.0', port=port)
