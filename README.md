# Jokes-generator-web
It is service build on top of two independent microservices: **api** and **web**. You can find details about them below.  
**Web** service sends requests to **api** service using http protocol to get prediction from model.    
Prediction in this task is text2text generation. Based on setup (and inspiration) model generates punch.  
More about model training and finetuning you can find here: 

Model training repo: https://github.com/nikitosl/jokes-generator  
Model weights: https://huggingface.co/naltukhov/joke-generator-rus-t5  
Train dataset preprocessing repo: https://github.com/nikitosl/jokes-generator-dataset  

## Api

Micro-service for hosting NLP generative model (T5). Uses Flask for model hosting.  
Model weights download from huggingface model repo when container start. It takes time.

Service listen 8888 port and gets next params as input from post request:
- _setup_ (required) - the beginning of joke you want to get punch for.
- _inspiration_ (optional, default=None) - inspiration for punch.
- _num_return_sequences_ (optional, default=1) - number of punches to generate.
- _temperature_ (optional, default=1) - model param which set randomness during generation.

## Web
Simple web-form on Flask to work with model.  
User fill in setup and inspiration (optional) and gets generated punch with mark.

# Run 
Create .env file in project root folder with next variables:  
- TG_API_TK=`<api token for telegram bot>`
- NEWS_API_TK=`<api token for newsapi>`
- TZ=`<current time zone>`
Service runs using docker-compose with command `bash deploy.sh`.  
For details check _docker-compose.yml_.
