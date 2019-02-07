from flask import Flask, request, jsonify
from flask_sslify import SSLify
from typing import Tuple, Dict
import requests, json, re, os

app = Flask(__name__)
sslify = SSLify(app)

# INSERT YOUR ACCESS TOKEN INSTEAD OF MINE
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
URL = f'https://api.telegram.org/bot{ACCESS_TOKEN}/'


def send_message_to_user(chat_id: int, text: str) -> str:
    """ Sends response to users on their requests.
        For these purposes, Telegram API gives us sendMessage method,
        which takes POST-requests as json-objects.

        :param chat_id: id of chat with a user
        :param text: the message to send to a user
        :returns: Telegram response in json-format
    """

    url = f'{URL}sendMessage'
    telegram_answer = {'chat_id': chat_id, 'text': text,}
    response = requests.post(url, json=telegram_answer)
    return response.json()


def parse_user_message_to_telegram(user_message: str) -> Tuple[str]:
    """ Extracts the only /<cryptocurrency> text from user_message.
        Users can send any messages, so we need to get /<cryptocurrency>
        text, to give them the response, that they need.

        :param user_message: User message to telegram bot to be handled
        :returns: the name of cryptocurrency without "/" symbol
    """
    cryptocurrency = re.search(r'/\w+', user_message).group()
    return cryptocurrency[1:]


def get_cryptocurrency_price(cryptocurrency: str) -> str:
    """Extracts cryptocurrency price from coinmarketcap.com via its API

        :param cryptocurrency: cryptocurrency, which needs to extract the price
        :returns: the price of needed cryptocurrency in USD
    """
    url = f'https://api.coinmarketcap.com/v1/ticker/{cryptocurrency}'
    response = requests.get(url).json()
    return response[-1]['price_usd']


def get_user_telegram_chat_info(telegram_response: Dict[str, str]) -> Tuple[int, str]:
    """Retrieves chat_id and message from user telegram chat with bot

        :param telegram_response: Telegram chat data with a user
        :returns: user chat_id and user message to Telegram
    """
    chat_id = telegram_response['message']['chat']['id']
    message = telegram_response['message']['text']
    return chat_id, message


@app.route('/', methods=['POST', 'GET'])
def index() -> str:
    """ Handles user request to the bot and sends a response
    """
    if request.method == 'POST':
        telegram_response = request.get_json()
        # Getting chat_id and message from telegram response
        chat_id, message = get_user_telegram_chat_info(telegram_response)
        pattern = r'/\w+'
        if re.search(pattern, message):
            # Getting cryptocurrency price searched by a user
            price = get_cryptocurrency_price(parse_user_message_to_telegram(message))
            # Sending the price back to a user
            send_message_to_user(chat_id, text=price)
        return jsonify(telegram_response)
    return json.dumps({'Telegram bot is working': True}), 200, {'ContentType':'application/json'}


if __name__ == '__main__':
    app.run()
