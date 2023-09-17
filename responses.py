import re
import commands
from classes.filasMantenedor import FilasMantenedor

class Responses():
    def __init__(self):
        self.Filas = FilasMantenedor

    def handle_response_msg(self, message) -> str:
        txt_command = re.sub(' +', ' ', message[1:])
        userArgs = txt_command.split(' ')
        return userArgs[1:]

    def showListFormatted(self):
        return commands.showList(self.Filas)

    def addAuthorToList(self, ctx):
        return commands.addUsersToList(self.Filas, [ctx.message.author])

    def addNamesToList(self, ctx, users):
        return commands.addUsersToList(self.Filas, users) 

    def addNewList(self, ctx, users):
        return commands.appendNewList(self.Filas, users)        
    
    def removeAuthorFromList(self, ctx):
        return commands.removeFromList(self.Filas, [ctx.message.author])

    def removeNamesFromList(self, ctx, users):
        return commands.removeFromList(self.Filas, users)    

    def removeList(self, number):
        return commands.removeList(self.Filas, int(number))        
    
    def lockUnlockGroupList(self):
        return commands.toggleListStatus(self.Filas)

    def defaultShuffle(self):
        return commands.qbgShuffleList(self.Filas, -1)

    def reShuffle(self):
        return commands.qbgShuffleList(self.Filas, 0)
    
    def shuffleEverything(self):
        return commands.qbgShuffleList(self.Filas, 2)

    def splitList(self, ctx = None):
        if (ctx != None and len(self.handle_response_msg(ctx.message.content)) > 0):
            return commands.splitList(self.Filas,int(self.handle_response_msg(ctx.message.content)[0]))
        else:
            return commands.splitList(self.Filas)
    
    def movePosition(self, ctx):
        return commands.movePositionFromList(self.Filas, self.handle_response_msg(ctx.message.content))

    def swapPosition(self, ctx):
        return commands.swapPositionFromList(self.Filas, self.handle_response_msg(ctx.message.content))

    def goodGames(self, ctx):
        return commands.advanceListStatus(self.Filas, ctx)

    def skipMatch(self, number):
        return commands.skipListStatus(self.Filas, number)

    def togglePlayerStatus(self, users):
        return commands.togglePlayerStatus(self.Filas, users)

    def startList(self):
        return commands.startList(self.Filas)

    def stopList(self):
        return commands.stopAllList(self.Filas)
responses = Responses()
