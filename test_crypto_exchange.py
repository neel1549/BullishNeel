import unittest
from unittest.mock import patch, MagicMock
from testcontainers.redis import RedisContainer
import redis
import ccxt
import json
from crypto_exchange import CryptoExchange 

class CryptoExchangeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls.redis_container = RedisContainer()
        cls.redis_container.start()
        cls.redis_host = cls.redis_container.get_container_host_ip()
        cls.redis_port = cls.redis_container.get_exposed_port(6379)

    @classmethod
    def tearDownClass(cls):
        cls.redis_container.stop()

    def setUp(self):
        self.redis_client = redis.Redis(host=self.redis_host, port=self.redis_port, db=0)
        self.mock_exchange = patch('ccxt.binance').start()

        self.order_book = CryptoExchange(exchange='binance',symbol="BTC/USDT")
        self.order_book.redis_client = self.redis_client


    def test_get_order_book(self):
        
        # Mock the order book data
        mock_order_book = {
            'timestamp': 1234567890,
            'bids': [[40000.0, 2.5]],
            'asks': [[41000.0, 1.2]],
        }

        # Store mock data in Redis manually
        key = f"binance:BTC/USDT:*:order_book"
        self.redis_client.set(key, json.dumps(mock_order_book))

        retrieved_order_book = self.order_book.get_order_book()

        print(retrieved_order_book)

        # Validate with mock data.
        self.assertEqual(retrieved_order_book['bids'], [[40000.0, 2.5]])
        self.assertEqual(retrieved_order_book['asks'], [[41000.0, 1.2]])


if __name__ == '__main__':
    unittest.main()