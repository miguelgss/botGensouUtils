import unittest
import commands

from classes.jogador import Jogador
from classes.filasMantenedor import FilasMantenedor

FilaMock = FilasMantenedor
JogadoresMock = [Jogador("1","Vibago"), Jogador("2","Kujibiki"), Jogador("3", "Machii"), Jogador("4", "Decarabia")]
FilasMantenedor.groupList[0] = JogadoresMock.copy()

UsersInputAddMock = [Jogador("123", "Haggen"), Jogador("456", "Nicolante")]
UsersInputAddWaitlistMock = [Jogador("900", "Lia"), Jogador("800", "Kret"), Jogador("700", "Looisin")]
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

    def test_toggleIsGroupListLocked(self):
        commands.toggleIsGroupListLocked(FilaMock)
        self.assertTrue(FilaMock.isGroupListLocked)
        commands.addUsersToList(FilaMock, UsersInputAddWaitlistMock)
        commands.toggleIsGroupListLocked(FilaMock)
        self.assertFalse(FilaMock.isGroupListLocked)

        for jogador in UsersInputAddWaitlistMock:
            self.assertIn(jogador, FilaMock.groupList[0])

if __name__ == '__main__':
    unittest.main()