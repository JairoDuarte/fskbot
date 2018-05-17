from __future__ import unicode_literals
from chatterbot.adapters import Adapter
from flask import Flask, request


class InputAdapter:
    AUDIO = 'audio'
    TEXT = 'text'
    IMAGE = 'image'
    VALID_FORMATS = (AUDIO, TEXT, IMAGE,)

    def __init__(self, data):
        self.data = data
        print('test')

    def detect_type(self):

        if self.data['entry'][0]['messaging'][0]['message']['text']:
            return self.TEXT
        else:
            if self.data['entry'][0]['messaging'][0]['message']['attachments'][0]['type'] == self.AUDIO:
                return self.AUDIO
            elif self.data['entry'][0]['messaging'][0]['message']['attachments'][0]['type'] == self.IMAGE:
                return self.IMAGE

    def process_input(self, *args, **kwargs):
        """
        Returns a statement object based on the input source.
        """

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

        except Exception as inst:
            print(inst)

        raise self.AdapterMethodNotImplementedError()

    def process_input_statement(self, *args, **kwargs):
        """
        Return an existing statement object (if one exists).
        """
        input_statement = self.process_input(*args, **kwargs)

        self.logger.info('Received input statement: {}'.format(input_statement.text))

        existing_statement = self.chatbot.storage.find(input_statement.text)

        if existing_statement:
            self.logger.info('"{}" is a known statement'.format(input_statement.text))
            input_statement = existing_statement
        else:
            self.logger.info('"{}" is not a known statement'.format(input_statement.text))

        return input_statement
