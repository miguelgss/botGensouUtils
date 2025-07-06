import random
import string
from .filasMantenedor import FilasMantenedor
from .jogador import Jogador

def generate_mock_jogador(idJogador=None, nome=None):
    """Generate a mock Jogador with optional id and name."""
    if idJogador is None:
        idJogador = random.randint(1, 999999)
    if nome is None:
        nome = ''.join(random.choices(string.ascii_letters, k=25))
    jogador = Jogador(idJogador, nome)
    jogador.lutando = False
    return jogador

def generate_mock_filas_mantenedor(num_groups=3, group_size=5, waitlist_size=4, locked=False):
    """Generate a mock FilasMantenedor with groups and waitlist filled with Jogador objects."""
    fm = FilasMantenedor()
    fm.groupList = []
    for _ in range(num_groups):
        group = [generate_mock_jogador() for _ in range(group_size)]
        fm.groupList.append(group)
    fm.waitList = [generate_mock_jogador() for _ in range(waitlist_size)]
    
    fm.isGroupListLocked = locked
    fm.areListsLooping = False
    return fm