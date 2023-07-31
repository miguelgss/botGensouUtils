# Importação de bibliotecas
import discord
import re
from discord.ext import commands

# Importação de arquivos
from responses import responses
from enums import Color, ErrorMessages, CommandNames
from errors import ExpectedException

intents =  discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='{', intents=intents)
bot.remove_command("help")

def run_discord_bot():

    roles = getValidRoles() 

    TOKEN = ''
    with open('config.txt') as f:
        for line in f:
            if re.search("token", line):
                TOKEN = line.split(' ')[2]

    @bot.event
    async def on_ready():
        print(f'{bot.user} ligou e está pronto para ser utilizado!' + " Use {h para ver os comandos disponíveis.")

    ###--- COMANDOS LIVRES
    @bot.command(aliases=CommandNames.Ajuda)
    async def Ajuda(ctx):
        ajudaRetorno = "Comandos: \n"
        for text in CommandNames.ajudaList:
            ajudaRetorno += "> " + text
            ajudaRetorno += "\n"
        await ctx.send(
            embed=discord.Embed(title=CommandNames.Ajuda[0],
            description=ajudaRetorno,
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
    async def Adiciona(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Adiciona[0]}",
            description=responses.addNamesToList(ctx),
            color=Color.Sucesso.value)
        )

    @bot.command(aliases=CommandNames.AdicionaLista)
    @commands.has_any_role(*roles)
    async def AdicionaLista(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.AdicionaLista[0]}",
            description=responses.addNewList(ctx),
            color=Color.Sucesso.value)
        )
        
    @bot.command(aliases=CommandNames.Remove)
    @commands.has_any_role(*roles)
    async def Remove(ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{CommandNames.Remove[0]}",
            description=responses.removeNamesFromList(ctx),
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
    ###---

    ###--- HANDLER DE ERROS 
    @bot.event
    async def on_command_error(ctx, error):
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

###---