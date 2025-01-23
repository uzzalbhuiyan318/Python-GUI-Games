import tkinter as tk
from tkinter import messagebox

# Global variables
current_player = "X"
board = [" " for _ in range(9)]  # Represents the 3x3 board
player_x_score = 0
player_o_score = 0

# Function to check the winner
def check_winner():
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
            return board[combo[0]]  # Return the winner ('X' or 'O')
    return None

# Function to handle button click
def button_click(index):
    global current_player
    
    if board[index] == " ":
        board[index] = current_player
        buttons[index].config(text=current_player, bg="white", fg="#333333")
        
        winner = check_winner()
        
        if winner:
            # Update the score based on the winner
            global player_x_score, player_o_score
            if winner == "X":
                player_x_score += 1
            else:
                player_o_score += 1
            
            # Show the scores and announce the winner
            update_scores()
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            play_again_button.grid(row=4, column=0, columnspan=3, pady=10)  # Show the Play Again button after the match ends
        elif " " not in board:
            # It's a tie, no score change
            update_scores()
            messagebox.showinfo("Game Over", "It's a tie!")
            play_again_button.grid(row=4, column=0, columnspan=3, pady=10)  # Show the Play Again button after the match ends
        else:
            # Switch players if the game continues
            current_player = "O" if current_player == "X" else "X"
            label.config(text=f"Player {current_player}'s Turn")

# Function to reset the game
def reset_game():
    global current_player, board
    current_player = "X"
    board = [" " for _ in range(9)]
    for button in buttons:
        button.config(text=" ", bg="#f2f2f2")  # Set the background to light gray
    label.config(text="Player X's Turn", fg="red")
    play_again_button.grid_forget()  # Hide the Play Again button initially

# Function to update the scores display
def update_scores():
    score_label.config(text=f"Player X: {player_x_score}  |  Player O: {player_o_score}")

# Create the main window
window = tk.Tk()
window.title("Tic Tac Toe")
window.configure(bg="#1e1e2f")  # Dark background color for a professional look

# Create a frame to hold the game platform in the center
game_frame = tk.Frame(window, bg="#1e1e2f", bd=10, relief="sunken", padx=20, pady=20)
game_frame.grid(row=0, column=0, padx=30, pady=30)

# Center the game frame horizontally and vertically without resizing it
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
game_frame.grid_rowconfigure(0, weight=1)
game_frame.grid_rowconfigure(1, weight=1)
game_frame.grid_rowconfigure(2, weight=3)
game_frame.grid_rowconfigure(3, weight=1)
game_frame.grid_rowconfigure(4, weight=1)
game_frame.grid_columnconfigure(0, weight=1)
game_frame.grid_columnconfigure(1, weight=1)
game_frame.grid_columnconfigure(2, weight=1)

# Create a label to show whose turn it is
label = tk.Label(game_frame, text="Player X's Turn", font=("Arial", 14), bg="#1e1e2f", fg="red")
label.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

# Create a label to display the scores
score_label = tk.Label(game_frame, text=f"Player X: {player_x_score}  |  Player O: {player_o_score}", font=("Arial", 12), bg="#1e1e2f", fg="green")
score_label.grid(row=1, column=0, columnspan=3, pady=5, sticky="nsew")

# Create a grid of buttons for the Tic Tac Toe board with hover effects and rounded corners
buttons = []
for i in range(9):
    button = tk.Button(game_frame, text=" ", width=10, height=3, font=("Arial", 20), command=lambda i=i: button_click(i), bg="#f2f2f2", bd=5, relief="solid", highlightbackground="#1e1e2f", highlightthickness=2)
    button.grid(row=(i//3)+2, column=i%3, padx=5, pady=5, sticky="nsew")
    button.bind("<Enter>", lambda e, btn=button: btn.config(bg="#e6e6e6"))  # Hover effect
    button.bind("<Leave>", lambda e, btn=button: btn.config(bg="#f2f2f2"))  # Reset hover effect
    buttons.append(button)

# Create a Play Again button with modern interactive effects and no border
def on_button_hover(event):
    play_again_button.config(bg="#45a049", fg="white", relief="raised")

def on_button_leave(event):
    play_again_button.config(bg="#4CAF50", fg="white", relief="solid")

def on_button_click(event):
    play_again_button.config(bg="#388E3C", fg="white")
    reset_game()

play_again_button = tk.Button(game_frame, text="Play Again", width=20, height=2, font=("Arial", 14), command=reset_game, bg="#4CAF50", fg="white")
play_again_button.grid(row=4, column=0, columnspan=3, pady=10)
play_again_button.grid_forget()  # Initially hide the button

# Adding hover and click effects for the Play Again button
play_again_button.bind("<Enter>", on_button_hover)
play_again_button.bind("<Leave>", on_button_leave)
play_again_button.bind("<Button-1>", on_button_click)

# Start the Tkinter event loop
window.mainloop()
