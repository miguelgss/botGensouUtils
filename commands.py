import random
from errors import ExpectedException
from enums import ErrorMessages, StatusLista
from classes.jogador import Jogador

def toggleIsGroupListLocked(filas):
    filas.isGroupListLocked = not filas.isGroupListLocked
    if (not filas.isGroupListLocked):
        filas.waitList
        addUsersToList(filas, filas.waitList)
        filas.waitList = []
    return StatusLista.Bloqueada if filas.isGroupListLocked else StatusLista.Desbloqueada

def toggleAreListsLooping(filas):
    filas.areListsLooping = not filas.areListsLooping
    return StatusLista.Loopando if filas.areListsLooping else StatusLista.SemLoop

def showList(filas) -> str:
    textoLista = StatusLista.Bloqueada + "\n\n" if filas.isGroupListLocked else ''
    textoLista += StatusLista.Loopando + "\n\n" if filas.areListsLooping else ''
    if(len(filas.groupList) < 1):
        raise ExpectedException("Não existem listas no momento. Por favor, utilize o comando 'adiciona' ou 'adicionalista' para gerar uma nova lista.")
    for index, lista in enumerate(filas.groupList):
        textoLista += "📜 Lista " + str(index+1) + ": \n"
        posCount = 1
        for jogador in lista:
            if jogador.lutando:
                textoLista += "**_" +str(posCount) + " -<@" + str(jogador.idJogador) + ">_**" + " 🥊 **LUTANDO!**" + "\n"
            else:
                textoLista += str(posCount) + " - <@" + str(jogador.idJogador) + ">" + "; \n"
            posCount += 1
    
    if filas.isGroupListLocked:
        textoLista += "\n🕒 Lista de Espera: \n"
        for jogador in filas.waitList:
            textoLista += jogador.nome + "; \n"

    return textoLista

# Iniciação e atualização de estado da lista (quem está jogando no momento)
def advanceListStatus(filas, ctx):
    msgRetorno = ""
    try:
        ctxAuthorEqualsPlayerFighting = False
        for index, lista in enumerate(filas.groupList):
            for i, jogador in enumerate(lista):
                if(jogador.lutando and (jogador.idJogador == ctx.author.id or jogador.nome == ctx.author.name)):
                    ctxAuthorEqualsPlayerFighting = True

                    if(lista[len(lista)-1].lutando and lista[0].lutando):
                        stopList(filas, index)
                        msgRetorno += f"Partidas da Lista {index+1} finalizadas. \n"
                    elif(lista.index(jogador) == 0):
                        lista[i].lutando = False
                        if(len(lista) > 2):
                            lista[i+2].lutando = True
                        else:
                            stopList(filas, index)
                            msgRetorno += f"Partidas da Lista {index+1} finalizadas. \n"
                    elif(lista.index(jogador) == (len(lista)-1) or (lista.index(jogador)+1 == (len(lista)-1) and lista[i+1].lutando)):
                        if(filas.areListsLooping):
                            lista[i].lutando = False
                            lista[0].lutando = True
                        else:
                            stopList(filas, index)
                            msgRetorno += f"Partidas da Lista {index+1} finalizadas. \n"
                    elif(lista.index(jogador) != 0 and lista[i-1].lutando == True):
                        lista[i-1].lutando = False
                        lista[i+1].lutando = True
                    elif(lista.index(jogador) > 0 and jogador.lutando and lista[i+1].lutando):
                        lista[i].lutando = False
                        lista[i+2].lutando = True
            lutandoAgora = list(filter(lambda x: x.lutando==True, lista))

            filas.groupList[index] = lista

            if(ctxAuthorEqualsPlayerFighting):
                if(len(lutandoAgora) > 0):
                    msgRetorno += f"Lista {index+1}: <@" + str(lutandoAgora[0].idJogador) + ">" + " VS " + "<@" + str(lutandoAgora[1].idJogador) + "> \n"
                else:
                    msgRetorno += f"Não há ninguém lutando na Lista {index+1}. \n"
            elif(len(lutandoAgora) > 0):
                msgRetorno += f"Lista {index+1}: Quem está lutando agora são os jogadores {lutandoAgora[0].nome} e {lutandoAgora[1].nome}. \n"
            else:
                msgRetorno += f"Não há ninguém lutando na Lista {index+1}. \n"
            
            ctxAuthorEqualsPlayerFighting = False        

        manageListTxtFile(filas)
        return msgRetorno
    except Exception as e:
        raise e

def skipListStatus(filas, index = 1):
    index -= 1
    msgRetorno = ""
    try:
        for i, jogador in enumerate(filas.groupList[index]):
            if(jogador.lutando):
                if(filas.groupList[index][len(filas.groupList[index])-1].lutando and filas.groupList[index][0].lutando):
                    stopList(filas, index)
                    msgRetorno += f"Partidas da Lista {index+1} finalizadas. \n"
                    break
                elif(filas.groupList[index].index(jogador) == 0):
                    filas.groupList[index][i].lutando = False
                    if(len(filas.groupList[index]) > 2):
                        filas.groupList[index][i+2].lutando = True
                    else:
                        stopList(filas, index)
                        msgRetorno += f"Partidas da filas.groupList[index] {index+1} finalizadas. \n"
                    break
                elif(filas.groupList[index].index(jogador) == (len(filas.groupList[index])-1) or (filas.groupList[index].index(jogador)+1 == (len(filas.groupList[index])-1) and filas.groupList[index][i+1].lutando)):
                    if(filas.areListsLooping):
                            filas.groupList[index][i].lutando = False
                            filas.groupList[index][0].lutando = True
                    else:
                        stopList(filas, index)
                        msgRetorno += f"Partidas da Lista {index+1} finalizadas. \n"
                    break
                elif(filas.groupList[index].index(jogador) != 0 and filas.groupList[index][i-1].lutando == True):
                    filas.groupList[index][i-1].lutando = False
                    filas.groupList[index][i+1].lutando = True
                    break
                elif(filas.groupList[index].index(jogador) > 0 and jogador.lutando and filas.groupList[index][i+1].lutando):
                    filas.groupList[index][i].lutando = False
                    filas.groupList[index][i+2].lutando = True
                    break
        lutandoAgora = list(filter(lambda x: x.lutando==True, filas.groupList[index]))

        manageListTxtFile(filas)
        if(len(lutandoAgora) > 0):
            msgRetorno += f"Lista {index+1}:" + "<@" + str(lutandoAgora[0].idJogador) + ">" + " VS " + "<@" + str(lutandoAgora[1].idJogador) + "> \n"
        else:
            msgRetorno += f"Não há ninguém lutando na Lista {index+1}. \n"
        
        return msgRetorno
    except Exception as e:
        raise e

def togglePlayerStatus(filas, users):
    msgsLista = ''
    try:
        for user in users:
            jogador = user if isinstance(user, Jogador) else Jogador(user.id, user.name)

            countNamesList = []
            jaEstaNaLista = False
            indexLista = 0
            for index, lista in enumerate(filas.groupList):
                if jogador in lista:
                    lista[lista.index(jogador)].lutando = not lista[lista.index(jogador)].lutando
                    msgsLista += f"{jogador.nome} agora está lutando!" if lista[lista.index(jogador)].lutando else f"{jogador.nome} não está lutando mais!"   

        manageListTxtFile(filas)
        return msgsLista 
    except Exception as e:
        raise e

def startList(filas, indexFila = 0):
    indexFila -= 1
    msgRetorno = ""
    try:
        if(indexFila < 0):
            stopAllList(filas)
            for index, lista in enumerate(filas.groupList):
                if(len(lista) < 2):
                    msgRetorno += ErrorMessages.SemJogadoresSuficientes(index+1) + "\n"
                elif(any(list(filter(lambda x: x.lutando==True, lista)))):
                    msgRetorno += ErrorMessages.ListaJaIniciada(index+1) + "\n"
                else:
                    filas.groupList[index][0].lutando = True
                    filas.groupList[index][1].lutando = True
                    msgRetorno += "<@" + str(filas.groupList[index][0].idJogador) + ">" + " VS " + "<@" + str(filas.groupList[index][1].idJogador) + "> \n"
        else:
            stopList(filas, indexFila)
            if(len(filas.groupList[indexFila]) < 2):
                msgRetorno += ErrorMessages.SemJogadoresSuficientes(index+1) + "\n"
            elif(any(list(filter(lambda x: x.lutando==True, filas.groupList[indexFila])))):
                msgRetorno += ErrorMessages.ListaJaIniciada(index+1) + "\n"
            else:
                filas.groupList[indexFila][0].lutando = True
                filas.groupList[indexFila][1].lutando = True
                msgRetorno += "<@" + str(filas.groupList[indexFila][0].idJogador) + ">" + " VS " + "<@" + str(filas.groupList[indexFila][1].idJogador) + "> \n"
                
        manageListTxtFile(filas)
        return msgRetorno
    except Exception as e:
        raise e

def stopAllList(filas):
    try:
        for index, lista in enumerate(filas.groupList):
            for i, jogador in enumerate(lista):
                lista[i].lutando = False

            filas.groupList[index] = lista
        manageListTxtFile(filas)
        return "Todas as listas foram paradas."

    except Exception as e:
        raise e

def stopList(filas, index):
    try:
        for i, jogador in enumerate(filas.groupList[index]):
            filas.groupList[index][i].lutando = False

            filas.groupList[index] = filas.groupList[index]
        manageListTxtFile(filas)
    except Exception as e:
        raise e

# Criação, separação e exclusão de listas

def appendNewList(filas, users):
    newlist = []
    msgsLista = 'Nova lista criada! \n'
    try:
        for user in users:
            jogador = user if isinstance(user, Jogador) else Jogador(user.id, user.name)

            jaEstaNaLista = False
            indexLista = 0
            for index, lista in enumerate(filas.groupList):

                if jogador in lista:
                    jaEstaNaLista = True
                    indexLista = index
            
            if(jaEstaNaLista):
                msgsLista += jogador.nome + " já está na lista " + str(indexLista+1) + "! \n"
            else:
                newlist.append(jogador)
                msgsLista += jogador.nome + " foi adicionado a nova lista! \n"          
        
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
        if(filas.isGroupListLocked):
            toggleIsGroupListLocked(filas)

        newlist = filas.groupList[listIndex][(len(filas.groupList[listIndex])//2):]
        removeFromList(filas, newlist)

        filas.groupList.append(newlist)

        for jogador in newlist:
            msgLista += jogador.nome + " foi adicionado a nova lista! \n"

        manageListTxtFile(filas)
        return msgLista
    except Exception as e:
        raise e

def removeList(filas, listIndex):
    listIndex -= 1
    msgReturn = ""
    try:
        manageDeletedListTxtFile(listIndex)
        msgReturn += "O arquivo da lista selecionada foi limpado; \n"
        try:
            listCopy = filas.groupList[listIndex].copy()
            filas.groupList.pop(listIndex)

            addUsersToList(filas, listCopy)
            msgReturn += f'lista {listIndex + 1} foi removida. Os membros contidos nela foram movidos para outra(s) lista(s).'
        except IndexError as ie:
            msgReturn += "A lista especificada não existe no momento."

        return msgReturn
    except IndexError as ie:
        raise "Não foi possível remover o nome solicitado. Por favor, verifique a escrita ou o que há na lista e tente novamente."
    except Exception as e:
        raise e

# Manipulação dos nomes nas listas

def addUsersToList(filas, users):
    msgsLista = ''
    try:
        if(filas.isGroupListLocked):
            for user in users:
                jogador = user if isinstance(user, Jogador) else Jogador(user.id, user.name)

                jaEstaNaLista = False
                jaEstaNaListaEspera = False
                indexLista = 0
                for index, lista in enumerate(filas.groupList):

                    if jogador in lista:
                        jaEstaNaLista = True
                        indexLista = index
                
                if jogador in filas.waitList:
                    jaEstaNaListaEspera = True
                
                if(jaEstaNaLista):
                    msgsLista += jogador.nome + " já está na lista " + str(indexLista+1) + "! \n"
                elif(jaEstaNaListaEspera):
                    msgsLista += jogador.nome + " já está na lista de espera! \n"
                else:
                    filas.waitList.append(jogador)
                    msgsLista += jogador.nome + " foi adicionado a lista de espera! \n"
        else:
            if(len(filas.groupList) < 1):
                return appendNewList(users)
            for user in users:
                jogador = user if isinstance(user, Jogador) else Jogador(user.id, user.name)

                countNamesList = []
                jaEstaNaLista = False
                indexLista = 0
                for index, lista in enumerate(filas.groupList):

                    if jogador in lista:
                        jaEstaNaLista = True
                        indexLista = index
                    countNamesList.append(len(lista))
                
                if(jaEstaNaLista):
                    msgsLista += jogador.nome + " já está na lista " + str(indexLista+1) + "! \n"
                else:
                    jogador.posicao = min(countNamesList)+1
                    jogador.lista = countNamesList.index(min(countNamesList))+1
                    filas.groupList[countNamesList.index(min(countNamesList))].append(jogador)
                    msgsLista += jogador.nome + " foi adicionado a lista! \n" 
            
            manageListTxtFile(filas)
        return msgsLista
    except Exception as e:
        raise e

def qbgShuffleList(filas, shuffleOrReShuffle):
    try:
        listPlayersOnTop = []
        if(shuffleOrReShuffle == -1 or shuffleOrReShuffle == 0):
            for index, lista in enumerate(filas.groupList):
                listPlayersOnTop.append(lista[shuffleOrReShuffle])
                filas.groupList[index].remove(lista[shuffleOrReShuffle])
        
        allListPlayers = []
        numLists = len(filas.groupList)
        for index, lista in enumerate(filas.groupList):
            for element in lista:
                allListPlayers.append(element)
        for name in allListPlayers:
            for lista in filas.groupList:
                try:
                    lista.remove(name)
                except Exception as e:
                    continue
        random.shuffle(allListPlayers)
        addUsersToList(filas, listPlayersOnTop)
        addUsersToList(filas,allListPlayers)

        if(filas.isGroupListLocked):
            toggleIsGroupListLocked(filas)

        manageListTxtFile(filas)
        return showList(filas)

    except Exception as e:
        raise e
    
def removeFromList(filas, users):
    try:
        msgsLista = ""
        for user in users:
            jogador = user if isinstance(user, Jogador) else Jogador(user.id, user.name)

            # Remove o nome caso esteja preente em alguma das listas
            for index, lista in enumerate(filas.groupList):
                try:
                    if(lista[lista.index(jogador)].lutando):
                        msgsLista += f"# ⚠️ <@{jogador.idJogador}> \n ## NÃO PODE SAIR POIS AINDA ESTÁ LUTANDO! \n ## CAN'T LEAVE BECAUSE YOU'RE STILL FIGHTING!"
                        continue
                    lista.remove(jogador)
                    msgsLista += jogador.nome + " foi removido! \n"
                except Exception as e:
                    continue
            
            # Remove nome da waitList
            try:
                filas.waitList.remove(jogador)
                msgsLista += jogador.nome + " foi removido! \n"
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
        return showList(filas)

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
        return showList(filas)
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
        for jogador in lista:
            if(jogador.lutando):
                textoLista += "*" + str(posCount) + " - " + jogador.nome + "; \n"
            else:
                textoLista += str(posCount) + " - " + jogador.nome + "; \n"
            posCount += 1
        with open('listOBS' + str(index+1) + '.txt', 'w', encoding="utf-8") as file:
            file.write(textoLista)
    
    manageBackupTxtFile(filas)

def manageBackupTxtFile(filas):
    textoBackup = ''
    for index, lista in enumerate(filas.groupList):
        textoBackup += f"Membros lista {index+1}: "
        for jogador in lista:
            textoBackup += f"{jogador.nome} "
        lutandoAgora = list(filter(lambda x: x.lutando==True, lista))
        if(len(lutandoAgora) > 0):
            textoBackup += f"\nEstavam lutando na lista {index+1}: "
            for jogador in lutandoAgora:
                textoBackup += f"{jogador.nome} "

        textoBackup += "\n\n"

    with open('backup.txt', 'w', encoding="utf-8") as file:
        file.write(textoBackup)

def manageDeletedListTxtFile(removedIndex):
    with open('listOBS' + str(removedIndex+1) + '.txt', 'w', encoding="utf-8") as file:
        file.write(' ')
