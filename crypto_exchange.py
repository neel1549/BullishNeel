
from flask import Flask, jsonify
import ccxt
import redis
import json
import os
import time


class CryptoExchange:
    def __init__(self, exchange, symbol):

        self.exchange = self.get_exchange_instance(exchange)
        self.symbol = symbol
        self.redis_client = self.instantiate_redis()
        self.order_book_primary_key = f"{exchange}_{symbol}_l1_order_book_data"

    def instantiate_redis(self):
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = os.getenv('REDIS_PORT', 6379)
        return redis.Redis(host=redis_host, port=int(redis_port))

    def get_exchange_instance(self, exchange_name):
        if exchange_name == "gemini":
            ex = ccxt.gemini()
            ex.proxyUrl = 'https://fast-dawn-89938.herokuapp.com/'
            return ex
        else:
            raise ValueError(f"Unsupported exchange: {exchange_name}")


    def generate_l1_order_book(self):
        order_book = self.exchange.fetch_order_book(self.symbol, limit=1)
        return order_book


    def store_order_book(self, symbol, order_book):

        order_book_gen_timestamp = order_book['timestamp']
        order_book_key = f"{self.exchange.id}:{symbol}:{order_book_gen_timestamp}:l1_order_book"
        bids_key = f"{self.exchange.id}:{symbol}:{order_book_gen_timestamp}:bids"
        asks_key = f"{self.exchange.id}:{symbol}:{order_book_gen_timestamp}:asks"
        

        # Store the order book and bids and asks
        self.redis_client.set(order_book_key, json.dumps(order_book))
        self.redis_client.set(bids_key, json.dumps(order_book['bids']))
        self.redis_client.set(asks_key, json.dumps(order_book['asks']))

        return {"l1_order_book_key": order_book_key}


    def get_order_book(self):

        keys = self.redis_client.keys(f"{self.exchange.id}:{self.symbol}:*:order_book")

        if not keys:
            return {"error": "No data found for the given symbol and exchange. Please hit the /generate_order_book endpoint."}

        order_book_data = self.redis_client.get(max(keys))

        if order_book_data:
            return json.loads(order_book_data)
        else:
            return {"error": "No data found for the given symbol and exchange. Please hit the /generate_order_book endpoint."}


    def get_asks_or_bids(self, order_requests='asks'):

        # Either asks or bids
        keys = self.redis_client.keys(f"{self.exchange.id}:{symbol}:*:{order_requests}")

        if not keys:
            return {"error": "No data found for the given symbol and exchange. Please hit the /generate_order_book endpoint."}

        order_data = self.redis_client.get(max(keys))

        if order_data:
            return json.loads(order_data)
        else:
            return {"error": f"N data found for the given symbol and exchange for {order_requests}. Please hit the /generate_order_book endpoint."}



    



