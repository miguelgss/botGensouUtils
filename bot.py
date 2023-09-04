# Importação de bibliotecas
import discord
import re
from discord.ext import commands
import requests

# Importação de arquivos
from responses import responses
from enums import Color, ErrorMessages, CommandNames
from errors import ExpectedException

intents =  discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='{', intents=intents)
bot.remove_command("help")

versaoAtual = 220;

def run_discord_bot():

    roles = getValidRoles() 

    TOKEN = ''
    with open('config.txt') as f:
        for line in f:
            if re.search("token", line):
                TOKEN = line.split(' ')[2]

    @bot.event
    async def on_ready():
        try:
            response = requests.get("https://api.github.com/repos/miguelgss/botGensouUtils/tags")
            jsonConversion = response.json()
            versaoLatest = jsonConversion[0]['name'].replace('v','')
            versaoLatest = versaoLatest.replace('.','')
            if(versaoAtual < int(versaoLatest)):
                print(f"Nova versão (v{versaoLatest}) disponível! Acesse https://github.com/miguelgss/botGensouUtils/releases para baixar.")

        except Exception as e:
            print(str(e))

        print(f'Versão atual: v{versaoAtual}')            
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
            description=responses.showListFormatted(),
            color=Color.Sucesso.value)
        )
            
    @bot.command(aliases=CommandNames.Adicioname)
    async def AdicionaMe(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Adicioname[0]}",
            description=responses.addAuthorToList(ctx),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Removeme)
    async def RemoveMe(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Removeme[0]}",
            description=responses.removeAuthorFromList(ctx),
            color=Color.Sucesso.value)
        )

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.default)
    @bot.command(aliases=CommandNames.BonsJogos)
    async def BonsJogos(ctx):
        await ctx.send(
            responses.goodGames(ctx)
        )
    ### ---

    ### --- COMANDOS COM PERMISSIONAMENTO
    @bot.command(aliases=CommandNames.Bloquear)
    @commands.has_any_role(*roles)
    async def BloquearDesbloquear(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Bloquear[0]}",
            description=responses.lockUnlockGroupList(),
            color=Color.Sucesso.value)
        )
        
    @bot.command(aliases=CommandNames.Adiciona)
    @commands.has_any_role(*roles)
    async def Adiciona(ctx, *users: discord.Member):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Adiciona[0]}",
            description=responses.addNamesToList(ctx, users),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.AdicionaLista)
    @commands.has_any_role(*roles)
    async def AdicionaLista(ctx, *users: discord.Member):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.AdicionaLista[0]}",
            description=responses.addNewList(ctx, users),
            color=Color.Sucesso.value)
        )
        
    @bot.command(aliases=CommandNames.Remove)
    @commands.has_any_role(*roles)
    async def Remove(ctx, *users: discord.Member):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Remove[0]}",
            description=responses.removeNamesFromList(ctx, users),
            color=Color.Sucesso.value)
        )
        
    @bot.command(aliases=CommandNames.RemoveLista)
    @commands.has_any_role(*roles)
    async def RemoveLista(ctx, number):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.RemoveLista[0]}",
            description=responses.removeList(number),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Embaralha)
    @commands.has_any_role(*roles)
    async def Embaralha(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Embaralha[0]}",
            description=responses.defaultShuffle(),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Reembaralha)
    @commands.has_any_role(*roles)
    async def Reembaralha(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Reembaralha[0]}",
            description=responses.reShuffle(),
            color=Color.Sucesso.value)
        )
        
    @bot.command(aliases=CommandNames.EmbaralhaTodos)
    @commands.has_any_role(*roles)
    async def EmbaralhaTodos(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.EmbaralhaTodos[0]}",
            description=responses.shuffleEverything(),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Separar)
    @commands.has_any_role(*roles)
    async def Separar(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Separar[0]}",
            description=responses.splitList(ctx),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Move)
    @commands.has_any_role(*roles)
    async def Move(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Move[0]}",
            description=responses.movePosition(ctx),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.Trocar)
    @commands.has_any_role(*roles)
    async def Trocar(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Trocar[0]}",
            description=responses.swapPosition(ctx),
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

    @bot.command(aliases=CommandNames.IniciarLista)
    @commands.has_any_role(*roles)
    async def IniciarLista(ctx):
        await ctx.send(
            responses.startList()
            )

    @bot.command(aliases=CommandNames.PararLista)
    @commands.has_any_role(*roles)
    async def PararLista(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.PararLista[0]}",
            description=responses.stopList(),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.AvancarLista)
    @commands.has_any_role(*roles)
    async def AvancarLista(ctx, number = 1):
        await ctx.send(
            responses.skipMatch(number)
        )
    ###---

    ###--- HANDLER DE ERROS 
    @bot.event
    async def on_command_error(ctx, error):
        print(error)
        if isinstance(error, commands.errors.MissingAnyRole):
            await ctx.send(
                embed=discord.Embed(title="Alerta:",
                description=f'De: {ctx.message.author}; Comando: {ctx.message.content}; \n\n' + ErrorMessages.SemPermissao.value,
                color=Color.Alerta.value)
            )
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send(
                embed=discord.Embed(title="Alerta:",
                description=f'De: {ctx.message.author}; Comando: {ctx.message.content}; \n\n' + ErrorMessages.ComandoNaoEncontrado.value,
                color=Color.Alerta.value)
            )
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send(
                embed=discord.Embed(title="Alerta:",
                description=f'De: {ctx.message.author}; Comando: {ctx.message.content}; \n\n' + ErrorMessages.UsuarioNaoEncontrado.value,
                color=Color.Alerta.value)
            )
        else:
            await ctx.send(
                embed=discord.Embed(title="Erro:",
                description=f'De: {ctx.message.author.name}; Comando: {ctx.message.content}; \n\n' + str(error),
                color=Color.Erro.value)
            )
        print(str(error)) 

    # Inicia o bot
    bot.run(TOKEN)

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

def checkRoles(userRoles, validRoles) -> bool:
    if(len(validRoles) == 0):
        return True
    for user in userRoles:
        for valid in validRoles:
            if(re.search(str(user).lower(),str(valid).lower())):
                return True
    return False

###---