

import conversation

def postOnScreen(msg):
    print(msg)

myConversation = conversation.Conversation(replyTo=postOnScreen)
myConversation.talk("Do you have John Doe's bio?")
