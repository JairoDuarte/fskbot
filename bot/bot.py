# -*- coding: utf-8 -*-
import json

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from pymongo import MongoClient

from credentials import DB_PWD, DB_USER, DB_URL, DB_NAME, DB_PORT

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
    Conversation = bot.storage.get_model('conversation')
    Session = bot.storage.Session
    session = Session()
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
        existing_conversation = session.query(Conversation).get(conversation.id)  #Conversation_.query.filter(id=conversation.id)
        print('id '+str(existing_conversation.id))

        if existing_conversation:
            Statement = bot.storage.get_model('statement')

            statement_query = session.query(
                Statement
            ).filter(
                Statement.conversations.any(id=conversation.id)
            )

            for statement in statement_query:
                print(statement.get_statement())
                conversation.statements.append(statement.get_statement())

    except Exception as ex:
        data = '{}'
        conversation.id = bot.storage.create_conversation()
        json_conversation = json.loads(data)
        json_conversation['conversation_id'] = conversation.id
        json_conversation['user_id'] = user_id
        coll_conversation.insert_one(json_conversation)
        print(ex)

    session.close()
    connection.close()
    return conversation
