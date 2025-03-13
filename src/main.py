import asyncio
import threading
import bot
import playerGui
from classes.filasMantenedor import FilasMantenedor
from requestsFila import RequestsFila

from classes.jogador import Jogador

Filas = FilasMantenedor()
reqs = RequestsFila(Filas)

ListaJogadoresSeparavel = [
    Jogador("AliceSilva", "Alice Silva"),
    Jogador("Buruno", "Bruno Santos"),
    Jogador("Carola", "Carolina Oliveira"),
    Jogador("Danizinha", "Daniel Souza"),
    Jogador("Duda", "Eduarda Lima"),
    Jogador("Felps", "Felipe Costa"),
    Jogador("Gabys", "Gabriela Rocha"),
    Jogador("Henriqs", "Henrique Mendes"),
    Jogador("Izzys", "Isabela Fernandes"),
    Jogador("Jonas", "João Pereira"),
    Jogador("Karolina", "Karina Alves"),
]

reqs.addNamesToList(None, ListaJogadoresSeparavel)

def run_bot(loop):
    asyncio.run_coroutine_threadsafe(bot.run_discord_bot(reqs), loop)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    
    bot_thread = threading.Thread(target=loop.run_forever)
    bot_thread.start()
    
    run_bot(loop)
    
    ui = playerGui.PlayerManagerGUI(Filas)
    ui.run()
    
    loop.call_soon_threadsafe(loop.stop)
    bot_thread.join()
