import os
import sys
import tkinter as tk
import random
import time
import copy
import math
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class TicTacToe:
    MAX_DEPTH = 7
    RESTART_DELAY_MS = 1000
    COLOR_BACKGROUND = "#263238"
    COLOR_BUTTON_NORMAL = "#455A64"
    COLOR_BUTTON_HOVER = "#546E7A"
    COLOR_BUTTON_DISABLED = "#37474F"
    COLOR_TEXT_NORMAL = "#ECEFF1"
    COLOR_TEXT_DISABLED = "#90A4AE"
    COLOR_X = "#80CBC4"
    COLOR_O = "#FFAB91"
    COLOR_X_REMOVAL_HIGHLIGHT_BG = "#347870"
    COLOR_O_REMOVAL_HIGHLIGHT_BG = "#8f5a4b"
    FONT_BUTTON = ("Segoe UI", 28, "bold")
    FONT_LABEL = ("Segoe UI", 14)
    FONT_SCORE = ("Segoe UI", 16, "bold")
    def __init__(self, root):
        self.root = root
        self.root.title("Infinite Tic Tac Toe - Enhanced")
        self.root.configure(bg=self.COLOR_BACKGROUND)
        self.root.geometry("450x550")
        icon_path = os.path.join(BASE_DIR, "icon.ico")
        self.root.iconbitmap(icon_path)
        self.bot_score = 0
        self.human_score = 0
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self._create_widgets()
        self.reset_game(first_game=True)
    def _create_widgets(self):
        self.info_frame = tk.Frame(self.root, bg=self.COLOR_BACKGROUND)
        self.info_frame.pack(pady=15)
        self.score_label = tk.Label(self.info_frame, text="", font=self.FONT_SCORE,
                                    bg=self.COLOR_BACKGROUND, fg=self.COLOR_TEXT_NORMAL)
        self.score_label.pack()
        self.status_label = tk.Label(self.info_frame, text="", font=self.FONT_LABEL,
                                     bg=self.COLOR_BACKGROUND, fg=self.COLOR_TEXT_NORMAL)
        self.status_label.pack(pady=5)
        self.button_frame = tk.Frame(self.root, bg=self.COLOR_BACKGROUND)
        self.button_frame.pack(pady=10)
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.button_frame, text="", font=self.FONT_BUTTON, width=4, height=1,
                    relief=tk.FLAT, borderwidth=0,
                    bg=self.COLOR_BUTTON_NORMAL, fg=self.COLOR_TEXT_NORMAL,
                    activebackground=self.COLOR_BUTTON_HOVER,
                    activeforeground=self.COLOR_TEXT_NORMAL,
                    disabledforeground=self.COLOR_TEXT_DISABLED,
                    command=lambda r=i, c=j: self.player_move(r, c)
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                button.bind("<Enter>", lambda e, b=button: self._on_enter(b))
                button.bind("<Leave>", lambda e, b=button: self._on_leave(b))
                self.buttons[i][j] = button
    def _on_enter(self, button):
        if button['state'] == tk.NORMAL:
            button.config(bg=self.COLOR_BUTTON_HOVER)
    def _on_leave(self, button):
        self._update_button_visual_state(button)
    def _update_button_visual_state(self, button):
        """
        Updates a single button's visual state (color, text, enabled/disabled)
        based on the current game board and move lists. This NOW INCLUDES HIGHLIGHTING.
        """
        coords = None
        for r_find in range(3):
            for c_find in range(3):
                if self.buttons[r_find][c_find] == button:
                    coords = (r_find, c_find)
                    break
            if coords: break
        if not coords: return
        r, c = coords
        player_at_pos = self.board[r][c]
        button_config = {}
        is_game_over = self.game_over
        is_x_removal_candidate = (player_at_pos == "X" and len(self.x_moves) == 3 and self.x_moves[0] == (r, c))
        is_o_removal_candidate = (player_at_pos == "O" and len(self.o_moves) == 3 and self.o_moves[0] == (r, c))
        if player_at_pos == "X":
            button_config['text'] = "X"
            button_config['fg'] = self.COLOR_X
            button_config['state'] = tk.DISABLED
            button_config['bg'] = self.COLOR_X_REMOVAL_HIGHLIGHT_BG if is_x_removal_candidate and not is_game_over else self.COLOR_BUTTON_DISABLED
            button_config['disabledforeground'] = self.COLOR_X
        elif player_at_pos == "O":
            button_config['text'] = "O"
            button_config['fg'] = self.COLOR_O
            button_config['state'] = tk.DISABLED
            button_config['bg'] = self.COLOR_O_REMOVAL_HIGHLIGHT_BG if is_o_removal_candidate and not is_game_over else self.COLOR_BUTTON_DISABLED
            button_config['disabledforeground'] = self.COLOR_O
        else:
            button_config['text'] = ""
            button_config['state'] = tk.NORMAL if not is_game_over else tk.DISABLED
            button_config['bg'] = self.COLOR_BUTTON_NORMAL if not is_game_over else self.COLOR_BUTTON_DISABLED
            button_config['fg'] = self.COLOR_TEXT_NORMAL
        button.config(**button_config)
    def _update_all_button_visuals(self):
        """ Updates the visual state of all buttons on the board. """
        for i in range(3):
            for j in range(3):
                 if self.buttons[i][j]:
                     self._update_button_visual_state(self.buttons[i][j])
        self.root.update_idletasks()
    def reset_game(self, first_game=False):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.x_moves = []
        self.o_moves = []
        self.total_moves_played = 0
        self.current_player = "X"
        self.game_over = False
        self.bot_player = random.choice(["X", "O"])
        self.human_player = "O" if self.bot_player == "X" else "X"
        if not first_game:
             print("-" * 20)
             print(f"🔄 Resetting Game... Score: Bot {self.bot_score} - Human {self.human_score}")
        print(f"✨ New Round! Bot is {self.bot_player}. Human is {self.human_player}.")
        # print(f"Bot search depth: {self.MAX_DEPTH}")
        self._update_all_button_visuals()
        self._update_scoreboard_label()
        self._update_status()
        if not self.game_over and self.current_player == self.bot_player:
            self.root.after(500, self._delayed_bot_move)
    def _update_scoreboard_label(self):
        score_text = f"Score: Bot {self.bot_score}  -  Human {self.human_score}"
        if hasattr(self, 'score_label') and self.score_label:
             self.score_label.config(text=score_text)
    def _update_status(self):
        if self.game_over: return
        status_text = f"Bot: {self.bot_player} | Human: {self.human_player} | Turn: {self.current_player}"
        if self.current_player == self.bot_player:
            status_text += " (Bot thinking...)"
        else:
            status_text += " (Your turn)"
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.config(text=status_text)
        self.root.update_idletasks()
    def make_move_on_board(self, row, col, player):
        """CORE LOGIC: Updates board, lists, handles removal. Returns removed coords."""
        if self.board[row][col] != "": return None
        self.board[row][col] = player
        moves_list = self.x_moves if player == "X" else self.o_moves
        moves_list.append((row, col))
        self.total_moves_played += 1
        removed_coords = None
        if len(moves_list) > 3:
            r_rem, c_rem = moves_list.pop(0)
            print(f"Oldest move ({r_rem}, {c_rem}) by {player} removed!")
            self.board[r_rem][c_rem] = ""
            removed_coords = (r_rem, c_rem)
        return removed_coords
    def highlight_next_moves(self):
        """Refreshes all button visuals which includes checking for highlights."""
        self._update_all_button_visuals()
    def player_move(self, row, col):
        if self.game_over or self.current_player != self.human_player or self.board[row][col] != "":
            return
        player = self.human_player
        print(f"Debug: Human ({player}) playing at ({row},{col})")
        removed_info = self.make_move_on_board(row, col, player)
        self._update_all_button_visuals()
        if self.check_winner(player, self.board):
            self.end_game(f"Player {player} wins!")
            return
        if self.is_draw():
            self.end_game("It's a draw!")
            return
        self.current_player = self.bot_player
        self._update_status()
        if not self.game_over:
            self._delayed_bot_move()
    def _delayed_bot_move(self):
        if not self.game_over:
            self._update_status()
            self.root.after(100, self.bot_move)
    def bot_move(self):
        if self.game_over or self.current_player != self.bot_player: return
        start_time = time.time()
        print(f"Bot ({self.bot_player}) is thinking (depth={self.MAX_DEPTH})...")
        available_moves = self.get_available_moves(self.board)
        if not available_moves: return
        best_score = -math.inf
        best_move = available_moves[0]
        for r, c in available_moves:
            sim_result = self.simulate_move_for_minimax(r, c, self.bot_player, self.board, self.x_moves, self.o_moves)
            if sim_result:
                next_board, next_x, next_o = sim_result
                move_score = self.minimax(next_board, next_x, next_o, self.MAX_DEPTH - 1, -math.inf, math.inf, False)
                if move_score > best_score:
                    best_score = move_score
                    best_move = (r, c)
        end_time = time.time()
        final_r, final_c = best_move
        print(f"Bot finished in {end_time - start_time:.3f}s. Chooses: ({final_r},{final_c}), Score: {best_score}")
        player = self.bot_player
        removed_info = self.make_move_on_board(final_r, final_c, player)
        print(f"Player {player} placed at ({final_r}, {final_c})")
        self._update_all_button_visuals()
        if self.check_winner(player, self.board):
            self.end_game(f"Player {player} wins!")
            return
        if self.is_draw():
            self.end_game("It's a draw!")
            return
        self.current_player = self.human_player
        self._update_status()
    def end_game(self, message):
        if self.game_over: return
        print(f"Game Over: {message}")
        self.game_over = True
        winner = None
        if self.check_winner(self.bot_player, self.board):
            self.bot_score += 1
            winner = self.bot_player
        elif self.check_winner(self.human_player, self.board):
            self.human_score += 1
            winner = self.human_player
        if winner == self.bot_player:
             final_message = f"Bot Wins! (Score: Bot {self.bot_score} - Human {self.human_score})"
        elif winner == self.human_player:
              final_message = f"You Win! (Score: Bot {self.bot_score} - Human {self.human_score})"
        else:
             final_message = f"It's a Draw! (Score: Bot {self.bot_score} - Human {self.human_score})"
        print(final_message)
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.config(text=final_message)
        self._update_scoreboard_label()
        self._update_all_button_visuals()
        print(f"Restarting in {self.RESTART_DELAY_MS / 1000} seconds...")
        self.root.after(self.RESTART_DELAY_MS, self.reset_game)
    def get_available_moves(self, board_state):
        return [(r, c) for r in range(3) for c in range(3) if board_state[r][c] == ""]
    def check_winner(self, player, board_state):
        b = board_state
        for i in range(3):
            if all(b[i][j] == player for j in range(3)): return True
            if all(b[j][i] == player for j in range(3)): return True
        if all(b[i][i] == player for i in range(3)): return True
        if all(b[i][2 - i] == player for i in range(3)): return True
        return False
    def is_draw(self):
         return not self.get_available_moves(self.board) and \
                not self.check_winner("X", self.board) and \
                not self.check_winner("O", self.board)
    def evaluate_board(self, board_state, current_depth):
        if self.check_winner(self.bot_player, board_state): return 100 - (self.MAX_DEPTH - current_depth)
        elif self.check_winner(self.human_player, board_state): return -100 + (self.MAX_DEPTH - current_depth)
        else: return 0
    def simulate_move_for_minimax(self, r, c, player, board, x_moves, o_moves):
        if board[r][c] != "": return None
        temp_board = copy.deepcopy(board)
        temp_x_moves = copy.deepcopy(x_moves)
        temp_o_moves = copy.deepcopy(o_moves)
        temp_board[r][c] = player
        moves_list = temp_x_moves if player == "X" else temp_o_moves
        moves_list.append((r, c))
        if len(moves_list) > 3:
            r_rem, c_rem = moves_list.pop(0)
            temp_board[r_rem][c_rem] = ""
        return temp_board, temp_x_moves, temp_o_moves
    def minimax(self, board, x_moves, o_moves, depth, alpha, beta, is_maximizing):
        score = self.evaluate_board(board, depth)
        if score != 0 or depth == 0: return score
        available_moves = self.get_available_moves(board)
        if not available_moves: return 0
        player_to_move = self.bot_player if is_maximizing else self.human_player
        if is_maximizing:
            max_eval = -math.inf
            for r, c in available_moves:
                sim_result = self.simulate_move_for_minimax(r, c, player_to_move, board, x_moves, o_moves)
                if sim_result:
                    new_board, new_x, new_o = sim_result
                    eval_score = self.minimax(new_board, new_x, new_o, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha: break
            return max_eval
        else:
            min_eval = math.inf
            for r, c in available_moves:
                sim_result = self.simulate_move_for_minimax(r, c, player_to_move, board, x_moves, o_moves)
                if sim_result:
                    new_board, new_x, new_o = sim_result
                    eval_score = self.minimax(new_board, new_x, new_o, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha: break
            return min_eval
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
