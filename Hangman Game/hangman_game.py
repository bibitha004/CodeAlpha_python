import random
import tkinter as tk
from tkinter import messagebox
import time

# List of words
words_list = ['python', 'hangman', 'challenge', 'developer', 'programming']

# Function to choose a random word
def choose_word():
    return random.choice(words_list)

# Function to update the displayed word with guessed letters
def update_displayed_word():
    displayed_word.set(' '.join([letter if letter in correct_guesses else '_' for letter in word]))

# Function to handle button click (guessing a letter)
def guess_letter(letter):
    if letter in correct_guesses or letter in incorrect_guesses:
        messagebox.showinfo("Hangman", "You've already guessed that letter.")
        return

    if letter in word:
        correct_guesses.append(letter)
        update_displayed_word()
        if all(l in correct_guesses for l in word):
            show_celebration_animation()  # Trigger celebration on win
    else:
        incorrect_guesses.append(letter)
        incorrect_guesses_label.config(text="Incorrect guesses: " + ', '.join(incorrect_guesses))
        attempts_left.set(attempts_left.get() - 1)
        if attempts_left.get() == 0:
            messagebox.showinfo("Hangman", f"Game Over! The word was: {word}")
            reset_game()

# Function to reset the game
def reset_game():
    global word, correct_guesses, incorrect_guesses
    word = choose_word()
    correct_guesses = []
    incorrect_guesses = []
    update_displayed_word()
    incorrect_guesses_label.config(text="Incorrect guesses: ")
    attempts_left.set(max_attempts)

# Celebration Animation
def show_celebration_animation():
    # Disable the buttons during animation
    for button in buttons_frame.winfo_children():
        button.config(state="disabled")
    
    celebration_window = tk.Toplevel(root)
    celebration_window.geometry("400x400")
    celebration_window.title("Congratulations!")

    # Center the celebration window
    center_window(celebration_window, 400, 400)

    canvas = tk.Canvas(celebration_window, width=400, height=400, bg='white')
    canvas.pack()

    # Create the congratulations message
    canvas.create_text(200, 100, text="Congratulations!", font=("Helvetica", 24, "bold"), fill="green")

    # Create confetti particles
    confetti = []
    for _ in range(50):
        x = random.randint(0, 400)
        y = random.randint(0, 400)
        size = random.randint(10, 20)
        color = random.choice(["red", "blue", "green", "yellow", "purple", "orange"])
        confetti.append(canvas.create_oval(x, y, x + size, y + size, fill=color, outline=color))

    # Animate the confetti falling down
    for _ in range(100):  # Repeat animation for 100 frames
        for particle in confetti:
            canvas.move(particle, random.randint(-5, 5), random.randint(2, 10))
        celebration_window.update()
        time.sleep(0.05)

    # End the game and reset after the celebration
    celebration_window.after(1000, lambda: [celebration_window.destroy(), reset_game()])

# Function to center the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

# Initialize the main window
root = tk.Tk()
root.title("Hangman Game")
root.configure(bg='light blue')  # Set background color to light blue

# Set the dimensions of the main window and center it
window_width = 600
window_height = 400
center_window(root, window_width, window_height)

# Variables
correct_guesses = []
incorrect_guesses = []
max_attempts = 6
attempts_left = tk.IntVar(value=max_attempts)
displayed_word = tk.StringVar()

# Choose a random word to start
word = choose_word()

# GUI Layout
word_label = tk.Label(root, textvariable=displayed_word, font=('Helvetica', 18), bg='light blue')
word_label.pack(pady=20)

attempts_label = tk.Label(root, text="Attempts left: ", bg='light blue')
attempts_label.pack()

attempts_left_label = tk.Label(root, textvariable=attempts_left, font=('Helvetica', 14), bg='light blue')
attempts_left_label.pack()

incorrect_guesses_label = tk.Label(root, text="Incorrect guesses: ", font=('Helvetica', 12), bg='light blue')
incorrect_guesses_label.pack(pady=10)

# Alphabet buttons for guessing letters
buttons_frame = tk.Frame(root, bg='light blue')
buttons_frame.pack()

# Create buttons for each letter
for letter in 'abcdefghijklmnopqrstuvwxyz':
    btn = tk.Button(buttons_frame, text=letter.upper(), width=4, height=2,
                    command=lambda l=letter: guess_letter(l), bg='blue', fg='white')  # Blue button with white text
    btn.grid(row=(ord(letter) - 97) // 9, column=(ord(letter) - 97) % 9)

# Reset button to start a new game
reset_button = tk.Button(root, text="Reset Game", command=reset_game, font=('Helvetica', 12), bg='blue', fg='white')
reset_button.pack(pady=20)

# Initial word display
update_displayed_word()

# Run the main application loop
root.mainloop()
