from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from speech.speechTotext import speech_to_text
from speech.speech_to_text import get_text as gcc_get_text
from fbmessenger import BaseMessenger, elements, MessengerClient, attachments
from typing import Text, List, Dict, Any, Callable
from speech.texttospeech import get_url
logger = logging.getLogger(__name__)


class MessengerInput(BaseMessenger):
    """Implement a fbmessenger to parse incoming webhooks and send msgs."""

    def __init__(self, page_access_token):
        # type: (Text, Callable[[UserMessage], None]) -> None

        self.page_access_token = page_access_token
        super(MessengerInput, self).__init__(self.page_access_token)

    @staticmethod
    def _is_audio_message(message):
        # type: (Dict[Text, Any]) -> bool
        """Check if the users message is a recorced voice message."""
        return (message.get('message') and
                message['message'].get('attachments') and
                message['message']['attachments'][0]['type'] == 'audio')

    @staticmethod
    def _is_user_message(message):
        # type: (Dict[Text, Any]) -> bool
        """Check if the message is a message from the user"""
        return (message.get('message') and
                message['message'].get('text') and
                not message['message'].get("is_echo"))

    def message(self, msg):
        # type: (Dict[Text, Any]) -> None
        """Handle an incoming event from the fb webhook."""
        text = ''
        if self._is_user_message(msg):
            text = msg['message']['text']
            try:
                if self.last_message['message']['text'] == text:
                    print('txt')
                    return ''
            except Exception as exc:
                print(exc)
                pass
        elif self._is_audio_message(msg):
            attachment = msg['message']['attachments'][0]
            text = attachment['payload']['url']
            try:
                if self.last_message['message']['attachments'][0]['payload']['url'] == text:
                    print('url')
                    return ''
            except Exception as exc:
                print(exc)
                pass
            text = gcc_get_text(text)
        else:
            logger.warn("Received a message from facebook that we can not "
                        "handle. Message: {}".format(self.message))

        self.last_message = msg
        return text

    def postback(self, message):
        # type: (Dict[Text, Any]) -> None
        """Handle a postback (e.g. quick reply button)."""

        text = message['postback']['payload']
        self._handle_user_message(text, self.get_user_id())

    def _handle_user_message(self, text, sender_id):
        # type: (Text, Text) -> None
        """Pass on the text to the dialogue engine for processing."""

        # out_channel = MessengerBot(self.client)
        # user_msg = UserMessage(text, out_channel, sender_id)

    def delivery(self, message):
        # type: (Dict[Text, Any]) -> None
        """Do nothing. Method to handle `message_deliveries`"""
        pass

    def read(self, message):
        # type: (Dict[Text, Any]) -> None
        """Do nothing. Method to handle `message_reads`"""
        pass

    def account_linking(self, message):
        # type: (Dict[Text, Any]) -> None
        """Do nothing. Method to handle `account_linking`"""
        pass

    def optin(self, message):
        # type: (Dict[Text, Any]) -> None
        """Do nothing. Method to handle `messaging_optins`"""
        pass


class MessengerOutput:
    """A bot that uses fb-messenger to communicate."""

    def __init__(self, messenger_client):
        # type: (MessengerClient) -> None

        self.messenger_client = messenger_client

    def send(self, recipient_id, element):
        # type: (Text, Any) -> None
        """Sends a message to the recipient using the messenger client."""

        # this is a bit hacky, but the client doesn't have a proper API to
        # send messages but instead expects the incoming sender to be present
        # which we don't have as it is stored in the input channel.
        self.messenger_client.send(element.to_dict(),
                                   {"sender": {"id": recipient_id}},
                                   'RESPONSE')
        pass

    def send_text_message(self, recipient_id, message):
        # type: (Text, Text) -> None
        """Send a message through this channel."""
        print('sed text')
        logger.info("Sending message: " + message)

        self.send(recipient_id, elements.Text(text=message))

    def send_audio_message(self, recipient_id, message):
        # type: (Text, Text) -> None
        """Send a message through this channel."""
        print('sed text')
        logger.info("Sending message: " + message)
        url = get_url(message)
        self.send(recipient_id, elements.Text(text=message))

    def send_image_url(self, recipient_id, image_url):
        # type: (Text, Text) -> None
        """Sends an image. Default will just post the url as a string."""

        self.send(recipient_id, attachments.Image(url=image_url))

    def send_text_with_buttons(self, recipient_id, text, buttons, **kwargs):
        # type: (Text, Text, List[Dict[Text, Any]], **Any) -> None
        """Sends buttons to the output."""

        # buttons is a list of tuples: [(option_name,payload)]
        if len(buttons) > 3:
            logger.warn("Facebook API currently allows only up to 3 buttons. "
                        "If you add more, all will be ignored.")
            self.send_text_message(recipient_id, text)
        else:
            self._add_postback_info(buttons)

            # Currently there is no predefined way to create a message with
            # buttons in the fbmessenger framework - so we need to create the
            # payload on our own
            payload = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": buttons
                    }
                }
            }

    def send_custom_message(self, recipient_id, elements):
        # type: (Text, List[Dict[Text, Any]]) -> None
        """Sends elements to the output."""

        for element in elements:
            self._add_postback_info(element['buttons'])

        payload = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            }
        }
        self.messenger_client.send(payload,
                                   self._recipient_json(recipient_id),
                                   'RESPONSE')

    @staticmethod
    def _add_postback_info(buttons):
        # type: (List[Dict[Text, Any]]) -> None
        """Set the button type to postback for all buttons. Happens in place."""
        for button in buttons:
            button['type'] = "postback"

    @staticmethod
    def _recipient_json(recipient_id):
        # type: (Text) -> Dict[Text, Dict[Text, Text]]
        """Generate the response json for the recipient expected by FB."""
        return {"sender": {"id": recipient_id}}
