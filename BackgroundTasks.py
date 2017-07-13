#!/usr/bin/python
import chatexchange
import threading
import Chatcommunicate
import time
from Utilities import rooms
import Utilities
import TrackBots
import chatexchangeExtension as ceExt

shouldShutdown = False
shouldReboot = False

def listenForMessages (client, roomIDs):
    for each_id in roomIDs:
        rooms.append (client.get_room (each_id))

    for each_room in rooms:
        each_room.join()
        print ("Joined room " + str(each_room.id) + ".")
        each_room.send_message("Thunder started.")
    
        each_room.watch (Chatcommunicate.handleMessage)


def scheduleBackgroundTasks (client, roomIDs):
    #Listen for input
    inputListener = threading.Thread (target=listenForMessages, args=(client, roomIDs), kwargs={})

    inputListener.start()
    
    botListLen = len (TrackBots.botsList)
    
    #Load the list of bots from the pickle
    TrackBots.botsList = Utilities.loadFromPickle ("bot_list.pickle")

    while (1):
        try:
            #Remove commands which have completed.
            if len (Chatcommunicate.runningCommands) > 0:
                for i in range (len(Chatcommunicate.runningCommands)):
                    print ("STATUS:")
                    print (str (Chatcommunicate.runningCommands [i]["thread"].is_alive()))
                    if Chatcommunicate.runningCommands [i]["thread"].is_alive() != True:
                        print ("deleting...")
                        del Chatcommunicate.runningCommands [i]
        except TypeError:
            pass
    
        if shouldShutdown == True or shouldReboot == True:
            break
        
        if len (TrackBots.botsList) != botListLen:
            botListLen = len (TrackBots.botsList)
            Utilities.saveToPickle ("bot_list.pickle", TrackBots.botsList)
        
        #Check if a bot is dead
        for each_bot in TrackBots.botsList:
            if TrackBots.isBotAlive (each_bot ["user_id"]) == False and each_bot ["status"] == "alive":
                for each_room in each_bot ["rooms"]:
                    ceExt.getRoomFromID (each_room).send_message ("@" + each_bot ["name"] + " alive")
                currentTime = time.time()
                while (time.time() - currentTime < 30):
                    if TrackBots.isBotAlive (each_bot ["user_id"]) == True:
                        break

                if TrackBots.isBotAlive (each_bot ["user_id"]) == False:
                    for each_room in each_bot ["rooms"]:
                        ceExt.getRoomFromID (each_room).send_message (each_bot ["name"] + " is dead. " + each_bot ["to_ping"])
                            
                    each_bot ["status"] = "dead"

        time.sleep (1)

    for each_room in rooms:
        each_room.leave()
