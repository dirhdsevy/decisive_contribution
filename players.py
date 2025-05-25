import random
from tkinter import messagebox


class AIPlayer:
    def __init__(self, color, game):
        self.color = color
        self.game = game

    def make_move(self):
        if not hasattr(self.game, 'is_bot_game') or not self.game.is_bot_game:
            return
        if self.game.board.current_player != self.color:
            return
        
        possible_moves = self.get_all_possible_moves()

        if not possible_moves:
            self.game.board.switch_player()
            return

        start, end = random.choice(possible_moves)

        if self.game.board.move_piece(start, end):
            if hasattr(self.game, 'update_counters'):
                self.game.update_counters()
            self.game.draw_board()
            
            winner = self.game.board.check_winner()
            if winner:
                self.game.root.after(1000,
                                     lambda: messagebox.showinfo("Гра завершена", f"Переміг гравець {winner}!"))
                self.game.restart()
                return

            if (hasattr(self.game.board, 'must_capture') and
                    self.game.board.must_capture and
                    self.game.board.last_capture_pos == end):
                self.game.root.after(1000, self.make_move)

    def get_all_possible_moves(self):
        moves = []
        board = self.game.board

        if hasattr(board, 'get_forced_captures'):
            forced_captures = board.get_forced_captures()
            if forced_captures:
                return forced_captures

        for row in range(board.size):
            for col in range(board.size):
                piece = board.grid[row][col]
                if piece and piece.color == self.color:
                    if piece.is_king:
                        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                            distance = 1
                            while True:
                                new_row, new_col = row + dr * distance, col + dc * distance
                                if not (0 <= new_row < board.size and 0 <= new_col < board.size):
                                    break
                                if board.grid[new_row][new_col] is not None:
                                    break
                                moves.append(((row, col), (new_row, new_col)))
                                distance += 1
                    else:
                        directions = [(-1, -1), (-1, 1)] if self.color == 'white' else [(1, -1), (1, 1)]
                        for dr, dc in directions:
                            new_row, new_col = row + dr, col + dc
                            if (0 <= new_row < board.size and 0 <= new_col < board.size and
                                    board.grid[new_row][new_col] is None):
                                moves.append(((row, col), (new_row, new_col)))
        return moves


class HumanPlayer:
    def __init__(self, color, game):
        self.color = color
        self.game = game

    def make_move(self, start, end):
        return self.game.board.move_piece(start, end)
