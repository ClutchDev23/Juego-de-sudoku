import tkinter as tk
from tkinter import messagebox
import random

class Sudoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("450x600")
        self.root.configure(bg="#f0f0f0")
        
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        
        # Validación: solo números 1-9
        self.vcmd = (self.root.register(self.validate_input), '%P')
        
        self.create_grid()
        self.create_buttons()
        self.load_initial_puzzle()

    def validate_input(self, P):
        if P == "" or (P.isdigit() and len(P) == 1 and P != '0'):
            return True
        else:
            messagebox.showwarning("Atención", "Solo se permiten números del 1 al 9.")
            return False

    def get_bg_color(self, i, j):
        return "#e3f2fd" if (i // 3 + j // 3) % 2 == 0 else "#ffffff"

    def create_grid(self):
        self.main_frame = tk.Frame(self.root, bg="black", bd=2)
        self.main_frame.pack(pady=20)
        
        for i in range(9):
            for j in range(9):
                e = tk.Entry(self.main_frame, width=2, font=('Arial', 20, 'bold'),
                             justify='center', bd=1, relief="flat",
                             bg=self.get_bg_color(i, j), validate="key", 
                             validatecommand=self.vcmd)
                e.grid(row=i, column=j, padx=1, pady=1, ipady=5)
                self.entries[i][j] = e

    def create_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        style = {"font": ('Arial', 10, 'bold'), "fg": "white", "padx": 10, "pady": 5, "width": 12}

        tk.Button(btn_frame, text="Solucionar", command=self.auto_solve,
                  bg="#4CAF50", **style).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(btn_frame, text="Checkear", command=self.check_user_solution,
                  bg="#FF9800", **style).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(btn_frame, text="Limpiar", command=self.clear_board,
                  bg="#f44336", **style).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(btn_frame, text="Nuevo Juego", command=self.load_initial_puzzle,
                  bg="#2196F3", **style).grid(row=1, column=1, padx=5, pady=5)

    def load_initial_puzzle(self):
        self.clear_board()
        board = [
            [5,3,0,0,7,0,0,0,0], [6,0,0,1,9,5,0,0,0], [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3], [4,0,0,8,0,3,0,0,1], [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0], [0,0,0,4,1,9,0,0,5], [0,0,0,0,8,0,0,7,9]
        ]
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    self.entries[i][j].insert(0, str(board[i][j]))
                    self.entries[i][j].config(state="readonly", fg="#1a237e")

    def clear_board(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].config(state="normal", fg="black")
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(bg=self.get_bg_color(i, j))

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num: return False
        sr, sc = 3*(row//3), 3*(col//3)
        for i in range(sr, sr+3):
            for j in range(sc, sc+3):
                if board[i][j] == num: return False
        return True

    def solve(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for n in range(1, 10):
                        if self.is_valid(board, i, j, n):
                            board[i][j] = n
                            if self.solve(board): return True
                            board[i][j] = 0
                    return False
        return True

    def auto_solve(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                row.append(int(val) if val else 0)
            grid.append(row)
        
        if self.solve(grid):
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].config(state="normal")
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(grid[i][j]))
            messagebox.showinfo("Éxito", "Sudoku resuelto correctamente.")
        else:
            messagebox.showerror("Error", "No se encontró solución.")

    def check_user_solution(self):
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                if not val:
                    messagebox.showwarning("Incompleto", "Aún faltan celdas por completar.")
                    return
                
                num = int(val)
                self.entries[i][j].delete(0, tk.END)
                temp_board = []
                for r in range(9):
                    temp_board.append([int(self.entries[r][c].get() or 0) for c in range(9)])
                
                if not self.is_valid(temp_board, i, j, num):
                    self.entries[i][j].insert(0, str(num))
                    self.entries[i][j].config(bg="salmon")
                    messagebox.showerror("Error", f"☹️ Número {num} incorrecto en fila {i+1}, columna {j+1}")
                    return
                
                self.entries[i][j].insert(0, str(num))
        
        messagebox.showinfo("¡Felicidades!", "¡Has completado el Sudoku perfectamente! 🏆")

if __name__ == "__main__":
    root = tk.Tk()
    app = Sudoku(root)
    root.mainloop()