# To keep the bot alive while running on replit
# This is the websocket server
# To keep the bot going even after closing the replit tab

from flask import Flask
from threading import Thread # To run the server in a separate thread from the bot

app = Flask('')

@app.route('/')
def home():
  return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
