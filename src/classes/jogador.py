class Jogador():
    idJogador = None
    nome = ""
    posicao = 0
    lista = 0
    lutando = False

    def __init__(self, nome):
        self.nome = nome

    def __init__(self, idJogador, nome):
        self.idJogador = idJogador
        self.nome = nome

    def __eq__(self, other):
        if self.idJogador == other.idJogador \
        or self.nome == other.nome:
            return True
        else:
            return False