import tkinter as tk
import tkinter.simpledialog
import random
import sqlite3

class SnakeGame:
    def __init__(self, master, main_menu, username, difficulty):
        self.master = master
        self.main_menu = main_menu
        self.username = username
        self.difficulty = difficulty

        self.speed = 100  # Default speed
        self.food_count = 0
        if self.difficulty == "easy":
            self.speed = 200
        elif self.difficulty == "hard":
            self.speed = 50
        elif self.difficulty == "unlimited":
            self.speed = 200

        self.resolution = (1280, 720)  
        self.block_size = 20  
        self.canvas_width = self.resolution[0]
        self.canvas_height = self.resolution[1]

        self.master.title("Snake Game")
        self.master.geometry(f"{self.canvas_width}x{self.canvas_height}")

        self.canvas = tk.Canvas(self.master, bg="black", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.score = 0
        self.score_display = self.canvas.create_text(self.canvas_width - 20, 10, text=f"Score: {self.score}", fill="white", anchor="e")

        self.initial_message = self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2, text="Press SPACE to start...", fill="white", font=("Helvetica", 16), tags="initial_message")

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.food = self.create_food()

        self.game_running = False
        self.paused = False
        self.master.bind("<Key>", self.handle_key)

        # Initialize database
        self.conn = sqlite3.connect('snake_game.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS high_scores
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           player_name TEXT,
                           score INTEGER)''')
        self.conn.commit()

    def insert_score(self, player_name, score):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO high_scores (player_name, score) VALUES (?, ?)", (player_name, score))
        self.conn.commit()

    def fetch_high_scores(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT player_name, score FROM high_scores ORDER BY score DESC LIMIT 10")
        return cursor.fetchall()

    def create_food(self):
        x = random.randint(1, (self.canvas_width - self.block_size) // self.block_size) * self.block_size
        y = random.randint(1, (self.canvas_height - self.block_size) // self.block_size) * self.block_size
        food = self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill="red")
        return food

    def handle_key(self, event):
        if event.keysym == "space":
            if not self.game_running:
                self.reset_game()
            else:
                self.toggle_pause()

        if self.game_running and not self.paused:
            self.change_direction(event)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2, text="Paused. Press SPACE to continue...", fill="white", font=("Helvetica", 16), tags="paused_text")
        else:
            self.canvas.delete("paused_text")
            self.update()

    def reset_game(self):
        self.canvas.delete("initial_message")
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.score = 0
        self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")
        self.canvas.delete("game_over_text")
        self.game_running = True
        self.paused = False
        self.food_count = 0  # Reset food count for unlimited mode
        self.update()

    def change_direction(self, event):
        key = event.keysym
        if (key == "Up" or key == "w") and self.direction != "Down":
            self.direction = "Up"
        elif (key == "Down" or key == "s") and self.direction != "Up":
            self.direction = "Down"
        elif (key == "Left" or key == "a") and self.direction != "Right":
            self.direction = "Left"
        elif (key == "Right" or key == "d") and self.direction != "Left":
            self.direction = "Right"
        elif key == "8" and self.direction != "Down":
            self.direction = "Up"
        elif key == "5" and self.direction != "Up":
            self.direction = "Down"
        elif key == "4" and self.direction != "Right":
            self.direction = "Left"
        elif key == "6" and self.direction != "Left":
            self.direction = "Right"

    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Up":
            new_head = (head[0], head[1] - self.block_size)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + self.block_size)
        elif self.direction == "Left":
            new_head = (head[0] - self.block_size, head[1])
        elif self.direction == "Right":
            new_head = (head[0] + self.block_size, head[1])

        self.snake = [new_head] + self.snake[:-1]

        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + self.block_size, segment[1] + self.block_size, fill="green", tags="snake")

    def check_collision(self):
        head = self.snake[0]
        if head[0] < 0 or head[0] >= self.canvas_width or head[1] < 0 or head[1] >= self.canvas_height:
            return True

        for segment in self.snake[1:]:
            if head == segment:
                return True

        return False

    def check_food(self):
        head = self.snake[0]
        food_coords = self.canvas.coords(self.food)
        if head == (food_coords[0], food_coords[1]):
            self.snake.append((0, 0))
            self.canvas.delete(self.food)
            self.food = self.create_food()
            self.score += 1
            self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")

            # Increase speed for unlimited mode every 10 foods eaten
            if self.difficulty == "unlimited":
                self.food_count += 1
                if self.food_count % 10 == 0:
                    self.speed -= 10

    def update(self):
        if self.game_running and not self.paused:
            self.move_snake()
            if self.check_collision():
                self.show_game_over()
            else:
                self.check_food()
                self.master.after(self.speed, self.update)

    def show_game_over(self):
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2, text=f"Game Over\nScore: {self.score}", fill="white", font=("Helvetica", 16), tags="game_over_text")
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 80, text="Press SPACE to play again!", fill="white", font=("Helvetica", 12), tags="game_over_text")
        self.insert_score(self.username, self.score)  # Insert score into database
        self.game_running = False

        # Add button to view leaderboard
        self.view_leaderboard_button = tk.Button(self.master, text="View Leaderboard", command=self.main_menu.view_leaderboard)
        self.view_leaderboard_button.pack()

class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game Main Menu")
        self.master.geometry("400x300")

        self.difficulty_label = tk.Label(self.master, text="Difficulty:")
        self.difficulty_label.pack()

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("normal")

        self.difficulty_menu = tk.OptionMenu(self.master, self.difficulty_var, "easy", "normal", "hard", "unlimited")
        self.difficulty_menu.pack()

        self.play_button = tk.Button(self.master, text="Play", command=self.start_game)
        self.play_button.pack(pady=10)

        self.leaderboard_button = tk.Button(self.master, text="View Leaderboard", command=self.view_leaderboard)
        self.leaderboard_button.pack(pady=10)

    def start_game(self):
        username = self.get_username()
        if username:
            difficulty = self.difficulty_var.get()
            self.master.withdraw()  # Hide main menu window
            game_window = tk.Toplevel(self.master)
            game_window.title("Snake Game")
            game = SnakeGame(game_window, self, username, difficulty)
            game_window.protocol("WM_DELETE_WINDOW", lambda: self.show_menu(username))
            game_window.mainloop()

    def get_username(self):
        username = tkinter.simpledialog.askstring("Username", "Enter your username:")
        return username

    def show_menu(self, username):
        self.master.deiconify()  # Show main menu window

    def view_leaderboard(self):
        leaderboard_window = tk.Toplevel(self.master)
        leaderboard_window.title("Leaderboard")
        leaderboard_window.geometry("300x300")

        label = tk.Label(leaderboard_window, text="Top 10 High Scores")
        label.pack()

        # Fetch high scores from database
        conn = sqlite3.connect('snake_game.db')
        cursor = conn.cursor()
        cursor.execute("SELECT player_name, score FROM high_scores ORDER BY score DESC LIMIT 10")
        scores = cursor.fetchall()
        for idx, (player_name, score) in enumerate(scores):
            label = tk.Label(leaderboard_window, text=f"{idx+1}. {player_name}: {score}")
            label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()
