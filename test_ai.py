#!/usr/bin/env python3
"""Simple test to verify the improved AI works correctly"""

import sys
import os

# Mock the names module
class MockNames:
    @staticmethod
    def get_first_name():
        return "TestAI"

sys.modules['names'] = MockNames()

# Mock GameBoard module functions
class MockGameBoard:
    @staticmethod
    def transpose(matrix):
        """Transpose matrix"""
        if not matrix:
            return []
        rows = len(matrix)
        columns = len(matrix[0])
        matrix_t = []
        for j in range(columns):
            row = []
            for i in range(rows):
                row.append(matrix[i][j])
            matrix_t.append(row)
        return matrix_t

    @staticmethod
    def diagonals(matrix):
        """Get diagonals"""
        if not matrix:
            return []
        h, w = len(matrix), len(matrix[0])
        return [[matrix[h - p + q - 1][q]
                 for q in range(max(p - h + 1, 0), min(p + 1, w))]
                for p in range(h + w - 1)]

    @staticmethod
    def anti_diagonals(matrix):
        """Get anti-diagonals"""
        if not matrix:
            return []
        h, w = len(matrix), len(matrix[0])
        return [[matrix[p - q][q]
                 for q in range(max(p - h + 1, 0), min(p + 1, w))]
                for p in range(h + w - 1)]

sys.modules['user_interface.GameBoard'] = MockGameBoard

from user_interface.Players import AI

def test_ai_basic():
    """Test that AI can make a valid move on an empty board"""
    print("Testing AI on empty board...")
    board = [[' ', ' ', ' ', ' ', ' ', ' '] for _ in range(7)]
    ai = AI(turn=1)

    move = ai.get_AIMove(board)
    print(f"AI chose column: {move}")

    assert move is not None, "AI should return a move"
    assert 0 <= move < 7, f"Move should be between 0 and 6, got {move}"
    print("✓ AI makes valid move on empty board")

def test_ai_win_detection():
    """Test that AI detects and takes a winning move"""
    print("\nTesting AI win detection...")
    # Create a board where AI (player 1) can win in column 3
    board = [[' ', ' ', ' ', ' ', ' ', ' '] for _ in range(7)]
    # Set up three in a row vertically in column 3
    board[3][0] = 'p1'
    board[3][1] = 'p1'
    board[3][2] = 'p1'

    ai = AI(turn=1)
    move = ai.get_AIMove(board)
    print(f"AI chose column: {move}")

    # AI should choose column 3 to win
    assert move == 3, f"AI should choose winning move (column 3), but chose {move}"
    print("✓ AI detects and takes winning move")

def test_ai_block_opponent():
    """Test that AI blocks opponent's winning move"""
    print("\nTesting AI blocking opponent...")
    # Create a board where opponent (player 2) can win in column 2
    board = [[' ', ' ', ' ', ' ', ' ', ' '] for _ in range(7)]
    board[2][0] = 'p2'
    board[2][1] = 'p2'
    board[2][2] = 'p2'

    ai = AI(turn=1)
    move = ai.get_AIMove(board)
    print(f"AI chose column: {move}")

    # AI should block by playing in column 2
    assert move == 2, f"AI should block opponent's win (column 2), but chose {move}"
    print("✓ AI blocks opponent's winning move")

def test_ai_center_preference():
    """Test that AI prefers center columns when all else is equal"""
    print("\nTesting AI center column preference...")
    board = [[' ', ' ', ' ', ' ', ' ', ' '] for _ in range(7)]
    ai = AI(turn=1)

    # Make several moves to see if center is preferred
    moves = []
    for _ in range(5):
        move = ai.get_AIMove(board)
        moves.append(move)

    print(f"First 5 moves: {moves}")
    # First move should be center (column 3) since board is empty
    assert moves[0] == 3, f"First move should be center column (3), but got {moves[0]}"
    print("✓ AI prefers center column on empty board")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Improved Connect Four AI")
    print("=" * 60)

    try:
        test_ai_basic()
        test_ai_win_detection()
        test_ai_block_opponent()
        test_ai_center_preference()

        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
