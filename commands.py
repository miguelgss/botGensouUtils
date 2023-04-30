import random

groupList = [[]]

def showList() -> str:
    textoLista = ''
    if(len(groupList) < 1):
        return "Não existem listas no momento. Por favor, utilize o comando 'adiciona' ou 'adicionalista' para gerar uma nova lista."
    for index, lista in enumerate(groupList):
        textoLista += "Lista " + str(index+1) + ": \n"
        posCount = 1
        for name in lista:
            textoLista += str(posCount) + " - " + name + "; \n"
            posCount += 1

    return textoLista

# Criação, separação e exclusão de listas
def appendNewList(names):
    newlist = []
    msgsLista = 'Nova lista criada! \n'
    try:
        for name in names:
            jaEstaNaLista = False
            indexLista = 0
            for index, lista in enumerate(groupList):
                listLower = map(str.lower, lista)

                if name.lower() in listLower:
                    jaEstaNaLista = True
                    indexLista = index
            
            if(jaEstaNaLista):
                msgsLista += name + " já está na lista " + str(indexLista+1) + "! \n"
            else:
                newlist.append(name)
                msgsLista += name + " foi adicionado a nova lista! \n"          
        
        groupList.append(newlist)

        manageListTxtFile()
        return msgsLista
    except Exception as e:
        return "Erro: " + str(e)

def splitList(listIndex = 1):
    newlist = []
    msgLista = 'Nova lista criada! \n'
    listIndex -= 1
    try:
        newlist = groupList[listIndex][(len(groupList[listIndex])//2):]
        removeFromList(newlist)

        groupList.append(newlist)

        for name in newlist:
            msgLista += name + " foi adicionado a nova lista! \n"

        manageListTxtFile()
        return msgLista
    except Exception as e:
        return "Erro: " + str(e)

def removeList(listIndex):
    listIndex -= 1
    try:
        msgLista = "**_Backup listas passadas: _** \n" + showList()
        groupList.pop(listIndex)

        manageDeletedListTxtFile(listIndex)
        return msgLista
    except Exception as e:
        return "Erro: " + str(e)

# Manipulação dos nomes nas listas
def addToList(names):
    msgsLista = ''
    try:
        if(len(groupList) < 1):
            return appendNewList(names)
        for name in names:
            countNamesList = []
            jaEstaNaLista = False
            indexLista = 0
            for index, lista in enumerate(groupList):
                
                listLower = map(str.lower, lista)

                if name.lower() in listLower:
                    jaEstaNaLista = True
                    indexLista = index
                countNamesList.append(len(lista))
            
            if(jaEstaNaLista):
                msgsLista += name + " já está na lista " + str(indexLista+1) + "! \n"
            else:
                groupList[countNamesList.index(min(countNamesList))].append(name)
                msgsLista += name + " foi adicionado a lista! \n" 
        
        manageListTxtFile()
        return msgsLista
    except Exception as e:
        return "Erro: " + str(e)
    

def qbgShuffleList(shuffleOrReShuffle):
    try:
        for index, lista in enumerate(groupList):
            newlist = [lista[shuffleOrReShuffle]]
            lista.remove(lista[shuffleOrReShuffle])

            if(len(lista) > 1):
                random.shuffle(lista)
            
            for element in lista:
                newlist.append(element)
            
            groupList[index] = newlist.copy()
            
        manageListTxtFile()
        return showList()
    except Exception as e:
        return "Erro: " + str(e)
    
def removeFromList(names):
    try:
        msgsLista = ""
        for name in names:
            for lista in groupList:
                try:
                    lista.remove(name)
                    msgsLista += name + " foi removido! \n"
                except Exception as e:
                    continue

        manageListTxtFile()
        return msgsLista

    except Exception as e:
        return "Não foi possível remover o nome solicitado. Por favor, verifique a escrita ou o que há na lista e tente novamente."

def movePositionFromList(positions):
    try:
        if(len(positions) != 2 and len(positions) != 4):
            raise Exception("O número de argumentos está fora do formato. Informe 2 argumentos (apenas as posições para mexer na primeira lista) ou 4 argumentos (para mover posições de outras listas ou entre listas).")
        for index, number in enumerate(positions):
            positions[index] = int(number)
        for index,number in enumerate(positions):
            positions[index] = number -1
        if(len(positions) == 2):
            movedName = groupList[0][positions[0]]
            groupList[0].remove(movedName)
            groupList[0] = groupList[0][0:positions[1]] + [movedName] + groupList[0][positions[1]:]
        elif(len(positions) == 4):
            movedName = groupList[positions[0]][positions[1]]
            groupList[positions[0]].remove(movedName)
            groupList[positions[2]] = groupList[positions[2]][0:positions[3]] + [movedName] + groupList[positions[2]][positions[3]:]
        manageListTxtFile()
        return showList()
    except Exception as e:
        return "Erro: " + str(e)

def swapPositionFromList(positions):
    try:
        if(len(positions) != 2 and len(positions) != 4):
            raise Exception("O número de argumentos está fora do formato. Informe 2 argumentos (apenas as posições para mexer na primeira lista) ou 4 argumentos (para mover posições de outras listas ou entre listas).")
        for index, number in enumerate(positions):
            positions[index] = int(number)
        for index,number in enumerate(positions):
            positions[index] = number -1
        if(len(positions) == 2):
            groupList[0][positions[0]], groupList[0][positions[1]] = groupList[0][positions[1]], groupList[0][positions[0]]
        elif(len(positions) == 4):
            groupList[positions[0]][positions[1]], groupList[positions[2]][positions[3]] = groupList[positions[2]][positions[3]], groupList[positions[0]][positions[1]]

        manageListTxtFile()
        return showList()
    except Exception as e:
        return "Erro: " + str(e)

# Criação de arquivo com a lista
def manageListTxtFile():
    for index, lista in enumerate(groupList):
        textoLista = ''
        textoLista += "Lista " + str(index+1) + ": \n"
        posCount = 1
        for name in lista:
            textoLista += str(posCount) + " - " + name + "; \n"
            posCount += 1
        with open('listOBS' + str(index+1) + '.txt', 'w') as file:
            file.write(textoLista)

def manageDeletedListTxtFile(removedIndex):
    with open('listOBS' + str(removedIndex+1) + '.txt', 'w') as file:
        file.write(' ')