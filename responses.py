import re
import commands
import commandNames as cn

def handle_response(messageObj, message) -> str:
    # Remove espaços extras
    txt_command = re.sub(' +', ' ', message[1:])
    txt_splitted = txt_command.split(' ')
    userInput = txt_splitted[0].lower()
    prefix = message[0]

    hasPermission = checkRoles(messageObj.author.roles, getValidRoles())
    if prefix == '{':
        if checkCommand(userInput, cn.adiciona, hasPermission):
            return commands.addToList(txt_splitted[1:])
        
        if checkCommand(userInput, cn.adicionalista, hasPermission):
            return commands.appendNewList(txt_splitted[1:])

        if checkCommand(userInput, cn.remove, hasPermission):
            return commands.removeFromList(txt_splitted[1:])

        if checkCommand(userInput, cn.removelista, hasPermission):
            return commands.removeList(int(txt_splitted[1]))

        if checkCommand(userInput, cn.embaralha, hasPermission):
            return commands.qbgShuffleList(-1)
        
        if checkCommand(userInput, cn.reembaralha, hasPermission):
            return commands.qbgShuffleList(0)

        if checkCommand(userInput, cn.embaralhatodos, hasPermission):
            return commands.qbgShuffleList(2)

        if checkCommand(userInput, cn.separar, hasPermission):
            if (len(txt_splitted) > 1):
                return commands.splitList(int(txt_splitted[1]))
            else:
                return commands.splitList()
        
        if checkCommand(userInput, cn.move, hasPermission):
            return commands.movePositionFromList(txt_splitted[1:])

        if checkCommand(userInput, cn.trocar, hasPermission):
            return commands.swapPositionFromList(txt_splitted[1:])

        if checkCommand(userInput, cn.lista):
            return commands.showList()
            
        if checkCommand(userInput, cn.adicioname):
            return commands.addToList( [str(messageObj.author.name)])

        if checkCommand(userInput, cn.removeme):
            return commands.removeFromList( [str(messageObj.author.name)] )

        if checkCommand(userInput, cn.ajuda):
            ajudaRetorno = "Comandos: \n"
            for text in cn.ajudaList:
                ajudaRetorno += "> " + text
                ajudaRetorno += "\n"
            return ajudaRetorno

def checkCommand(userInput, commandName, hasPermission = True) -> bool:
    if(hasPermission):
        for command in commandName:
            if(userInput == command):
                return True
    return False

## Métodos de verificação

def checkRoles(userRoles, validRoles) -> bool:
    if(len(validRoles) == 0):
        return True
    for user in userRoles:
        for valid in validRoles:
            if(re.search(str(user).lower(),str(valid).lower())):
                return True
    return False

def getValidRoles():
    listRoles = []
    retornoList = []

    with open('config.txt') as f:   
        for line in f:
            if re.search("roles", line):
                listRoles = line.split("=")
                listRoles.pop(0)
                for i in listRoles:
                    j = i.split(',')
                    retornoList = j
    
    return retornoList