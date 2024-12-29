import tkinter as tk
from tkinter import messagebox
import math


class Game:
    def __init__(self):
        # create the window
        self.window = tk.Tk()
        self.window.title("3moveXO Game")
        self.window.configure(bg="#343434")

        # set default window dimensions
        window_width = 480
        window_height = 600

        # set the window location by default to the center of the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_top = int((screen_height - window_height) / 2)
        position_left = int((screen_width - window_width) / 2)
        self.window.geometry(
            f"{window_width}x{window_height}+{position_left}+{position_top}"
        )

        # define game variables
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.moves = {"X": [], "O": []}
        self.current_player = "X"

        # make the element inside the window dynamic
        self.window.rowconfigure(0, weight=1)
        for i in range(1, 5):
            self.window.rowconfigure(i, weight=1)
        for i in range(3):
            self.window.columnconfigure(i, weight=1)

        # initializing the status label
        self.state_label = tk.Label(
            self.window,
            text="Player X's turn",
            font=("Consolas", 30, "bold"),
            bg="#343434",
            fg="#ffde57",
        )
        self.state_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

        # initializing the buttons grid
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

        # initializing the restart button
        restart_button = tk.Button(
            self.window,
            text="Restart",
            command=self.restart_game,
            bg="#343434",
            fg="#ffffff",
            font=("Consolas", 25, "bold"),
        )
        restart_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

        # initializing the close button
        close_button = tk.Button(
            self.window,
            text="Close",
            command=self.window.quit,
            bg="#343434",
            fg="#ffffff",
            font=("Consolas", 25, "bold"),
        )
        close_button.grid(row=4, column=2, sticky="nsew")

        self.window.mainloop()

    def create_board(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    self.window,
                    text=" ",
                    font=("Consolas", 60, "bold"),
                    bg="#343434",
                    command=lambda r=row, c=col: self.handle_click(r, c),
                )
                button.grid(row=row + 1, column=col, sticky="nsew", padx=5, pady=5)
                self.buttons[row][col] = button

    def handle_click(self, row, col):
        # Non-empty cell
        if self.board[row][col] != " ":
            return

        # apply the move
        self.board[row][col] = self.current_player
        self.update_button(row, col)

        # check for winner and show the result after that restart the game
        if self.check_win(self.current_player):
            self.state_label.config(text=f"Player {self.current_player} wins!")
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.restart_game()
            return

        # check for draw and show the result after that restart the game
        if self.is_draw():
            self.state_label.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            self.restart_game()
            return

        # delete the third Symbol if there isn't winner
        if len(self.moves[self.current_player]) >= 2:
            old_row, old_col = self.moves[self.current_player].pop(0)
            self.board[old_row][old_col] = " "
            self.buttons[old_row][old_col].config(text=" ", bg="#343434")

        # add the move to the move_list
        self.moves[self.current_player].append((row, col))

        # change the player
        self.current_player = "O" if self.current_player == "X" else "X"

        # update state label
        self.state_label.config(text=f"Player {self.current_player}'s turn")

        # make the ai play
        if self.current_player == "O":
            self.computer_turn()

    def update_button(self, row, col):
        color = "#ff781f" if self.current_player == "X" else "#4584b6"
        self.buttons[row][col].config(
            text=self.current_player,
            fg=color,
            bg="#646464",
            font=("Consolas", 60, "bold"),
        )

    def check_win(self, player):
        #check if the player has won in any row
        for row in self.board:
            if all(
                cell == player for cell in row
            ):
                return True

        #check if the player has won in any column
        for col in range(3):
            if all(
                self.board[row][col] == player for row in range(3)
            ):
                return True

        #check if the player has won in either diagonal
        if all(self.board[i][i] == player for i in range(3)) or all(
            self.board[i][2 - i] == player for i in range(3)
        ):
            return True

        return False

    def is_draw(self):
        return all(
            self.board[row][col] != " " for row in range(3) for col in range(3)
        )

    def computer_turn(self):
        move = self.best_move()
        if move:
            row, col = move
            self.handle_click(row, col)

    def best_move(self):
        best_score = -math.inf
        move = None
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    self.board[row][col] = "O"
                    score = self.minimax(0, False)
                    self.board[row][col] = " "
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        return move

    def minimax(self, depth, is_maximizing):
        player = "O" if is_maximizing else "X"
        if self.check_win("O"):
            return 10 - depth
        if self.check_win("X"):
            return depth - 10
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == " ":
                        self.board[row][col] = "O"
                        score = self.minimax(depth + 1, False)
                        self.board[row][col] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == " ":
                        self.board[row][col] = "X"
                        score = self.minimax(depth + 1, True)
                        self.board[row][col] = " "
                        best_score = min(score, best_score)
            return best_score

    def restart_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.moves = {"X": [], "O": []}
        self.current_player = "X"
        self.state_label.config(text="Player X's turn")
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=" ", bg="#343434")


Game()
