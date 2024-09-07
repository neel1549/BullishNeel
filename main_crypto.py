from flask import Flask, jsonify, request
import ccxt
import redis
import json
import os
import time
from crypto_exchange import CryptoExchange
import requests

app = Flask(__name__)

exchange_name= "binanceus"

@app.route('/generate_order_book', methods=['POST'])
def generate_order_book():

    symbol = request.json.get('symbol')

    if not symbol:
        return HTTPResponse("Please provide a symbol.", 400)

    order_book_fetcher = CryptoExchange(exchange_name, symbol)
    order_book = order_book_fetcher.generate_l1_order_book()
    result = order_book_fetcher.store_order_book(symbol, order_book)

    return jsonify({"message": f"Stored order book for {symbol} on {exchange_name}.", "query_key": result["l1_order_book_key"]})

@app.route('/query_order_book', methods=['GET'])
def query_order_book():


    symbol = request.args.get('symbol')
    timestamp = request.args.get('timestamp')

    if not symbol:
        return jsonify({"error": "Please provide symbol."}), 400

    order_book_fetcher = CryptoExchange(exchange_name, symbol)

    result = order_book_fetcher.get_order_book()
    
    return jsonify(result)

@app.route('/query_asks', methods=['GET'])
def query_asks():
    symbol = request.args.get('symbol')

    if not symbol:
        return jsonify({"error": "Please provide symbol."}), 400

    order_book_fetcher = CryptoExchange(exchange_name, symbol)
    result = order_book_fetcher.get_asks_or_bids('asks')
    return jsonify(result)

@app.route('/query_bids', methods=['GET'])
def query_bids():

    symbol = request.args.get('symbol')

    if  not symbol:
        return jsonify({"error": "Please provide symbol."}), 400

    order_book_fetcher = CryptoExchange(exchange_name, symbol)
    result = order_book_fetcher.get_asks_or_bids('bids')
    return jsonify(result)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)