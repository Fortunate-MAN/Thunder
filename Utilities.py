#!/usr/bin/python

import pickle

#The chat host
host = "stackoverflow.com"

#This will contain an array of the Class 'Room' once the bot joins the specified rooms
rooms = list ()

#The roomIDs the bot should join
roomIDs = [123602, 1]

myself = None
client = None

#The name of the bot. A message must start with this name to be recognized as a command
name = "@TestBot"

#The number of characters of the name that must be included
minNameCharacters = 4

def saveToPickle (filename, list):
    try:
        with open (filename, 'wb') as toSave:
            pickle.dump (list, toSave)
    except IOError as err:
        print ("File Error: " + err)
    except pickle.PickleError as perr:
        print ("Pickle Error: " + perr)

def loadFromPickle (filename):
    try:
        with open (filename, "rb") as toRead:
            return pickle.load (toRead)
    except IOError as err:
        print ("File Error: " + str(err))
    except pickle.PickleError as perr:
        print ("Pickle Error: " + str(perr))
    
    return []

