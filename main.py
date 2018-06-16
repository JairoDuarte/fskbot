from flask import Flask, request
import os
from adapters.messenger import MessengerInput, MessengerOutput
from bot.bot import bot
from credentials import FB_ACCESS_TOKEN, FB_VERIFY_TOKEN

app = Flask(__name__)
inputmessenger = MessengerInput(FB_ACCESS_TOKEN)
outputmessenger = MessengerOutput(inputmessenger.client)

@app.route('/')
def hello_world():
  return 'Chatbot online'

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
        outputmessenger.send_audio_message(inputmessenger.get_user_id(), str(response))

    return "success"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
else:
    app.run(debug=True)
