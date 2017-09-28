from flask import Flask
from flask_ask import Ask, statement, question
import requests
import json
import random
import os
import logging

app = Flask(__name__)
ask = Ask(app, '/')


# log = logging.getLogger()
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)
# logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.default_intent
def default():
    help_text = "hmm I didn't quite get that..." \
                "You can ask Doge Ticker tell me the current dogecoin price," \
                "or, you can say exit. What can I help you with?"
    return question(help_text).reprompt(help_text)


@ask.intent('priceInquiry')
def showPrice():
    response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=DOGE&tsyms=USD')
    json_data = json.loads(response.text)
    price = float(json_data['USD']) * 1000

    speech_text = ["The exchange rate is currently " + '${:,.2f}'.format(price) + " USD for 1000 dogecoins",
                   "Currently, 1000 dogecoins cost " + '${:,.2f}'.format(price) + " USD",
                   "Dogecoins are " + '${:,.2f}'.format(price) + " USD for 1000 coins",
                   "Much wow! " + '${:,.2f}'.format(price) + " USD for 1000 dogecoins. Very rich!"]

    speech_text = speech_text[random.randint(0,3)]


    return statement(speech_text).simple_card(speech_text)


@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = "Good bye!"
    return statement(bye_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = "You can ask Doge Ticker tell me the current dogecoin price, " \
                " or you can say exit. What can I help you with?"
    return question(help_text).reprompt("Hmm... I didn't quite get that. " + help_text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    bye_text = "Wow. so doge. much nice. very money."
    return statement(bye_text)


@ask.launch
def new_game():
    prompt = "Hmm... I didn't quite get that. You can ask Doge Ticker tell me the current dogecoin price, " \
                "or you can say exit. What can I help you with?"
    return question("Welcome to Doge Ticker! Please ask me about the current dogecoin price").reprompt(prompt)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run()
