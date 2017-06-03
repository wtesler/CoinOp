__author__ = 'Will Tesler'

from datetime import datetime
import json
import pyrebase
from coinmarketcap import Market

# Firebase Config
config = {
    "apiKey": "FIREBASE_WEB_API_KEY",
    "authDomain": "mydomain.firebaseapp.com",
    "databaseURL": "https://myurl.firebaseio.com",
    "storageBucket": "tesler.will.coinop",
    "serviceAccount": "firebase-service-account.json"
}

GLOBAL_STATS = "global_stats"
TIMESTAMPS = "timestamps"
TOP_X_COINS = 10

def run(event, context):
    # The Database.
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    # The id associated with this particular run of the function.
    stepUuid = db.generate_key()

    # Current UTC Time
    timestamp = datetime.utcnow().strftime("%Y %m %d %H %M %S")

    # The market has coin data in it.
    market = Market()

    # Accumulate data in this update from the coin and global data.
    update = {}

    _addCoinData(market, update, stepUuid, timestamp)
    _addGlobalData(market, update, stepUuid, timestamp)

    db.update(update)


# Add new coin data from the market to our accumulating data.
def _addCoinData(market, data, stepUuid, timestamp):
    coin_stats = json.loads(market.ticker("?limit=" + str(TOP_X_COINS)))
    for coin in coin_stats:
        _setTimestamp(coin["id"], stepUuid, timestamp, data)
        _setCoinData(coin, "price_usd", stepUuid, data)
        _setCoinData(coin, "percent_change_1h", stepUuid, data)
        _setCoinData(coin, "percent_change_24h", stepUuid, data)
        _setCoinData(coin, "percent_change_7d", stepUuid, data)
        _setCoinData(coin, "24h_volume_usd", stepUuid, data)
        _setCoinData(coin, "market_cap_usd", stepUuid, data)


# Add new global data from the market to our accumulating data.
def _addGlobalData(market, data, stepUuid, timestamp):
    global_stats = json.loads(market.stats())
    _setTimestamp(GLOBAL_STATS, stepUuid, timestamp, data)
    _setGlobalData("total_24h_volume_usd", stepUuid, global_stats, data)
    _setGlobalData("total_market_cap_usd", stepUuid, global_stats, data)


def _setTimestamp(prefix, uuid, value, data):
    data[prefix + "/" + TIMESTAMPS + "/" + uuid] = value


def _setCoinData(coin, key, uuid, data):
    data[coin["id"] + "/" + key + "/" + uuid] = coin[key]


def _setGlobalData(key, uuid, global_stats, data):
    data[GLOBAL_STATS + "/" + key + "/" + uuid] = global_stats[key]
