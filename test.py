

import conversation

def postOnScreen(msg):
    print(msg)

myConversation = conversation.Conversation(replyTo=postOnScreen)
myConversation.talk("Do you have Paul Mortimer's bio?")
#myConversation.talk("Paul mortimer's bio")
#myConversation.talk("/find @Arnaud Ruiz")
