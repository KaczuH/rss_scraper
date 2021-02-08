# ECB currencies exchange rates app
This app scrapes European Central Bank currencies exchange rates 
from https://www.ecb.europa.eu/home/html/rss.en.html. 
It uses celerybeat to perform periodic tasks and Django Rest Framework to present the data.

## Installation
To install this project you need to clone it, 
create a `.env` file (using `.env.example` as an example) and then run:

`docker-compose up`

The super-user with credentials provided in your `.env` file will be created 
along with all available currencies. The exchange rates will be populated from a celery task.


## Rates update
The task is scheduled using celerybeat to run at 16:30 every day, 
because the ECB updates the rates at about 16:00 CET 
(source: https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html).


## Access
The django admin panel is available at http://localhost:8000/admin/.
The API documentation can be found at http://localhost:8000/v1/docs/.

To login to either one you need to provide credentials that were specified in your `.env` file.

## Django models
There are two django models that hold the data:
`Currency` and `ExchangeRateLog`. 

### Currency
Currency holds the current exchange rate information and also the variable `update` 
which when set to False will stop the currency from being updated.

Field `ecb_update` is fetched from ECB RSS feed whereas
field `last_fetched` records the time at which celery task updated the data in django database.

### ExchangeRateLog
ExchangeRateLog model is used to store the historical data about exchange rates.

## API endpoints
There are 4 API endpoints available.
`/v1/exchange_rates/current/`
`/v1/exchange_rates/current/without_pagination/`
`/v1/exchange_rates/current/{code}`
`/v1/exchange_rates/historical/?code={code}`

First two are lists with current exchange rates for various currencies. 

One is paginated, the other one is not.

Third endpoint can be used to retrieve current data about one specific currency by providing it's code (eg. USD).

Fourth endpoint is paginated and returns historical logs of exchange rates that can be filtered by a currency code.