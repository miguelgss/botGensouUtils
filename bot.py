import discord
import re
from discord.ext import commands

import responses

intents =  discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
async def send_message(message, user_message):
    try:
        response = responses.handle_response(message, user_message)
        if(type(response) is str):
            await message.channel.send(
                embed=discord.Embed(title=user_message,
                description=response,
                color=0xFF5733)
                )
        elif(user_message[0] == '{'): await message.channel.send(
                embed=discord.Embed(title=user_message,
                description="Comando não reconhecido. Use 'h' ou 'help' para verificar os comandos disponíveis.",
                color=0xFF5733)
                )
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = ''
    with open('token.txt') as f:
        for line in f:
            if re.search("token", line):
                print(line.split(' '))
                TOKEN = line.split(' ')[2]
                
    client = discord.Client(intents = intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        await send_message(message, user_message)

    client.run(TOKEN)

