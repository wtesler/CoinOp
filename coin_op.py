__author__ = 'Will Tesler'

# Firebase Config
config = {
    "apiKey": "AAPI_KEY",
    "authDomain": "mydomain.firebaseapp.com",
    "databaseURL": "https://myurl.firebaseio.com",
    "storageBucket": "tesler.will.coinop",
    "serviceAccount": "firebase-service-account.json"
}

COIN_LIMIT = "10"

from datetime import datetime
import json
import pyrebase
from coinmarketcap import Market


def run(event, context):
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    market = Market()

    data = {}
    timestamp = datetime.utcnow().strftime("%Y %m %d %H %M %S")
    uuid = db.generate_key()

    key_timestamp = "timestamps"
    key_total_24h_volume_usd = "total_24h_volume_usd"
    key_total_market_cap_usd = "total_market_cap_usd"

    global_stats = json.loads(market.stats())

    setGlobalData(key_timestamp, uuid, timestamp, data)
    setGlobalData(key_total_24h_volume_usd, uuid, global_stats[key_total_24h_volume_usd], data)
    setGlobalData(key_total_market_cap_usd, uuid, global_stats[key_total_market_cap_usd], data)

    coin_stats = json.loads(market.ticker("?limit=" + COIN_LIMIT))

    key_price_usd = "price_usd"
    key_percent_change_1h = "percent_change_1h"
    key_percent_change_24h = "percent_change_24h"
    key_percent_change_7d = "percent_change_7d"
    key_24h_volume_usd = "24h_volume_usd"
    key_market_cap_usd = "market_cap_usd"

    for coin in coin_stats:
        coin_id = coin["id"]
        setCoinData(coin_id, key_timestamp, uuid, timestamp, data)
        setCoinData(coin_id, key_price_usd, uuid, coin[key_price_usd], data)
        setCoinData(coin_id, key_percent_change_1h, uuid, coin[key_percent_change_1h], data)
        setCoinData(coin_id, key_percent_change_24h, uuid, coin[key_percent_change_24h], data)
        setCoinData(coin_id, key_percent_change_7d, uuid, coin[key_percent_change_7d], data)
        setCoinData(coin_id, key_24h_volume_usd, uuid, coin[key_24h_volume_usd], data)
        setCoinData(coin_id, key_market_cap_usd, uuid, coin[key_market_cap_usd], data)

    db.update(data)


def setGlobalData(key, uuid, value, data):
    data["global_stats" + "/" + key + "/" + uuid] = value


def setCoinData(coinId, key, uuid, value, data):
    data[coinId + "/" + key + "/" + uuid] = value
