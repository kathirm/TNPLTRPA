from skpy import Skype
sk = Skype("terafastnetworkteam@gmail.com", "Terafastnetworkspvtltd") # connect to Skype
sk.user # you
cont = sk.contacts # your contacts
sk.chats # your conversations
#ch = sk.chats.create(["joe.4", "daisy.5"]) # new group conversation
ch = sk.contacts["live:imkathir"].chat # 1-to-1 conversation
ch.sendMsg("Hi (Y) AJAY (cake) ") # plain-text message
#ch.sendFile(open("song.mp3", "rb"), "song.mp3") # file upload
#ch.sendContact(sk.contacts["daisy.5"]) # contact sharing
ch.getMsgs() # retrieve recent messages
