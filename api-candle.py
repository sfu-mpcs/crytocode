# Using candels channel 

import time
import json
import jwt
import hashlib
import os
import websocket
import threading
import http.client
from datetime import datetime, timedelta
from private.private import *
from const import *


# API credentials

if not CDP_API_KEY or not CDP_API_KEY:
    raise ValueError("Missing mandatory environment variable(s)")

def sign_with_jwt(message, channel, products=[]):
    payload = {
        "iss": "coinbase-cloud",
        "nbf": int(time.time()),
        "exp": int(time.time()) + 120,
        "sub": CDP_API_KEY,
    }
    headers = {
        "kid": CDP_API_KEY,
        "nonce": hashlib.sha256(os.urandom(16)).hexdigest()
    }
    token = jwt.encode(payload, CDP_PRIVATE_KEY, algorithm=ALGORITHM_COINBASE, headers=headers)
    message['jwt'] = token
    return message

def on_message(ws, message ):
    data = json.loads(message)
    with open("Coins-USD-market.txt", "a") as f:
        f.write(json.dumps(data) + "\n")

def subscribe_to_products(ws, products, channel_name):
    message = {
        "type": "subscribe",
        "channel": channel_name,
        "product_ids": products
    }
    signed_message = sign_with_jwt(message, channel_name, products)
    ws.send(json.dumps(signed_message))

def unsubscribe_to_products(ws, products, channel_name):
    message = {
        "type": "unsubscribe",
        "channel": channel_name,
        "product_ids": products
    }
    signed_message = sign_with_jwt(message, channel_name, products)
    ws.send(json.dumps(signed_message))

def on_open(ws):
    '''
    conn = http.client.HTTPSConnection("api.exchange.coinbase.com")
    headers = {'Content-Type': 'application/json'}
    conn.request("GET", "/currencies", '', headers)
    res = conn.getresponse()
    data = res.read()
    parsed_data = json.loads(data)

    ids = [str(item['id'] + '-USD') for item in parsed_data] 
    with open('names-usd.txt', 'r') as f:
        products2 = [
            line.strip().replace('"', '').replace(',', '') for line in f.readlines() if line.strip()
        ]
    products = list(set(products2[:10])) 
    print("Subscribing to:", products) 
    '''
    print(coins)
    # candles ors level2 
    subscribe_to_products(ws, coins, COINBASE_CHANNEL_NAMES["candles"])

def start_websocket():
    ws = websocket.WebSocketApp(WS_API_COINBASE_URL, on_open=on_open, on_message=on_message)
    ws.run_forever()

def main():
    ws_thread = threading.Thread(target=start_websocket)
    ws_thread.start()

    sent_unsub = False
    start_time = datetime.utcnow()

    try:
        while True:
            if (datetime.utcnow() - start_time).total_seconds() > 5 and not sent_unsub:
                # Unsubscribe after 5 seconds
                ws = websocket.create_connection(WS_API_COINBASE_URL)
                unsubscribe_to_products(ws, ["BTC-USD"], COINBASE_CHANNEL_NAMES["candles"])
                ws.close()
                sent_unsub = True
            time.sleep(1)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()