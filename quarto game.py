import itertools
import random


class Piece:
    def __init__(self, color, shape, height, density):
        self.color = color  # 'white' or 'black'
        self.shape = shape  # 'round' or 'square'
        self.height = height  # 'tall' or 'short'
        self.density = density  # 'solid' or 'hollow'

    def __repr__(self):
        return f"{self.color} {self.shape} {self.height} {self.density}"


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(4)] for _ in range(4)]

    def place_piece(self, piece, row, col):
        if self.grid[row][col] is None:
            self.grid[row][col] = piece
            return True
        return False

    def check_quarto(self):
        lines = self.grid + list(zip(*self.grid))
        diagonals = [[self.grid[i][i] for i in range(4)], [self.grid[i][3 - i] for i in range(4)]]
        for line in lines + diagonals:
            if None not in line and self.common_characteristic(line):
                return True
        return False

    def common_characteristic(self, pieces):
        for attr in ['color', 'shape', 'height', 'density']:
            if len(set(getattr(piece, attr) for piece in pieces)) == 1:
                return True
        return False

    def is_full(self):
        return all(self.grid[row][col] is not None for row in range(4) for col in range(4))

    def display(self):
        for row in self.grid:
            print(' | '.join(str(piece) if piece else '____' for piece in row))
            print('-' * 20)


def initialize_pieces():
    combinations = list(
        itertools.product(['white', 'black'], ['round', 'square'], ['tall', 'short'], ['solid', 'hollow']))
    pieces = [Piece(*combo) for combo in combinations]
    random.shuffle(pieces)
    return pieces


def safe_input(prompt, expected_type, range=None):
    while True:
        try:
            user_input = input(prompt)
            if expected_type is int:
                user_input = int(user_input)
                if range and not (range[0] <= user_input <= range[1]):
                    raise ValueError("Input out of range.")
            elif expected_type is str:
                if range and user_input not in range:
                    raise ValueError("Input not in allowed values.")
            return user_input
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")


def select_piece(pieces, player_type="Human"):
    print("Available pieces:" if player_type == "Human" else "Computer is selecting a piece...")
    for i, piece in enumerate(pieces):
        print(f"{i + 1}: {piece}")
    if player_type == "Human":
        choice = safe_input("Select a piece to give (1-16): ", int, range=(1, len(pieces))) - 1
    else:
        choice = random.randint(0, len(pieces) - 1)
        print(f"Computer selects piece: {pieces[choice]}")
    return pieces.pop(choice)


def place_piece(board, piece, player_type="Human"):
    if player_type == "Human":
        board.display()
        while True:
            row = safe_input("Select row (1-4) to place piece: ", int, range=(1, 4)) - 1
            col = safe_input("Select column (1-4) to place piece: ", int, range=(1, 4)) - 1
            if board.place_piece(piece, row, col):
                break
            print("That space is already occupied. Please select a different space.")
    else:
        row, col = computer_places_piece(board)
        print(f"Computer placed piece at ({row + 1}, {col + 1})")
        board.place_piece(piece, row, col)


def computer_places_piece(board):
    for row in range(4):
        for col in range(4):
            if board.grid[row][col] is None:
                return row, col


def play_round(board, pieces, human_turn=True):
    while not board.is_full():
        piece = select_piece(pieces, "Human" if human_turn else "Computer")
        place_piece(board, piece, "Human" if human_turn else "Computer")
        board.display()
        if board.check_quarto():
            return "Human" if human_turn else "Computer"
        human_turn = not human_turn
    return "Draw"


def main_game():
    scores = {"Human": 0, "Computer": 0, "Draws": 0}
    while max(scores.values()) < 3:
        board = Board()
        pieces = initialize_pieces()
        print("\nNew Round\n")

        winner = play_round(board, pieces, human_turn=random.choice([True, False]))
        if winner != "Draw":
            print(f"{winner} wins the round!")
            scores[winner] += 1
        else:
            print("It's a draw.")
            scores["Draws"] += 1

        print(f"Scores: {scores}")

        if max(scores["Human"], scores["Computer"]) < 3:
            if safe_input("Play another round? (y/n): ", str, range=['y', 'n']).lower() != 'y':
                break

    print("Game Over")
    if scores["Human"] > scores["Computer"]:
        print("You win the game!")
    elif scores["Computer"] > scores["Human"]:
        print("Computer wins the game!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main_game()
