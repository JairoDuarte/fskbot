# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot
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
            'default_response': 'Je suis désolé, mais je n\'ai pas comprise'
        }
    ],
    output_adapter="chatterbot.output.OutputAdapter",
    database="./database.db"
)
bot.set_trainer(ChatterBotCorpusTrainer)
# First, lets train our bot with some data
#bot.train('chatterbot.corpus.french.conversations')
#bot.train('chatterbot.corpus.french')
bot.train("./bot/data/")
