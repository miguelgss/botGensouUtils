# Importação de bibliotecas
import discord
import re
from discord.ext import commands
import requests
import tkinter as tk
import webbrowser
import os
from datetime import datetime

# Importação de arquivos
from requestsFila import RequestsFila
from enums import Color, ErrorMessages, CommandNames
from errors import ExpectedException

intents =  discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='{', intents=intents)
bot.remove_command("help")

v = [2, 5, 0]

def check_need_update(v1:list, v2:list):
    length = max(len(v1), len(v2))

    for i in range(length):
        if v1[i] > int(v2[i]):
            return False
        if v1[i] < int(v2[i]):
            return True
    return False

async def run_discord_bot(requestsFila: RequestsFila):

    roles = getValidRoles() 
    adminRole = getValidAdminRole()

    TOKEN = ''
    with open('config.txt') as f:
        for line in f:
            if re.search("token", line):
                TOKEN = line.split(' ')[2]

    def openBrowserWithUpdate():
        import webbrowser
        url = "https://github.com/miguelgss/botGensouUtils/releases"
        webbrowser.open(url, new=0, autoraise=True)
    
    @bot.event
    async def on_ready():
        try:
            response = requests.get("https://api.github.com/repos/miguelgss/botGensouUtils/tags")
            jsonConversion = response.json()
            versaoLatest = str(jsonConversion[0]['name'].replace('v',''))
            versaoLatest = versaoLatest.split(".")
            if(check_need_update(v, versaoLatest)):
                try:
                    newVersionWindow = tk.Tk()
                    newVersionWindow.title("Nova atualização disponível!")
                    newVersionWindow.geometry("400x145")
                    updateMessage = f"Nova versão (v{versaoLatest[0]}.{versaoLatest[1]}.{versaoLatest[2]}) disponível! Acesse https://github.com/miguelgss/botGensouUtils/releases para baixar."
                    updateLabel = tk.Label(
                        text=updateMessage,
                        wraplength=300
                    )
                    updateLabel.pack()

                    buttonGetUpdate = tk.Button(
                        text="Download",
                        width=10,
                        height=1,
                        fg="black",
                        bg=Color.VerdeLimaoHEX.value,
                        command=openBrowserWithUpdate
                    )

                    buttonConfirm = tk.Button(
                        text="Ignorar",
                        width=10,
                        height=1,
                        fg="black",
                        bg=Color.CinzaClaroHEX.value,
                        command=newVersionWindow.destroy
                    )

                    buttonGetUpdate.pack()
                    buttonConfirm.pack()
                    newVersionWindow.mainloop()
                except Exception as e:
                    print(str(e))

                print(updateMessage)

        except Exception as e:
            print("Ocorreu um erro ao verificar se há novas versões... \n" + str(e))

        print(f'Versão atual: v{v[0]}.{v[1]}.{v[2]}')
        print(f'{bot.user} ligou e está pronto para ser utilizado!' + " Use {h para ver os comandos disponíveis.")

    ###--- COMANDOS LIVRES
    @bot.command(aliases=CommandNames.Ajuda)
    async def Ajuda(ctx):
        ajudaList = []
        if(checkRoles(ctx.author.roles, roles)):
            ajudaList = CommandNames.ajudaBasicoList + CommandNames.ajudaList
        else:
            ajudaList = CommandNames.ajudaBasicoList
        ajudaRetorno = "Comandos: \n"
        for text in ajudaList:
            ajudaRetorno += "> " + text
            ajudaRetorno += "\n"
        await ctx.send(
            embed=discord.Embed(title=CommandNames.Ajuda[0],
            description=ajudaRetorno,
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Tutorial)
    async def Tutorial(ctx):
        await ctx.send(
            embed=discord.Embed(title=CommandNames.Tutorial[0],
            description=CommandNames.ajudaGringous[0],
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Lista)
    async def Lista(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Lista[0]}",
            description=requestsFila.showListFormatted(),
            color=Color.Sucesso.value)
        )
            
    @bot.command(aliases=CommandNames.Adicioname)
    async def AdicionaMe(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Adicioname[0]}",
            description=requestsFila.addAuthorToList(ctx),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Removeme)
    async def RemoveMe(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Removeme[0]}",
            description=requestsFila.removeAuthorFromList(ctx),
            color=Color.Sucesso.value)
        )

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.default)
    @bot.command(aliases=CommandNames.BonsJogos)
    async def BonsJogos(ctx):
        await ctx.send(
            requestsFila.goodGames(ctx)
        )
    ### ---

    ### --- COMANDOS COM PERMISSIONAMENTO
    @bot.command(aliases=CommandNames.Bloquear)
    @commands.has_any_role(*roles)
    async def BloquearDesbloquear(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Bloquear[0]}",
            description=requestsFila.lockUnlockGroupList(),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Loop)
    @commands.has_any_role(*roles)
    async def HabilitaDesabilitaLoop(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Loop[0]}",
            description=requestsFila.loopUnloopLists(),
            color=Color.Sucesso.value)
        )    
        
    @bot.command(aliases=CommandNames.Adiciona)
    @commands.has_any_role(*roles)
    async def Adiciona(ctx, *users: discord.Member):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Adiciona[0]}",
            description=requestsFila.addNamesToList(ctx, users),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.AdicionaLista)
    @commands.has_any_role(*roles)
    async def AdicionaLista(ctx, *users: discord.Member):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.AdicionaLista[0]}",
            description=requestsFila.addNewList(ctx, users),
            color=Color.Sucesso.value)
        )
        
    @bot.command(aliases=CommandNames.Remove)
    @commands.has_any_role(*roles)
    async def Remove(ctx, *users: discord.Member):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Remove[0]}",
            description=requestsFila.removeNamesFromList(ctx, users),
            color=Color.Sucesso.value)
        )
        
    @bot.command(aliases=CommandNames.RemoveLista)
    @commands.has_any_role(*roles)
    async def RemoveLista(ctx, number):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.RemoveLista[0]}",
            description=requestsFila.removeList(number),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Embaralha)
    @commands.has_any_role(*roles)
    async def Embaralha(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Embaralha[0]}",
            description=requestsFila.defaultShuffle(),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Reembaralha)
    @commands.has_any_role(*roles)
    async def Reembaralha(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Reembaralha[0]}",
            description=requestsFila.reShuffle(),
            color=Color.Sucesso.value)
        )
        
    @bot.command(aliases=CommandNames.EmbaralhaTodos)
    @commands.has_any_role(*roles)
    async def EmbaralhaTodos(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.EmbaralhaTodos[0]}",
            description=requestsFila.shuffleEverything(),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Separar)
    @commands.has_any_role(*roles)
    async def Separar(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Separar[0]}",
            description=requestsFila.splitList(ctx),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Move)
    @commands.has_any_role(*roles)
    async def Move(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Move[0]}",
            description=requestsFila.movePosition(ctx),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Trocar)
    @commands.has_any_role(*roles)
    async def Trocar(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Trocar[0]}",
            description=requestsFila.swapPosition(ctx),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Limpar)
    @commands.has_any_role(*roles)
    async def Clear(ctx, number = 20):
        messagesList = []
        number = int(number) 

        async for message in ctx.channel.history(limit=number):
            if message.author == bot.user:
                messagesList.append(message)
        await ctx.channel.delete_messages(messagesList)

    @bot.command(aliases=CommandNames.LimparTodos)
    @commands.has_any_role(*adminRole)
    async def ClearAll(ctx, number = 20):
        messagesList = []
        number = int(number) 

        async for message in ctx.channel.history(limit=number):
            messagesList.append(message)
        await ctx.channel.delete_messages(messagesList)

    @bot.command(aliases=CommandNames.IniciarLista)
    @commands.has_any_role(*roles)
    async def IniciarLista(ctx, number = 0):
        await ctx.send(
            requestsFila.startList(number)
            )

    @bot.command(aliases=CommandNames.PararLista)
    @commands.has_any_role(*roles)
    async def PararLista(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.PararLista[0]}",
            description=requestsFila.stopList(),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.AvancarLista)
    @commands.has_any_role(*roles)
    async def AvancarLista(ctx, number = 1):
        await ctx.send(
            requestsFila.skipMatch(number)
        )

    @bot.command(aliases=CommandNames.MudarEstadoJogador)
    @commands.has_any_role(*roles)
    async def MudarEstadoJogador(ctx, *users: discord.Member):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.MudarEstadoJogador[0]}",
            description=requestsFila.togglePlayerStatus(users),
            color=Color.Sucesso.value)
        )
    ###---

    ###--- HANDLER DE ERROS 
    @bot.event
    async def on_command_error(ctx, error):
        title = "⚠️ Alerta:"
        errorMessage = ""
        errorColor = Color.Alerta.value
        if isinstance(error, commands.errors.MissingAnyRole):
            errorMessage=f'De: {ctx.message.author}; Comando: {ctx.message.content}; \n\n {ErrorMessages.SemPermissao.value} \n {error} \n\n OBS: Se a lista de roles estiver vazia, favor incluir as roles e adminRole no config.txt.'

        elif isinstance(error, commands.errors.CommandNotFound):
            errorMessage=f'De: {ctx.message.author}; Comando: {ctx.message.content}; \n\n' + ErrorMessages.ComandoNaoEncontrado.value

        elif isinstance(error, commands.errors.MemberNotFound):
            errorMessage=f'De: {ctx.message.author}; Comando: {ctx.message.content}; \n\n' + ErrorMessages.UsuarioNaoEncontrado.value

        else:
            title = "🚫 Erro:"
            errorMessage = f'De: {ctx.message.author.name}; Comando: {ctx.message.content}; \n\n' + str(error)
            errorColor = Color.Erro.value
            
        await ctx.send(
            embed=discord.Embed(title=title,
            description=errorMessage,
            color=errorColor)
        )
        print(str(error)) 

        time_msg = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        log_message = (
            f"{time_msg}\\\\"
            f"{errorMessage}"
        )
        append_to_daily_log(log_message)

    ###--- Registrar log básico de comandos
    @bot.event
    async def on_command(ctx):
        command_name = ctx.command.name
        author_name = ctx.author.display_name
        guild_name = ctx.guild.name if ctx.guild else "Direct Message"
        channel_name = ctx.channel.name if ctx.channel.name else "Direct Message"

        time_msg = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        log_message = (
            f"{time_msg}\\\\"
            f"Comando '{command_name}' utilizado por '{author_name}' "
            f"em: '{guild_name}' (Channel: '{channel_name}')"
        )
        print(log_message)
        append_to_daily_log(log_message)

    # Inicia o bot
    try:
        await bot.start(TOKEN)
    except Exception as e:
        if isinstance(e, discord.errors.LoginFailure):
            print(ErrorMessages.TokenIncorreto.value + "\n" + ErrorMessages.InvalidToken.value)
        else:
            print(e)

###--- Verifica Permissões

def getValidRoles():
    listRoles = []
    retornoList = []

    with open('config.txt') as f:   
        for line in f:
            if re.search("roles", line):
                listRoles = line.split("=")
                listRoles.pop(0)
                for i in listRoles:
                    roles = i.split(',')
                    retornoList = list(map(str.strip, roles))
    
    return retornoList

def getValidAdminRole():
    listRoles = []
    retornoList = []

    with open('config.txt') as f:   
        for line in f:
            if re.search("adminRole", line):
                listRoles = line.split("=")
                listRoles.pop(0)
                for i in listRoles:
                    roles = i.split(',')
                    retornoList = list(map(str.strip, roles))
    
    return retornoList

def checkRoles(userRoles, validRoles) -> bool:
    if(len(validRoles) == 0):
        return True
    for user in userRoles:
        for valid in validRoles:
            if(re.search(str(user).lower(),str(valid).lower())):
                return True
    return False

###---

###--- Utilitário manipulação logs

def append_to_daily_log(log_message: str, log_folder: str = "log"):
    """
    Append a log message to a daily log file inside the specified log folder.
    The log file is named as YYYY-MM-DD.log based on the current date.

    Args:
        log_message (str): The message string to append to the log.
        log_folder (str): The folder where log files are saved (default "log").
    """
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_file_path = os.path.join(log_folder, f"{today_str}.log")
    
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(log_message + "\n")

###---