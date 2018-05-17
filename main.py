from flask import Flask, request
import requests
from fb_credentials import VERIFY_TOKEN, ACCESS_TOKEN
from adapters.messenger import MessengerInput
from adapters.speechTotext import YOUR_AUDIO_FILE,handler

app = Flask(__name__)

@app.route('/app/facebook/webhook', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"


@app.route('/app/facebook/webhook', methods=['POST'])
def handle_messages():
    data = request.json
    message = data['entry'][0]['messaging'][0]
    inputmessenger = MessengerInput(ACCESS_TOKEN)
    msg = inputmessenger.message(message)
    handler(msg)

    print(msg)

    return "success"


if __name__ == '__main__':
    app.run(debug=True)
else:
    app.run(debug=True)
