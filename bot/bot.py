# -*- coding: utf-8 -*-
import json
import os

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from pymongo import MongoClient
from django.apps import apps
from django.conf import settings

from credentials import DB_PWD, DB_USER, DB_URL, DB_NAME, DB_PORT

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot.settings")
apps.populate(settings.INSTALLED_APPS)




bot = ChatBot(
    "Terminal",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': "Je suis désolé, mais je n'ai pas comprise."
        }
    ],
    output_adapter="chatterbot.output.OutputAdapter"
)
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train('chatterbot.corpus.french')
bot.train("./bot/data/")


def get_conversation(user_id):
    """
    Return the conversation for the session if one exists.
    Create a new conversation if one does not exist.
    """
    from chatterbot.conversation import Response
    Conversation = bot.storage.get_model('conversation')
    connection = MongoClient(DB_URL, DB_PORT)
    db = connection[DB_NAME]
    db.authenticate(DB_USER, DB_PWD)

    coll_conversation = db.conversation

    class Obj(object):
        def __init__(self):
            self.id = None
            self.statements = []

    conversation = Obj()

    try:
        conversation_ = coll_conversation.find_one({"user_id": user_id})
        print(conversation_)
        conversation.id =  conversation_['conversation_id']
        print(conversation.id)
    except Exception as ex:
        conversation.id = 0

    existing_conversation = False
    try:
        print('try 2')
        Conversation.objects.get(id=conversation.id)
        print('get conversation')
        existing_conversation = True

    except Conversation.DoesNotExist:
        data = '{}'
        conversation.id = bot.storage.create_conversation()
        json_conversation = json.loads(data)
        json_conversation['conversation_id'] = conversation.id
        json_conversation['user_id'] = user_id
        coll_conversation.insert_one(json_conversation)

    if existing_conversation:
        responses = Response.objects.filter(
            conversations__id=conversation.id
        )

        for response in responses:
            conversation.statements.append(response.statement.serialize())
            conversation.statements.append(response.response.serialize())

    connection.close()
    return conversation
