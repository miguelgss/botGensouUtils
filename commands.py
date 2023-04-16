import random

list = []
segundaList = []

def showList() -> str:
    posCount = 1
    textoLista = ''
    for name in list:
        textoLista += str(posCount) + " - " + name + "; \n"
        posCount += 1

    # if (len(segundaList) > 0):
    #     textoLista += "LISTA 2: \n"
    #     for name in segundaList:
    #         textoLista += name + "; \n"

    return textoLista

def addToList(names):
    msgsLista = ''

    for name in names:

        listLower = map(str.lower, list)
        segundaListLower = map(str.lower, segundaList)

        if name.lower() in listLower or name in segundaListLower:
            msgsLista += name + " já está na lista! \n"
            continue

        list.append(name)
        msgsLista += name + " foi adicionado! \n"

    manageListTxtFile()
    return msgsLista

def shuffleList():
    random.shuffle(list)
    random.shuffle(segundaList)
    

def qbgShuffleList(shuffleOrReShuffle):
    global list 
    global segundaList 

    try:
        newlist = [list[shuffleOrReShuffle]]
        list.remove(list[shuffleOrReShuffle])

        if(len(list) > 1):
            random.shuffle(list)
        
        for element in list:
            newlist.append(element)
        
        list = newlist.copy()

        # if (len(segundaList) > 0):
        #     newlist2 = [segundaList[shuffleOrReShuffle]]
        #     list.remove(segundaList[shuffleOrReShuffle])

        #     if(len(segundaList) > 1):
        #         random.shuffle(segundaList)
        #     for element in segundaList:
        #         newlist2.append(element)
        #     segundaList = newlist2.copy()
        
        manageListTxtFile()
        return showList()
    except Exception as e:
        return "Erro: " + str(e)
    
def removeFromList(names):
    try:
        msgsLista = ""
        for name in names:
            list.remove(name)
            msgsLista += name + " foi removido! \n"
            if (len(segundaList) > 0):
                segundaList.remove(name)
                msgsLista += name + " foi removido! \n"

        manageListTxtFile()
        return msgsLista

    except Exception as e:
        print(e)
        return "Não foi possível remover o nome solicitado. Por favor, verifique a escrita ou o que há na lista e tente novamente."

def swapPositionFromList(pos1, pos2):
    try:
        pos1 -= 1
        pos2 -= 1
        list[pos1], list[pos2] = list[pos2], list[pos1]

        manageListTxtFile()
        return showList()
    except Exception as e:
        return e

# Criação de arquivo com a lista
def manageListTxtFile():
    with open('listOBS.txt', 'w') as file:
        file.write(showList())

