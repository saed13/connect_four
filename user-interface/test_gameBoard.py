import unittest
from io import StringIO
from unittest.mock import patch
from GameBoard import *


class TestConnect4(unittest.TestCase):

    def runTest(self, given_answer, expected_out):
        with patch('builtins.input', return_value=given_answer), patch('sys.stdout', new=StringIO()) as fake_out:
            answer()
            self.assertEqual(fake_out.getvalue().strip(), expected_out)

    def test_startGame(self):
        pass

    def test_askInput(self):
        self.assertAlmostEqual(GameBoard.askInput())

    def test_check(self):
        self.assertEqual(GameBoard.check(GameBoard, 2), "2")
        self.assertEqual(GameBoard.check(GameBoard, 6), "6")
        self.assertEqual(GameBoard.check(GameBoard, 5), "5")
        # self.assertEqual(GameBoard.check(GameBoard, 23), input())
        # self.assertEqual(GameBoard.check(GameBoard, "a"), input())

    def test_addToken(self):
        gameBoard1 = GameBoard()
        gameBoard2 = GameBoard()
        test_board1 = "[[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', 'X'], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]"
        test_board2 = "[[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', 'X'], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]"
        self.assertEqual(gameBoard1.addToken(2), test_board1)
        self.assertEqual(gameBoard2.addToken(3), test_board2)

    def test_transpose(self):
        pass

    def test_toString(self):
        pass
