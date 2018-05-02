from flask import Flask, request
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAAC7WhfEH1IBAE4osJZC7rimawM24MZAQP11jdhKg5vLWeY3XObNg8cQISQMOEfqjaTTCI0TZC22z20qbNZCFDKfz4xi0Q01Ewv0JNuXSUEX0ZCiDkWMqoZCx7BUq3DfyTOp9YCeFjibv38QfimoNpEEG2BgDohB02GATNZAS32JQZDZD"
VERIFY_TOKEN = "secret"


def reply(data):
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = ''
    message = 'test'
    try:
        print(data)
        user_id = data['entry'][0]['messaging'][0]['sender']['id']
        message = data['entry'][0]['messaging'][0]['message']['text']
        print(message)
        data = {
            "recipient": {"id": user_id},
            "message": {"text": message}
        }
        reply(data)

    except Exception as inst:
        try:
            print(data)
            user_id = data['entry'][0]['messaging'][0]['sender']['id']
            url = data['entry'][0]['messaging'][0]['message']['attachments'][0]['payload']['url']
            data = {
                "recipient": {"id": user_id},
                "message": {"attachment": {"type": "audio", "payload": {
                    "url": url,
                    "is_reusable": True}}}
            }
            reply(data)
        except Exception as exc:
            print(inst)
            print(exc)

    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
else:
    app.run(debug=True)
