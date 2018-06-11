import requests
from fbmessenger import MessengerClient, elements
from flask import Flask, request
from credentials import FB_VERIFY_TOKEN, FB_ACCESS_TOKEN
from adapters.messenger import MessengerInput, MessengerOutput
from bot.bot import bot

app = Flask(__name__)
inputmessenger = MessengerInput(FB_ACCESS_TOKEN)
outputmessenger = MessengerOutput(inputmessenger.client)


@app.route('/app/facebook/webhook', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == FB_VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"


@app.route('/app/facebook/webhook', methods=['POST'])
def handle_messages():
    data = request.json
    message = data['entry'][0]['messaging'][0]
    print(message)
    outputmessenger.send_mark_seen(message['sender']['id'])
    msg = inputmessenger.message(message)

    if msg == '':
        outputmessenger.send_text_message(inputmessenger.get_user_id(), '')
    else:
        response = bot.get_response(msg)
        print(msg)
        print(response)
        outputmessenger.send_audio_message(inputmessenger.get_user_id(), response)

    """
    data = {
        "recipient": {"id": inputmessenger.get_user_id()},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    """

    return "success"


if __name__ == '__main__':
    app.run(debug=True)
else:
    app.run(debug=True)
