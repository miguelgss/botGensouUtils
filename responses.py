import re
import commands

ajudaList = [
        "**help/h** - Mostra os comandos do bot;",
        "**lista/l** - Mostra a lista atual;",
        "**adiciona/add/a** - Recebe um ou mais argumentos para adicionar alguém a lista;",
        "**adicioneMe/addme/am** - Adiciona quem mandou a mensagem para a lista;",
        "**remover/r** - Recebe um ou mais argumentos para remover alguém da lista;",
        "**removerme/rme** - Remove quem mandou a mensagem da lista;",
        "**embaralhar/e** - Move o último para a primeira posição e então embaralha a lista;",
        "**reembaralhar/re** - Reembaralha todos da lista exceto o primeiro;"
        ]

def handle_response(messageObj, message) -> str:
    # Remove espaços extras
    txt_command = re.sub(' +', ' ', message[1:])
    txt_splitted = txt_command.split(' ')
    txt_splitted[0] = txt_splitted[0].lower()
    prefix = message[0]

    if prefix == '{':

        if txt_splitted[0] == 'lista' or txt_splitted[0] == 'l':
            return commands.showList()

        if txt_splitted[0] == 'adiciona' or txt_splitted[0] == 'add' or txt_splitted[0] == 'a':
            return commands.addToList(txt_splitted[1:])
        
        if txt_splitted[0] == 'adicioneme' or txt_splitted[0] == 'addme' or txt_splitted[0] == 'am':
            return commands.addToList( [str(messageObj.author.name)] )

        if txt_splitted[0] == 'remover' or txt_splitted[0] == 'r':
            retorno = commands.removeFromList(txt_splitted[1:])
            return retorno
        
        if txt_splitted[0] == 'removerme' or txt_splitted[0] == 'rme':
            retorno = commands.removeFromList( [str(messageObj.author.name)] )
            return retorno

        if txt_splitted[0] == 'embaralhar' or txt_splitted[0] == 'e':
            return commands.qbgShuffleList(-1)
        
        if txt_splitted[0] == 'reembaralhar' or txt_splitted[0] == 're':
            return commands.qbgShuffleList(0)

        if txt_splitted[0] == 'help' or txt_splitted[0] == 'h':
            ajudaRetorno = "Comandos: \n"
            for text in ajudaList:
                ajudaRetorno += "> " + text
                ajudaRetorno += "\n\n"
            return ajudaRetorno
    
