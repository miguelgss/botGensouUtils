import unittest
import commands

from classes.jogador import Jogador
from classes.filasMantenedor import FilasMantenedor

FilaMock = FilasMantenedor()
JogadoresMock = [Jogador("1","Vibago"), Jogador("2","Kujibiki"), Jogador("3", "Machii"), Jogador("4", "Decarabia")]
FilaMock.groupList[0] = JogadoresMock.copy()

UsersInputAddMock = [Jogador("123", "Haggen"), Jogador("456", "Nicolante")]
UsersInputRemoveMock = [Jogador("1", "Vibago")]

class TestCommands(unittest.TestCase):
    def test_add(self):
        result = commands.addUsersToList(FilaMock, UsersInputAddMock)
        self.assertIn(UsersInputAddMock[0], FilaMock.groupList[0])
        self.assertIn(UsersInputAddMock[1], FilaMock.groupList[0])

    def test_remove(self):
        GroupListAnterior = FilaMock.groupList[0].copy()
        result = commands.removeFromList(FilaMock, UsersInputRemoveMock)
        self.assertIsNot(UsersInputRemoveMock[0], FilaMock.groupList[0])
        self.assertIsNot(FilaMock.groupList[0], GroupListAnterior)

    def test_movePosition(self):
        GroupListAnterior = FilaMock.groupList[0].copy()
        commands.movePositionFromList(FilaMock, [1, 2])
        MoveuParaSegundoLugar = FilaMock.groupList[0][1].nome == GroupListAnterior[0].nome
        self.assertTrue(MoveuParaSegundoLugar)

    def test_swapPosition(self):
        GroupListAnterior = FilaMock.groupList[0].copy()
        commands.swapPositionFromList(FilaMock, [1, 4])
        TrocouInicioComFim = FilaMock.groupList[0][3].nome == GroupListAnterior[0].nome and FilaMock.groupList[0][0].nome == GroupListAnterior[3].nome
        self.assertTrue(TrocouInicioComFim)

    def test_toggleIsGroupListLocked_AddPlayersWaiting(self):
        UsersInputAddWaitlistMock = [Jogador("900", "Lia"), Jogador("800", "Kret"), Jogador("700", "Looisin")]

        commands.toggleIsGroupListLocked(FilaMock)
        self.assertTrue(FilaMock.isGroupListLocked)

        commands.addUsersToList(FilaMock, UsersInputAddWaitlistMock)

        commands.toggleIsGroupListLocked(FilaMock)
        self.assertFalse(FilaMock.isGroupListLocked)

        for jogador in UsersInputAddWaitlistMock:
            self.assertTrue(
                jogador in FilaMock.groupList[0] or 
                jogador in FilaMock.groupList[1]
            )

    def test_separateList_OddNumberMembers(self):
        ListaJogadoresSeparavel = [
            Jogador("1", "A"),
            Jogador("2", "B"),
            Jogador("3", "C"),
            Jogador("4", "D"),
            Jogador("5", "E"),
            Jogador("6", "F"),
            Jogador("7", "G"),
            Jogador("8", "H"),
            Jogador("9", "I"),
            Jogador("10", "J"),
            Jogador("11", "K"),
            ]
        filaMock = FilasMantenedor()
        filaMock.groupList[0] = ListaJogadoresSeparavel.copy()
        commands.splitList(filaMock)

        self.assertTrue(filaMock.groupList[0] == ListaJogadoresSeparavel[0:5])
        self.assertTrue(filaMock.groupList[1] == ListaJogadoresSeparavel[5:11])

    def test_separaLista_IsGroupListLocked_AddPlayersWaitingToTop(self):
        ListaJogadoresSeparavel = [
            Jogador("1", "A"),
            Jogador("2", "B"),
            Jogador("3", "C"),
            Jogador("4", "D"),
            Jogador("5", "E"),
            Jogador("6", "F"),
            Jogador("7", "G"),
            Jogador("8", "H"),
            Jogador("9", "I"),
            Jogador("10", "J"),
            ]
        filaMock = FilasMantenedor()
        filaMock.isGroupListLocked = True
        filaMock.groupList[0] = ListaJogadoresSeparavel.copy()

        UsersInputAddWaitlistMock = [Jogador("900", "Lia"), Jogador("800", "Kret"), Jogador("700", "Looisin")]

        commands.addUsersToList(filaMock, UsersInputAddWaitlistMock)
        commands.splitList(filaMock)

        self.assertTrue(UsersInputAddWaitlistMock[0] in filaMock.groupList[0][0:3])
        self.assertTrue(UsersInputAddWaitlistMock[1] in filaMock.groupList[1][0:3])
        self.assertTrue(UsersInputAddWaitlistMock[2] in filaMock.groupList[0][0:2])

if __name__ == '__main__':
    unittest.main()