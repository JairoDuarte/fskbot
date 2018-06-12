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
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],
    output_adapter="chatterbot.output.OutputAdapter",
    database="../database.db"
)
bot.set_trainer(ChatterBotCorpusTrainer)
# First, lets train our bot with some data
#bot.train('chatterbot.corpus.french.conversations')
bot.train('chatterbot.corpus.french.greetings')
bot.train('chatterbot.corpus.french.trivia')
#bot.train('chatterbot.corpus.french.faqiam')
#bot.train('chatterbot.corpus.french.faqinwi')

# Print an example of getting one math based response


# Print an example of getting one time based response
"""
response = bot.get_response("What time is it?")
print(response)
response = bot.get_response(" COMMENT RECHARGER MON COMPTE JAWAL ?")
print(response)
"""
