import requests
from fbmessenger import MessengerClient, elements
from flask import Flask, request
from fb_credentials import VERIFY_TOKEN, ACCESS_TOKEN
from adapters.messenger import MessengerInput,MessengerOutput

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
    client = MessengerClient(ACCESS_TOKEN)
    message = data['entry'][0]['messaging'][0]
    inputmessenger = MessengerInput(ACCESS_TOKEN,message)
    outputmessenger = MessengerOutput(inputmessenger.client)
    msg = inputmessenger.message()

    outputmessenger.send_text_message(inputmessenger.get_user_id(), msg)

    print(msg)

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
