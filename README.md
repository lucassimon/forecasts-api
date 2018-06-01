# Notificação de clima por usuário


https://github.com/jeanfinck/api-challenge/blob/master/README.md

Algumas mudanças na arquitetura e estrutura do projeto foram feitas

## Requisitos

- Virtualenv
- Python3
- Flask
- MongoDB
- Redis
- RabbitMQ?

## Iniciando o mongoDB

```shell
$ docker run --name mongo-latest -p 27017:27017 -d mongo
```

## Iniciando o redis backend (using docker)

```shell
docker run -d --name redis -p 6379:6379 redis
```

## run celery worker
```shell
celery -A celery_worker:celery worker --loglevel=DEBUG
```

## run celery beat for periodic tasks
```shell
celery -A celery_worker:celery beat --loglevel=INFO
```


## Api

### Cadastrar um usuario

Payload

```json
{
    "name": "Lucas Simon",
    "email": "lucassrod@gmail.com",
    "password": "teste123"
}
```

Request

```shell
$ http -v POST http://0.0.0.0:5000/users full_name="Lucas Simon" email="lucassrod@gmail.com" password="teste123"
```

Response

```json
{
    "data": {
        "email": "lucassrod@gmail.com",
        "full_name": "Lucas Simon",
        "id": "5b0ee53cfb5d1b517e7b032a"
    },
    "message": "Usuário criado(a).",
    "resource": "Users",
    "status": 200
}
```

## Buscar um usuário

Request

```shell
$ http -v GET http://0.0.0.0:5000/users/5b0ee53cfb5d1b517e7b032a
```


Response

```json
{
    "data": {
        "email": "lucassrod@gmail.com",
        "id": "5b0eead1fb5d1b62d3df17bf",
        "name": "Lucas Simon"
    },
    "message": "Usuário retornado(a).",
    "resource": "Users",
    "status": 200
}
```

## Importar dados dos usuarios:

É necessário ter um arquivo `import_users.csv` no diretório `/tmp`

```
Usuario 1,user1@imported.com,teste123
Usuario 2,user2@imported.com,teste123
Usuario 3,user3@imported.com,teste123
Usuario 4,user4@imported.com,teste123
Usuario 5,user5@imported.com,teste123
```

Request

```shell
$ http -v GET http://0.0.0.0:5000/users/import/data
```

Response

```json
{
    "data": {
        "links": "http://localhost:5000/users/import/status/3ff6eb56-bccb-4f18-ae12-431115bbaeea",
        "task": "3ff6eb56-bccb-4f18-ae12-431115bbaeea"
    },
    "message": "Usuário retornado(a).",
    "resource": "Users",
    "status": 200
}
```

## Status do import do usuário:

Request

```shell
$ http -v GET http://0.0.0.0:5000/users/import/status/3ff6eb56-bccb-4f18-ae12-431115bbaeea
```

Response

```json
{
    "data": {
        "errors": [
            {
                "error": "Tried to save duplicate unique keys (E11000 duplicate key error collection: forecast.users index: email_1 dup key: { : \"user1@imported.com\" })",
                "line": 0
            },
            {
                "error": "Tried to save duplicate unique keys (E11000 duplicate key error collection: forecast.users index: email_1 dup key: { : \"user2@imported.com\" })",
                "line": 1
            },
            {
                "error": "Tried to save duplicate unique keys (E11000 duplicate key error collection: forecast.users index: email_1 dup key: { : \"user3@imported.com\" })",
                "line": 2
            },
            {
                "error": "Tried to save duplicate unique keys (E11000 duplicate key error collection: forecast.users index: email_1 dup key: { : \"user4@imported.com\" })",
                "line": 3
            },
            {
                "error": "Tried to save duplicate unique keys (E11000 duplicate key error collection: forecast.users index: email_1 dup key: { : \"user5@imported.com\" })",
                "line": 4
            }
        ],
        "imported": 0,
        "state": "SUCCESS",
        "status": "Task completed!",
        "total": 5
    },
    "message": "Usuário retornado(a).",
    "resource": "Users",
    "status": 200
}
```

## Exportar dados dos usuários:

Esse endpoint precisa que o celery worker esteja executando.

Request

```shell
$ http -v GET http://0.0.0.0:5000/users/export/data
```

Response

```json
{
    "data": {
        "links": "http://localhost:5000/users/export/download/897d02c8-96e6-4b3f-9e08-59b95cd6d25e",
        "task": "897d02c8-96e6-4b3f-9e08-59b95cd6d25e"
    },
    "message": "Usuário retornado(a).",
    "resource": "Users",
    "status": 200
}
```


## Status do download do export dos usuários:

Esse endpoint precisa que o celery worker esteja executando.

Request

```shell
$ http -v GET http://0.0.0.0:5000/users/export/download/eb24af5b-aad3-4c39-82cf-2b3a1544b5f0
```

Response

```json
{
    "data": {
        "filename": "897d02c8-96e6-4b3f-9e08-59b95cd6d25e.csv",
        "links": "CDN url or static url from flask",
        "message": "Verifique a pasta /tmp"
    },
    "message": "Usuário retornado(a).",
    "resource": "Users",
    "status": 200
}
```

## Criar configurações do clima para usuário

Payload:

```json
{
    "address": "London, UK",
    "period": {
        "start": "08:00",
        "end": "19:00"
    },
    "days": {
        "sunday": true,
        "monday": true,
        "tuesday": true,
        "wednesday": true,
        "thursday": true,
        "friday": true,
        "saturday": true
    },
    "notification": "07:00"
}
```

Request

Não se esquecer dos dados do payload. Eu utilizei outro client para fazer essa requisição chamado INSOMNIA. O POSTMAN também pode ser utilizado

```shell

http -v POST http://0.0.0.0:5000/users/5b0eead1fb5d1b62d3df17bf/forecasts
```

Response

```json
{
    "data": {
        "address": "London, UK",
        "days": {
            "friday": true,
            "monday": true,
            "saturday": true,
            "sunday": true,
            "thursday": true,
            "tuesday": true,
            "wednesday": true
        },
        "id": "5b0f07dafb5d1b058f5d8e26",
        "notification": "07:00",
        "period": {
            "end": "19:00",
            "start": "08:00"
        },
        "user_id": "5b0eead1fb5d1b62d3df17bf"
    },
    "message": "Configurações do clima criado(a).",
    "resource": "Forecasts Settings",
    "status": 200
}
```


## Testes

Para executar os testes, o virtualenv deve estar ativo, faça:

```shell
$ pip install -e .
```

Em seguida

```shell
$ pytest

collected 19 items

tests/forecasts/test_utils.py ..
tests/modules/openweathermap/test_openweather.py .
tests/users/test_models.py ...........
tests/users/test_resources.py .....
```

### Problemas com o pytest

Eu não etendi bem, mas tive um problema com a fixture do `test_client` e a do `celery_app`. Quando fazia os testes em cima das tasks com o `celery_app`, os outros testes davam erro de sobrescrita de urls do `flask`.

Como não consegui diagnosticar muito bem e ter uma solução não implementei testes em cima das tasks, priorizando os testes de aplicação.

## Desafio

- Crie serviços para gerenciar o cadastro de usuários e de seus respectivos dados para monitoramento.

> Feito os endpoints de forma mais simples.

- Implemente a integração com ao menos um provedor de informações meteorológicas.

> Feito o desenvolvimento da api [OpenWeatherMap Forecasts](https://openweathermap.org/forecast5). Pois ela traz a previsão de eventos futuros e os dados são atualizados a cada 03 horas

- Crie uma interface entre o(s) serviço(s) meteorológico(s) e a classe onde será implementada a lógica. A substituição ou adição de um novo serviço meteorológico não deve causar refatoração do código implementado.

> Fiz a implementação em `/modules/gw.py`


- Implementei a lógica para monitorar e notificar todos os usuários que devem ser avisados para não esquecerem seus guarda-chuvas.

> Realizei a lógica parcial deste problema utilizando uma solução com celery e tarefas periodicas a cada 30 minutos. Nesta lógica existem alguns itens a serem feitos como flag de notificação para não enviar mais de uma vez. A utilização do RabbitMQ para receber a mensagem e posteriormente consumir esse dado da fila notificando o usuário por e-mail/sms ou app android. Para consumidor é interessante utilizar o Node.JS por ser assincrono nativo. Se o processamento fosse muito pesado partiria para uma solução em GoLang

- Crie um método assíncrono para importar novos usuários a partir de um arquivo CSV (levar em consideração que o arquivo já exista na pasta /tmp por exemplo)

> Implementei a logica em `/users/tasks.py`.

- Crie um método assíncrono para exportar todos os usuários da base de dados em um arquivo CSV (o arquivo pode ser salvo na pasta /tmp)

> Implementei a logica em `/users/tasks.py`. Como é um servidor Rest seria interessante colocar o arquivo gerado em um CDN como o S3 utilizando Boto do proprio python e enviar o link para download na resposta JSON conforme descrito no endpoint correspondente.