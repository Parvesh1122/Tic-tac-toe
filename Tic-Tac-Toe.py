import tkinter as tk
import os
import sys

from tkinter import messagebox

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS   # for exe
    except:
        base_path = os.path.abspath(".")  # for normal run
    return os.path.join(base_path, relative_path)

# --- Game Logic ---
def restart():
    global turn
    turn = "X"
    for i in range(3):
        for j in range(3):
            button[i][j].config(text="", bg="#1a1a2e") # Deep space blue

def game(btn):
    global turn
    if btn["text"] == "":
        btn.config(text=turn, fg="#00d4ff" if turn == "X" else "#ff007f") # Cyan for X, Pink for O
        if not check_win() and not check_draw():
            turn = "O" if turn == "X" else "X"

def check_win():
    for i in range(3):
        # Check rows
        if button[i][0]["text"] == button[i][1]["text"] == button[i][2]["text"] != "":
            declare_winner()
            return True
        # Check columns
        if button[0][i]["text"] == button[1][i]["text"] == button[2][i]["text"] != "":
            declare_winner()
            return True
    # Check diagonals
    if button[0][0]["text"] == button[1][1]["text"] == button[2][2]["text"] != "":
        declare_winner()
        return True
    if button[0][2]["text"] == button[1][1]["text"] == button[2][0]["text"] != "":
        declare_winner()
        return True
    return False

def declare_winner():
    messagebox.showinfo("Game Over", f"Player {turn} wins!")
    restart()

def check_draw():
    for i in range(3):
        for j in range(3):
            if button[i][j]["text"] == "":
                return False
    messagebox.showinfo("Game Over", "It's a Draw! Try Again.")
    restart()
    return True

# --- UI Setup ---
root = tk.Tk()
root.title("Tic-Tac-Toe")

# 1. Load and Resize the Background
try:
    # Load original and shrink by half (subsample 2x2)
    original_img = tk.PhotoImage(file=resource_path("tic.png"))
    bg_image = original_img.subsample(2, 2) 
except:
    # Fallback if image is missing
    print("Error: 'Image' not found. Please place it in the script folder.")
    root.destroy()
    exit()

width = bg_image.width()
height = bg_image.height()

# 2. Create Canvas
canvas = tk.Canvas(root, width=width, height=height, highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, image=bg_image, anchor="nw")

# 3. Create Game Board (The Grid)
# We use a frame to hold the 3x3 buttons
board_frame = tk.Frame(root, bg="#0f0f1b") # Matches the phone screen color

# Position the frame in the middle of the phone screen area
# You can tweak the +30 value to move it up or down
canvas.create_window(width//2, height//2 + 30, window=board_frame)

button = [[None for _ in range(3)] for _ in range(3)]
turn = "X"

for i in range(3):
    for j in range(3):
        btn = tk.Button(board_frame, text="", font=("Arial", 16, "bold"), 
                        width=4, height=2, bg="#1a1a2e", fg="white",
                        relief="flat", activebackground="#252545")
        btn.grid(row=i, column=j, padx=3, pady=3)
        btn.config(command=lambda b=btn: game(b))
        button[i][j] = btn

# 4. Add a Restart Button at the bottom of the phone screen
restart_btn = tk.Button(root, text="RESTART GAME", font=("Arial", 10, "bold"),
                        command=restart, bg="#ff007f", fg="white", 
                        padx=10, relief="flat")
canvas.create_window(width//2, height - 80, window=restart_btn)

root.mainloop()