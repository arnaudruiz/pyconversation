import logging
import os
import sys
import json

from .intent import Intent

import spacy
nlp = spacy.load('en_core_web_sm')

class Lingo(object):
    """This object represents the linguistic used by the bot.
    Attributes:
        config (:obj:`file`): Configuration file.
        intents (:class:`conversation.Intent`): Optional. The conversation intents.
    Args:
        config (:obj:`file`): Configuration file.
    """

    def __init__(self, config = None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.logger.debug("Loading lingo")
        self.intents = []

        # Loading config file
        self.config = self.Config(self, config)
        try:
            self._loadIntents(self.config["resource"]["intents"])
        except Exception as e:
            print(e)

    class Config(object):
        def __init__(self, interpreter, filename):
            
            self.interpreter = interpreter

            if filename is None:
                self.configFile = "config.json"
            else:
                self.configFile = filename

            self.configPath = os.path.join(os.path.dirname(sys.argv[0]), self.configFile)
            
            if not os.path.exists(self.configPath):
                interpreter.logger.critical("Cannot find the configuration file")
                sys.exit(1)

            with open(self.configPath) as f:
                self.config = json.load(f)

        def __getitem__(self, item):
            return self.config[item]

    def _loadIntents(self, intents):
        for el in intents:
            intent = Intent()
            intent.parse(el)
            self.intents.append(intent)
    
    def getIntent(self, text):
        """
        Args:
            text (:obj:`str`): the message to analyze.

        Returns:
            :obj:`str`: the identified intent.
        """
        self.logger.debug("Matching intent...")

        doc = nlp(text)
        
        highestScore = 0
        bestIntent = None

        # compare with intents utterances
        for intent in self.intents:
            intentAvgScore = 0
            for utterance in intent.sampleUtterances:
                sample = nlp(utterance)
                score = doc.similarity(sample)
                intentAvgScore += score 
                if score > highestScore:
                    highestScore = score
                    bestIntent = intent

        # TODO: IF Score < 0.75 ? DECOMPOSE SENTENCE 

        print("Closest intent: ",bestIntent.name,"Score:",highestScore)
        return bestIntent

    def deconstruct(self, text):
        doc = nlp(text)
        ents = list(doc.ents) #Export entities
        for entity in ents:
            print(entity.label, entity.label_, ' '.join(t.orth_ for t in entity))
        