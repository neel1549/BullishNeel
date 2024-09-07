#### Bullish Take Home

## Summary:
Design a solution that queries a crypto exchange, downloads all their data, and stores it in a database. I will be dividing this solution into the steps above + setting up the infrastructure with docker containers. I will be using the CCXT library that provides support for Python. I will be defaulting to the Binance Exchange and designing a flask server around the consumption.


# Spin up Server:
` docker-compose up --build -d `

# Run Unit Tests:
` python test_crypto_exchange.py `


## Tasks:

- Setup Docker Container Infrastructure, with a Flask Server and a Redis DB

- Write Python Class that interacts with Binance using CCXT 

- Create a unique Primary Key and Storage Schema for the data in Redis

- Write a handler within the Python Class that retrieves either the entire order book, just the bids or just the asks

- Write the ingest and retrieve endpoints depending on symbol

- Write the unit tests with Python test Containers

There are 4 endpoints generate_order_book, query_order_book, query_asks, query_bids. All endpoints take a "symbol" parameter and will reject if a symbol's order book hasn't been generated










