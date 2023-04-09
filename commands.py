import random

list = []
segundaList = []

def showList() -> str:
    textoLista = "LISTA 1: \n"

    posCount = 1
    for name in list:
        textoLista += str(posCount) + " - " + name + "; \n"
        posCount += 1

    if (len(segundaList) > 0):
        textoLista += "LISTA 2: \n"
        for name in segundaList:
            textoLista += name + "; \n"

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
        print(newlist)

        if(len(list) > 1):
            random.shuffle(list)
        
        for element in list:
            newlist.append(element)
        
        list = newlist.copy()

        if (len(segundaList) > 0):
            newlist2 = [segundaList[shuffleOrReShuffle]]
            list.remove(segundaList[shuffleOrReShuffle])

            if(len(segundaList) > 1):
                random.shuffle(segundaList)
            for element in segundaList:
                newlist2.append(element)
            segundaList = newlist2.copy()
        
        return showList()
    except Exception as e:
        return "Erro: " + str(e)


    
def removeFromList(names):
    try:
        msgsLista = ''
        for name in names:
            list.remove(name)
            if (len(segundaList) > 0):
                segundaList.remove(name)
                msgsLista += name + " foi removido!"
        return msgsLista

    except Exception as e:
        return "Não foi possível remover o nome solicitado. Por favor, verifique a escrita ou o que há na lista e tente novamente."

def splitList():
    pass
