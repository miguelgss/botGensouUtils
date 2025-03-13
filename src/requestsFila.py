import re
import commands
from classes.filasMantenedor import FilasMantenedor
from constantes import numeros
from classes.jogador import Jogador

class RequestsFila():
    def __init__(self, filas:FilasMantenedor):
        self.Filas = filas

    def handle_response_msg(self, message) -> str:
        txt_command = re.sub(' +', ' ', message[1:])
        userArgs = txt_command.split(' ')
        return userArgs[1:]

    def showListFormatted(self):
        return commands.showList(self.Filas)

    def addAuthorToList(self, ctx):
        result = commands.addUsersToList(self.Filas, [ctx.message.author])
        self.Filas.notify_listeners()
        return result 

    def addNamesToList(self, ctx, users):
        result = commands.addUsersToList(self.Filas, users)
        self.Filas.notify_listeners() 
        return result

    def addNewList(self, ctx, users):
        result = commands.appendNewList(self.Filas, users)      
        self.Filas.notify_listeners() 
        return result
    
    def removeAuthorFromList(self, ctx):
        result = commands.removeFromList(self.Filas, [ctx.message.author])
        self.Filas.notify_listeners()
        return result

    def removeNamesFromList(self, ctx, users):
        result = commands.removeFromList(self.Filas, users)
        self.Filas.notify_listeners()
        return result

    def removeList(self, number):
        result = commands.removeList(self.Filas, int(number)) 
        self.Filas.notify_listeners()
        return result

    def lockUnlockGroupList(self):
        result = commands.toggleIsGroupListLocked(self.Filas)
        self.Filas.notify_listeners()
        return result
    
    def loopUnloopLists(self):
        return commands.toggleAreListsLooping(self.Filas)

    def defaultShuffle(self):
        result = commands.qbgShuffleList(self.Filas, numeros.DEFAULT_SHUFFLE)
        self.Filas.notify_listeners()
        return result

    def reShuffle(self):
        result = commands.qbgShuffleList(self.Filas, numeros.RESHUFFLE)
        self.Filas.notify_listeners()
        return result
    
    def shuffleEverything(self):
        result = commands.qbgShuffleList(self.Filas, numeros.SHUFFLE_EVERYTHING)
        self.Filas.notify_listeners()
        return result

    def splitList(self, ctx = None):
        result = None
        if (ctx != None and len(self.handle_response_msg(ctx.message.content)) > 0):
            result = commands.splitList(self.Filas,int(self.handle_response_msg(ctx.message.content)[0]))
        else:
            result = commands.splitList(self.Filas)
        self.Filas.notify_listeners()
        return result
    
    def movePosition(self, ctx):
        result = commands.movePositionFromList(self.Filas, self.handle_response_msg(ctx.message.content))
        self.Filas.notify_listeners()
        return result

    def swapPosition(self, ctx):
        result = commands.swapPositionFromList(self.Filas, self.handle_response_msg(ctx.message.content))
        self.Filas.notify_listeners()
        return result

    def goodGames(self, ctx):
        result = commands.swapPositionFromList(self.Filas, self.handle_response_msg(ctx.message.content))
        self.Filas.notify_listeners()
        return result

    def skipMatch(self, number):
        result = commands.skipListStatus(self.Filas, number)
        self.Filas.notify_listeners()
        return result

    def togglePlayerStatus(self, users):
        result = commands.togglePlayerStatus(self.Filas, users)
        self.Filas.notify_listeners()
        return result

    def startList(self, number):
        result = commands.startList(self.Filas, number)
        self.Filas.notify_listeners()
        return result

    def stopList(self):
        result = commands.stopAllList(self.Filas)
        self.Filas.notify_listeners()
        return result

    # COMANDOS EXCLUSIVOS PARA A INTERFACE VISUAL
    def getGroupList(self):
        return self.Filas.groupList