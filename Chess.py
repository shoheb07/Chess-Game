import tkinter as tk

BOARD_SIZE = 8
SQUARE_SIZE = 80
PIECES = {
    "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
    "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙"
}

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Chess Game")

        self.canvas = tk.Canvas(root, width=BOARD_SIZE*SQUARE_SIZE,
                                 height=BOARD_SIZE*SQUARE_SIZE)
        self.canvas.pack()

        self.board = [
            list("rnbqkbnr"),
            list("pppppppp"),
            list("........"),
            list("........"),
            list("........"),
            list("........"),
            list("PPPPPPPP"),
            list("RNBQKBNR")
        ]

        self.selected = None
        self.turn = "white"

        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                color = "#769656" if (r+c) % 2 else "#EEEED2"
                x1, y1 = c*SQUARE_SIZE, r*SQUARE_SIZE
                x2, y2 = x1+SQUARE_SIZE, y1+SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                piece = self.board[r][c]
                if piece != ".":
                    self.canvas.create_text(
                        x1+40, y1+40,
                        text=PIECES[piece],
                        font=("Arial", 36)
                    )

    def on_click(self, event):
        r = event.y // SQUARE_SIZE
        c = event.x // SQUARE_SIZE

        if self.selected:
            sr, sc = self.selected
            if self.is_valid_move(sr, sc, r, c):
                self.board[r][c] = self.board[sr][sc]
                self.board[sr][sc] = "."
                self.turn = "black" if self.turn == "white" else "white"
            self.selected = None
        else:
            piece = self.board[r][c]
            if piece != "." and self.is_correct_turn(piece):
                self.selected = (r, c)

        self.draw_board()

    def is_correct_turn(self, piece):
        return (piece.isupper() and self.turn == "white") or \
               (piece.islower() and self.turn == "black")

    def is_valid_move(self, sr, sc, r, c):
        piece = self.board[sr][sc]
        target = self.board[r][c]

        if target != "." and piece.isupper() == target.isupper():
            return False

        dr, dc = r - sr, c - sc

        if piece.lower() == "p":  # Pawn
            direction = -1 if piece.isupper() else 1
            return dc == 0 and dr == direction and target == "."

        if piece.lower() == "r":  # Rook
            return sr == r or sc == c

        if piece.lower() == "n":  # Knight
            return (abs(dr), abs(dc)) in [(2,1),(1,2)]

        if piece.lower() == "b":  # Bishop
            return abs(dr) == abs(dc)

        if piece.lower() == "q":  # Queen
            return sr == r or sc == c or abs(dr) == abs(dc)

        if piece.lower() == "k":  # King
            return abs(dr) <= 1 and abs(dc) <= 1

        return False

if __name__ == "__main__":
    root = tk.Tk()
    ChessGame(root)
    root.mainloop()
