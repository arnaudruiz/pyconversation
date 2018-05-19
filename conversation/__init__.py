#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    conversation module
'''

__version__ = "0.0.1"
__author__ = 'Arnaud Ruiz'
__email__ = 'arnaud.ruiz@us.bnpparibas.com'
__copyright__ = 'Copyright 2018, BNP Paribas'
__maintainer__ = "GM Site Builders"
__status__ = "Development"

import logging
from .intent import Intent
from .lingo import Lingo

class Conversation(object):
    """This object represents a conversation between the bot and the user.
    Attributes:
        config (:obj:`file`): Configuration file.
        logger (:obj:`logging`): logging object.
        lingo (:class:`conversation.Lingo`): The lingo class allowing to process messages.
        _intent (:class:`conversation.Intent`): Optional. The identified intent for this conversation.
        inProgress (:bool:): Optional. Weither the conversation is already in progress or not.
        response (:str: []): Optional. Array of sentences that represent the latest response by the bot
    Args:
        config (:obj:`file`): Configuration file.
    """
    def __init__(self, configFile = None, logger=None, replyTo = None):
        self.logger = logger or logging.getLogger(__name__)
        self.logger.debug("New interpreter instance")
        self.history = []
        self.lingo = Lingo()
        self.inProgress = False
        self._intent = None
        self.dialogState = None
        self.response = []
        self.reply = replyTo

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, value):
        self._history = value

    def _historize(self, value):
        self._history.append(value)

    @property
    def lastMessage(self):
        return self._history[-1]

    @property
    def intent(self):
        '''
        Returns the intent if it has already been identified
        otherwise try to match the last message with an intent
        '''
        if self._intent:
            return self._intent
        else: 
            self.logger.debug("No intent identified yet")
            self.intent = self.lingo.getIntent(self.lastMessage)
            return self._intent

    @intent.setter
    def intent(self, value):
        self._intent = value

    def talk(self, msg):
        print(msg)
        self._historize(msg)
        if self.inProgress:
            self._carryOn()
        else: 
            self._start()

    
    def _start(self):
        '''
        Starting conversation
        '''
        self.logger.debug("Starting new conversation")
        self.inProgress = True

        if self.intent.intro:
            self.reply(self.intent.intro)

        #If message is available, check if we can already fill some of the slots (hashtags and mention)
        
        #If there is a slot to ellicit for this intent we change the status 
        firstSlot = self._nextSlotToEllicit()
        if firstSlot:
            self.dialogState = "EllicitSlot"
        else:
            #Intent can be imediately fullfilled
            self.dialogState = "readyToFulfill"
        print ("Conversation:",self.dialogState)
        self._carryOn()


    def _carryOn(self):
        '''
            This function continue the conversation by identifying
            and sending the next message in the intent
        '''
        self.logger.debug("Carrying on existing conversation")
        
        if self.dialogState == "EllicitSlot":
            slot = self._nextSlotToEllicit()
            if slot:
                if not message:
                    # we display the message relative to the slot to ellicit
                    if slot.prompts:
                        for prompt in slot.prompts:
                            if prompt.name == "elicit":
                                self.reply(prompt.text)
                else:
                    # Check the answer
                    def slotValidationResult(valid):
                        if valid:
                            # The slot is valid
                            if slot.confirmationRequired:
                                # If it needs confirmation we reflect this in the dialog state
                                self.slotToValidate = slot
                                self.dialogState = "ConfirmSlot"
                                valueToConfirm = slot.value
                                if "|||" in valueToConfirm:
                                    valueToConfirm = slot.value.split("|||")[0]
                                self.reply("Is that {}?".format(valueToConfirm))
                            else:
                                # If the slot is valid we save it to the conversation
                                self.slots.append(slot)
                                # Then we carry on the conversation
                                self._carryOn(message=None)
                        else:
                            self.reply("Sorry I didn't get that. Please try again.")
                            self._carryOn(message=None)

                    slot.validate(message.body,slotValidationResult)
            else:
                self.dialogState = "readyToFulfill"
                self._carryOn(message=None)

        elif self.dialogState == "ConfirmSlot":
            yes = ["yes","yep","oui","y","si"]
                        
            if message.body.lower() in yes:
                self.slots.append(self.slotToValidate)
                self.slotToValidate = None
                self.dialogState = "EllicitSlot"
                self._carryOn(message=None)
            else:
                self.slotToValidate = None
                self.dialogState = "EllicitSlot"
                self.reply("Ok. Please try again with another value")
        
        elif self.dialogState == "readyToFulfill":
            if self.intent.readyFulfillMsg:
                self.reply(self.intent.readyFulfillMsg)
                     
    def _nextSlotToEllicit(self):
        if self.intent.hasSlots:
            for slot in self.intent.slots:
                #if an elicitation of the slot is required...
                if slot.elicitationRequired:
                    #we skip the slot if it is already fulfilled
                    if slot.value:
                        continue
                    #We return the slot
                    return slot
            print ("No more slot to elicit")
            return None #no more slot to elicit
        else:
            print ("No slot")
            return None