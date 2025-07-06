import unittest
import commands

from constantes import numeros
from classes.jogador import Jogador
from classes.filasMantenedor import FilasMantenedor
from classes.mockGenerator import generate_mock_jogador, generate_mock_filas_mantenedor

class TestCommands(unittest.TestCase):
    def test_add(self):
        mockFila = generate_mock_filas_mantenedor(1, 5, 0)
        newPlayers = [generate_mock_jogador(), generate_mock_jogador()]

        result = commands.addUsersToList(mockFila, newPlayers)

        self.assertIn(newPlayers[0], mockFila.groupList[0])
        self.assertIn(newPlayers[1], mockFila.groupList[0])

    def test_remove(self):
        mockFila = generate_mock_filas_mantenedor(1, 10, 0)
        removePlayer = [mockFila.groupList[0][2]]

        result = commands.removeFromList(mockFila, removePlayer)

        self.assertIsNot(removePlayer[0], mockFila.groupList[0])

    def test_movePosition(self):
        mockFila = generate_mock_filas_mantenedor(1, 10, 0)
        GroupListAnterior = mockFila.groupList[0].copy()
        
        commands.movePositionFromList(mockFila, [1, 2])

        MoveuParaSegundoLugar = mockFila.groupList[0][1].nome == GroupListAnterior[0].nome
        self.assertTrue(MoveuParaSegundoLugar)

    def test_swapPosition(self):
        mockFila = generate_mock_filas_mantenedor(1, 10, 0)
        GroupListAnterior = mockFila.groupList[0].copy()

        commands.swapPositionFromList(mockFila, [1, 4])

        TrocouInicioComFim = mockFila.groupList[0][3].nome == GroupListAnterior[0].nome and mockFila.groupList[0][0].nome == GroupListAnterior[3].nome
        self.assertTrue(TrocouInicioComFim)

    def test_toggleIsGroupListLocked_AddPlayersWaiting(self):
        mockFila = generate_mock_filas_mantenedor(2, 20, 0)
        UsersInputAddWaitlistMock = [generate_mock_jogador(), generate_mock_jogador(), generate_mock_jogador()]

        commands.toggleIsGroupListLocked(mockFila)
        self.assertTrue(mockFila.isGroupListLocked)

        commands.addUsersToList(mockFila, UsersInputAddWaitlistMock)

        commands.toggleIsGroupListLocked(mockFila)
        self.assertFalse(mockFila.isGroupListLocked)

        for jogador in UsersInputAddWaitlistMock:
            self.assertTrue(
                jogador in mockFila.groupList[0] or 
                jogador in mockFila.groupList[1]
            )

    def test_separateList_OddNumberMembers(self):
        membersNumber = 11
        mockSeparableList = []
        for _ in range(membersNumber):
            mockSeparableList.append(generate_mock_jogador())
        filaMock = FilasMantenedor()
        filaMock.groupList[0] = mockSeparableList.copy()

        result = commands.splitList(filaMock)

        self.assertTrue(len(filaMock.groupList[0]) + len(filaMock.groupList[1]) == membersNumber)

    def test_shuffle_sameNumberOfPlayersAfterShuffle(self):
        mockFila = generate_mock_filas_mantenedor(2, 50, 0)
        sumMembers = len(mockFila.groupList[0]) + len(mockFila.groupList[1])

        commands.qbgShuffleList(mockFila, numeros.DEFAULT_SHUFFLE)

        sumMembersAfterShuffle = len(mockFila.groupList[0]) + len(mockFila.groupList[1])
        self.assertEqual(sumMembers, sumMembersAfterShuffle) 

    def test_shuffle_IsGroupListLocked_withPlayersInWaiting_sameNumberOfPlayersAfterShuffle(self):
        mockFila = generate_mock_filas_mantenedor(2, 50, 5, True)
        sumMembers = len(mockFila.groupList[0]) + len(mockFila.groupList[1]) + len(mockFila.waitList)

        commands.qbgShuffleList(mockFila, numeros.DEFAULT_SHUFFLE)

        sumMembersAfterShuffle = len(mockFila.groupList[0]) + len(mockFila.groupList[1]) + len(mockFila.waitList)
        self.assertEqual(sumMembers, sumMembersAfterShuffle) 
        

if __name__ == '__main__':
    unittest.main()