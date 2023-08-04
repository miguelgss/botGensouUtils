import random
from errors import ExpectedException
from enums import Color, ErrorMessages, StatusLista
from classes.jogador import Jogador

#TODO: Registrar a classe 'Jogador" na lista ao invés do nome em texto.

def toggleListStatus(filas):
    filas.isGroupListLocked = not filas.isGroupListLocked
    if (not filas.isGroupListLocked):
        filas.waitList
        addToList(filas, filas.waitList)
        filas.waitList = []
    return StatusLista.Bloqueada.value if filas.isGroupListLocked else StatusLista.Desbloqueada.value

def showList(groupList: list, isGroupListLocked: bool, waitList: list) -> str:
    textoLista = StatusLista.Bloqueada.value + '\n\n' if isGroupListLocked else ''
    if(len(groupList) < 1):
        raise ExpectedException("Não existem listas no momento. Por favor, utilize o comando 'adiciona' ou 'adicionalista' para gerar uma nova lista.")
    for index, lista in enumerate(groupList):
        textoLista += "📜 Lista " + str(index+1) + ": \n"
        posCount = 1
        for name in lista:
            textoLista += str(posCount) + " - " + name + "; \n"
            posCount += 1
    
    if isGroupListLocked:
        textoLista += "\n🕒 Lista de Espera: \n"
        for name in waitList:
            textoLista += name + "; \n"

    return textoLista

# Criação, separação e exclusão de listas
def appendNewList(filas, names):
    newlist = []
    msgsLista = 'Nova lista criada! \n'
    try:
        for name in names:
            jaEstaNaLista = False
            indexLista = 0
            for index, lista in enumerate(filas.groupList):
                listLower = map(str.lower, lista)

                if name.lower() in listLower:
                    jaEstaNaLista = True
                    indexLista = index
            
            if(jaEstaNaLista):
                msgsLista += name + " já está na lista " + str(indexLista+1) + "! \n"
            else:
                newlist.append(name)
                msgsLista += name + " foi adicionado a nova lista! \n"          
        
        filas.groupList.append(newlist)

        manageListTxtFile(filas)

        return msgsLista
    except Exception as e:
        raise e

def splitList(filas, listIndex = 1):
    newlist = []
    msgLista = 'Nova lista criada! \n'
    listIndex -= 1
    try:
        newlist = filas.groupList[listIndex][(len(filas.groupList[listIndex])//2):]
        removeFromList(filas, newlist)

        filas.groupList.append(newlist)

        for name in newlist:
            msgLista += name + " foi adicionado a nova lista! \n"

        manageListTxtFile(filas)
        return msgLista
    except Exception as e:
        raise e

def removeList(filas, listIndex):
    listIndex -= 1
    try:
        if(len(filas.groupList) > 1):
            listCopy = filas.groupList[listIndex].copy()
            filas.groupList.pop(listIndex)

            addToList(filas, listCopy)

            manageDeletedListTxtFile(listIndex)
            return f'lista {listIndex + 1} foi removida. Os membros contidos nela foram movidos para outra(s) lista(s).'
        else:
            raise ExpectedException(ErrorMessages.SemListaApagavel.value)
    except ExpectedException as ee:
        raise ee
    except Exception as e:
        raise e

# Manipulação dos nomes nas listas
def addToList(filas, names):
    msgsLista = ''
    try:
        if(filas.isGroupListLocked):
            for name in names:
                jaEstaNaLista = False
                jaEstaNaListaEspera = False
                indexLista = 0
                for index, lista in enumerate(filas.groupList):
                    
                    listLower = map(str.lower, lista)

                    if name.lower() in listLower:
                        jaEstaNaLista = True
                        indexLista = index
                
                waitListLower = map(str.lower, filas.waitList)
                if name.lower() in waitListLower:
                    jaEstaNaListaEspera = True
                
                if(jaEstaNaLista):
                    msgsLista += name + " já está na lista " + str(indexLista+1) + "! \n"
                elif(jaEstaNaListaEspera):
                    msgsLista += name + " já está na lista de espera! \n"
                else:
                    filas.waitList.append(name)
                    msgsLista += name + " foi adicionado a lista de espera! \n"
        else:
            if(len(filas.groupList) < 1):
                return appendNewList(names)
            for name in names:
                countNamesList = []
                jaEstaNaLista = False
                indexLista = 0
                for index, lista in enumerate(filas.groupList):
                    listLower = map(str.lower, lista)

                    if name.lower() in listLower:
                        jaEstaNaLista = True
                        indexLista = index
                    countNamesList.append(len(lista))
                
                if(jaEstaNaLista):
                    msgsLista += name + " já está na lista " + str(indexLista+1) + "! \n"
                else:
                    filas.groupList[countNamesList.index(min(countNamesList))].append(name)
                    msgsLista += name + " foi adicionado a lista! \n" 
            
            manageListTxtFile(filas)
        return msgsLista
    except Exception as e:
        raise e

def qbgShuffleList(filas, shuffleOrReShuffle):
    try:
        if(filas.isGroupListLocked):
            toggleListStatus(filas)
        if(shuffleOrReShuffle == -1 or shuffleOrReShuffle == 0):
            for index, lista in enumerate(filas.groupList):
                newlist = [lista[shuffleOrReShuffle]]
                lista.remove(lista[shuffleOrReShuffle])

                if(len(lista) > 1):
                    random.shuffle(lista)
                
                for element in lista:
                    newlist.append(element)
                
                filas.groupList[index] = newlist.copy()
        else:
            allListNames = []
            numLists = len(filas.groupList)
            for index, lista in enumerate(filas.groupList):
                for element in lista:
                    allListNames.append(element)
            for name in allListNames:
                for lista in filas.groupList:
                    try:
                        lista.remove(name)
                    except Exception as e:
                        continue
            random.shuffle(allListNames)
            addToList(filas,allListNames)

        manageListTxtFile(filas)
        return showList(filas.groupList, filas.isGroupListLocked, filas.waitList)

    except Exception as e:
        return "Erro: " + str(e)
    
def removeFromList(filas, names):
    try:
        msgsLista = ""
        for name in names:
            # Remove o nome caso esteja preente em alguma das listas
            for lista in filas.groupList:
                try:
                    lista.remove(name)
                    msgsLista += name + " foi removido! \n"
                except Exception as e:
                    continue
            
            # Remove nome da waitList
            try:
                filas.waitList.remove(name)
                msgsLista += name + " foi removido! \n"
            except Exception as e:
                continue

        manageListTxtFile(filas)
        return msgsLista

    except Exception as e:
        return "Não foi possível remover o nome solicitado. Por favor, verifique a escrita ou o que há na lista e tente novamente."

def movePositionFromList(filas, positions):
    try:
        if(len(positions) != 2 and len(positions) != 4):
            raise ExpectedException("O número de argumentos está fora do formato. Informe 2 argumentos (apenas as posições para mexer na primeira lista) ou 4 argumentos (para mover posições de outras listas ou entre listas).")
        for index, number in enumerate(positions):
            positions[index] = int(number)
        for index,number in enumerate(positions):
            positions[index] = number -1
        if(len(positions) == 2):
            movedName = filas.groupList[0][positions[0]]
            filas.groupList[0].remove(movedName)
            filas.groupList[0] = filas.groupList[0][0:positions[1]] + [movedName] + filas.groupList[0][positions[1]:]
        elif(len(positions) == 4):
            movedName = filas.groupList[positions[0]][positions[1]]
            filas.groupList[positions[0]].remove(movedName)
            filas.groupList[positions[2]] = filas.groupList[positions[2]][0:positions[3]] + [movedName] + filas.groupList[positions[2]][positions[3]:]

        manageListTxtFile(filas)
        return showList(filas.groupList, filas.isGroupListLocked, filas.waitList)

    except ExpectedException as ee:
        raise ee
    except Exception as e:
        raise e

def swapPositionFromList(filas, positions):
    try:
        if(len(positions) != 2 and len(positions) != 4):
            raise ExpectedException("O número de argumentos está fora do formato. Informe 2 argumentos (apenas as posições para mexer na primeira lista) ou 4 argumentos (para mover posições de outras listas ou entre listas).")
        for index, number in enumerate(positions):
            positions[index] = int(number)
        for index,number in enumerate(positions):
            positions[index] = number -1
        if(len(positions) == 2):
            filas.groupList[0][positions[0]], filas.groupList[0][positions[1]] = filas.groupList[0][positions[1]], filas.groupList[0][positions[0]]
        elif(len(positions) == 4):
            filas.groupList[positions[0]][positions[1]], filas.groupList[positions[2]][positions[3]] = filas.groupList[positions[2]][positions[3]], filas.groupList[positions[0]][positions[1]]

        manageListTxtFile(filas)
        return showList(filas.groupList, filas.isGroupListLocked, filas.waitList)
    except ExpectedException as ee:
        raise ee
    except Exception as e:
        raise e

# Criação de arquivo com a lista
def manageListTxtFile(filas):
    for index, lista in enumerate(filas.groupList):
        textoLista = ''
        textoLista += "Lista " + str(index+1) + ": \n"
        posCount = 1
        for name in lista:
            textoLista += str(posCount) + " - " + name + "; \n"
            posCount += 1
        with open('listOBS' + str(index+1) + '.txt', 'w', encoding="utf-8") as file:
            file.write(textoLista)

def manageDeletedListTxtFile(removedIndex):
    with open('listOBS' + str(removedIndex+1) + '.txt', 'w', encoding="utf-8") as file:
        file.write(' ')
