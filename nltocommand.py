from geminillm import gemrequest
from cfllm import nsllmreq

def shouldIRespond(LoA, messages):#I'm going to expect a message list for this, though not sure how that'd look exactly.
    construct = ""

    construct += "A bot is capable of doing the following.\n"

    for i in LoA:
        construct += i
        construct += "\n"

    construct += "The following is a list of recent messages. Would the bot be able to meaningfully contribute? Reply with 1 for yes and 0 for no.\n"

    for i in messages:
        construct += i
        construct += "\n"

    try:
        gem = gemrequest(construct)[1]
    except:
        gem = nsllmreq("Only reply with a number. Do not contain any other text.",construct)

    try:
        return int(gem)
    except:
        return -1

def nltocommand(LoA, command):
    construct = ""

    construct += "The following is a list of actions a bot can take. Look at the message from the user and return only the number of the action that is most appropriate. \n"
    for i in LoA:
        construct += i
        construct += "\n"
    construct += "Command: " + command

    try:
        #Gemini API errored out on me once... not again.
        gem = gemrequest(construct)[1]
    except:
        #This might be less acuurate though.
        gem = nsllmreq("Only reply with a number. Do not contain any other text.",construct)

    try:
        return int(gem)
    except:
        return -1


if __name__ == "__main__":
    print(nltocommand(["0. Summary", "1. Conversation", "2. File conversion", "3. Transcription"], input("Input user message: ")))