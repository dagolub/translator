# Translator

[![Deploy](https://github.com/dagolub/translator/actions/workflows/deploy.yml/badge.svg)](https://github.com/dagolub/translator/actions/workflows/deploy.yml)

![PyTest](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/dagolub/25d4bd2f53ddf0792bb916d62ac0205a/raw/translator.json)

## If you want to run over docker-compose
```
docker-compose up -d
```
and site will be access via
```
http://localhost:8080
```

## If you want run directly
```bash
python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install poetry
poetry install
python main.py
```
and site will be access via
```
http://localhost:8000
```

## To run test
```
pytest --cov --cov-report term
```

To achieve goals of challenge I am using selenium (it is my selenoid on http://selenoid.fastapi.xyz),
basically I think the best idea to use Google api for such things

As database, I choose mongodb and test credentials in env file for production you don`t need use this

In repo, you can find postman collection to test requests.

Basically if you see in GitHub actions you can find deploy to my own server.

My server available at https://translator.fastapi.xyz/docs

Login and password to get api key is admin@admin.com and password: admin