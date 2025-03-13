import tkinter as tk
from responses import responses
from classes.jogador import Jogador

class DadosJogador:
    def __init__(self, jogador: Jogador, numeroLista: int, button: tk.Button):
        self.jogador = jogador
        self.lista = numeroLista
        self.button = button

class UIWindow:
    def __init__(self):
        self.running = False
        self.window = tk.Tk()
        self.window.title("Gerenciador das lista")
        self.window.geometry("360x640")
        self.window.configure(background='black')

        self.label = tk.Label(self.window, text="Bo um qbgs", font=("Arial", 12))
        self.label.pack(pady=5)

        self.stop_button = tk.Button(self.window, text="Encerrar", command=self.stop_loop, )
        self.stop_button.pack(pady=10)
        self.stop_button.place(relx=0.8, rely=0)

        self.players_buttons = [
            DadosJogador(Jogador(1, "Teste1"),1, tk.Button(self.window, text="Teste 1", height=1)),
            DadosJogador(Jogador(2, "Teste Lá ele"),1, tk.Button(self.window, text="Teste 89338", height=1)),
        ]

        for x in self.players_buttons:
            x.button.pack(pady=5)
        self.start_loop()

    def start_loop(self):
        if not self.running:
            self.running = True
            self.loop()

    def stop_loop(self):
        self.running = False
        self.window.quit()

    def loop(self):
        if self.running:
            #self.clearPlayers()

            self.updateAndDraw()

            self.window.after(1000, self.loop)

    def updateAndDraw(self):
        for i, lista in enumerate(getListPlayers()):
            for jogador in lista:
                newButton = tk.Button(self.window, text=jogador.nome + " Lista: " + str(i+1), height=1)
                newButton.pack(pady=2)
                self.players_buttons.append(DadosJogador(jogador, i+1, newButton))

    def clearPlayers(self):
        for p in self.players_buttons:
            p.button.destroy()
        self.players_buttons = []
        
    def run(self):
        self.window.mainloop()

def getListPlayers():
    return responses.getGroupList()
