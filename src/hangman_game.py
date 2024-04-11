import tkinter as tk
import random

ATTEMPTS = 7

class HangmanGame:
    def __init__ (self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.geometry("900x650")
        self.master.configure(bg='light blue')
        self.word_list = ["PYTHON", "JAVASCRIPT", "KOTLIN", "JAVA", "RUBY", "SWIFT"]
        self.secret_word = self.choose_secret_word()
        self.correct_guesses = set()
        self.incorrect_guesses = set()
        self.attempts_left = ATTEMPTS
        # Custom button styling
        self.button_bg = "#4a7a8c"
        self.button_fg = "black"
        self.button_font = ("Helvetica", 12, "bold")
        self.initialize_gui()
        

    def choose_secret_word(self):
        return random.choice(self.word_list)

    def initialize_gui(self):
        # Creating a Canvas where the hangman is drawn 
        self.hangman_canvas = tk.Canvas(self.master, width=300, height=300, bg="white")
        self.hangman_canvas.pack(pady=20)
        # Displaying the word with correctly guessed letters or blanks
        self.word_display = tk.Label(self.master, text = "_ " * len(self.secret_word), font =("Helvetica", 30), bg= 'light blue')
        self.word_display.pack(pady = (40, 20))
        # Displaying alphabet buttons for guessing letters
        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack(pady=20)
        self.setup_alphabet_buttons()
        # Add reset game button
        self.reset_button = tk.Button(self.master, text = "Reset Game", command = self.reset_game,  bg=self.button_bg, fg=self.button_fg, font=self.button_font )
        self.reset_button.pack(pady=(10,0))

    def update_hangman_canvas(self):
        self.hangman_canvas.delete("all")   # Clear the canvas for redrawing        
        stages = [self.draw_head, self.draw_body, self.draw_left_arm, self.draw_right_arm, self.draw_left_leg, self.draw_right_leg, self.draw_face]
        incorrect_guesses_count = len(self.incorrect_guesses)
        for i in range (incorrect_guesses_count):
            if i < len(stages):
                stages[i]() # Call the drawing method for each incorrect guess

    def draw_head(self):
        self.hangman_canvas.create_oval(125, 50, 185, 110, outline = "black")

    def draw_body(self):
        self.hangman_canvas.create_line(155, 110, 155, 170, fill = "black")

    def draw_left_arm(self):
        self.hangman_canvas.create_line(155, 130, 125, 150, fill = "black")

    def draw_right_arm(self):
        self.hangman_canvas.create_line(155, 130, 180, 150, fill = "black")

    def draw_left_leg(self):
        self.hangman_canvas.create_line(155, 170, 125, 200, fill = "black")

    def draw_right_leg(self):
        self.hangman_canvas.create_line(155, 170, 185, 200, fill = "black")

    def draw_face(self):
        self.hangman_canvas.create_line(140, 70, 150, 80, fill = "black")   # Draw left eye
        self.hangman_canvas.create_line(160, 70, 170, 80, fill = "black")   # Draw right eye
        self.hangman_canvas.create_arc(140, 85, 170, 105, start = 0, extent = -180, fill = "black")


    # This function handles letter guesses
    def guess_letter(self, letter):
        if letter in self.secret_word and letter not in self.correct_guesses:
            self.correct_guesses.add(letter)
        elif letter not in self.incorrect_guesses:
            self.incorrect_guesses.add(letter)
            self.attempts_left -= 1
            self.update_hangman_canvas()

        self.update_word_display()
        self.check_game_over()

    def update_word_display(self):
        displayed_word = "".join([(letter + " ") if letter in self.correct_guesses else "_ " for letter in self.secret_word])
        self.word_display.config(text=displayed_word)

    def check_game_over(self):
        if set(self.secret_word).issubset(self.correct_guesses):
            self.display_game_over_message("Congratulations, Youv'e won!")
        elif self.attempts_left == 0:
            self.display_game_over_message(f"Game over! The word was: {self.secret_word}")

    def setup_alphabet_buttons(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        upper_row = alphabet[:13] #First half of alphabet
        lower_row = alphabet[13:] #Second half of alphabet

        upper_frame = tk.Frame(self.buttons_frame)
        upper_frame.pack()
        lower_frame = tk.Frame(self.buttons_frame)
        lower_frame.pack()

        for letter in upper_row:
            button = tk.Button(upper_frame, text=letter, command=lambda l=letter: self.guess_letter(l), width=3, height=2, bg=self.button_bg, fg=self.button_fg, font=self.button_font)
            button.pack(side="left", padx=2, pady=2)

        for letter in lower_row:
            button = tk.Button(lower_frame, text=letter, command=lambda l=letter: self.guess_letter(l), width=2, height=2,  bg=self.button_bg, fg=self.button_fg, font=self.button_font)
            button.pack(side="left", padx=2, pady=2)

    def display_game_over_message(self, message):
        # Hide the reset button
        self.reset_button.pack_forget()
        # Hide the alphabet buttons 
        self.buttons_frame.pack_forget()
        # Display the game over message in the now-empty area
        self.game_over_label = tk.Label(self.master, text=message, font= ("Helvetica", 18), fg="red", bg="light blue")
        self.game_over_label.pack(pady=(10, 20))
        # Display the Restart button
        self.restart_button = tk.Button(self.master, text = "Restart Game", command = self.reset_game, width=20, height=2)
        self.restart_button.pack(pady=(10,20))

    def reset_game(self):
        
        self.secret_word = self.choose_secret_word()
        self.correct_guesses = set()
        self.incorrect_guesses = set()
        self.attempts_left = ATTEMPTS

        self.hangman_canvas.delete("all")
        self.update_word_display()

        for frame in self.buttons_frame.winfo_children():
            for button in frame.winfo_children():
                button.configure(state = tk.NORMAL)

        if hasattr(self, 'game_over_label'):
            self.game_over_label.destroy()

        # Reset game state and GUI elements as previously outlined
        # Hide the game over label and the Restart button when the game is reset
        if hasattr(self, 'game_over_label') and self.game_over_label.winfo_exists():
            self.game_over_label.pack_forget()
        if hasattr(self, 'restart_button') and self.restart_button.winfo_exists():
            self.restart_button.pack_forget()

        # Ensure the alphabet buttons frame and other interactive elements are visible again
        self.buttons_frame.pack(pady=20)

        # Re-show the reset button
        self.reset_button.pack(pady=(10,0))

def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()