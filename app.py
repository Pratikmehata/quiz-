# Online Quiz Application
# Save as: app.py
# Run with: python3 app.py

import tkinter as tk
from tkinter import messagebox
import json
import os

quiz_data = {
    "Python": [
        {"question": "What does 'len()' do?", 
         "options": ["Returns length", "Adds two numbers", "Prints string", "None"], 
         "answer": "Returns length"},
        {"question": "Which keyword is used to define a function?", 
         "options": ["define", "func", "def", "function"], 
         "answer": "def"},
        {"question": "What is the output of 'print(2**3)'?", 
         "options": ["6", "8", "9", "Error"], 
         "answer": "8"},
        {"question": "Which of the following is a tuple?", 
         "options": ["[1, 2, 3]", "(1, 2, 3)", "{1, 2, 3}", "{\"a\": 1}"], 
         "answer": "(1, 2, 3)"},
        {"question": "Which data type is immutable?", 
         "options": ["List", "Dictionary", "Tuple", "Set"], 
         "answer": "Tuple"}
    ],
    "Networking": [
        {"question": "What does HTTP stand for?", 
         "options": ["HyperText Transfer Protocol", "HighText Transfer Protocol", 
                    "HyperText Transmission Protocol", "None"], 
         "answer": "HyperText Transfer Protocol"},
        {"question": "What is the default port for HTTP?", 
         "options": ["80", "443", "22", "21"], 
         "answer": "80"},
        {"question": "Which device routes traffic between networks?", 
         "options": ["Switch", "Router", "Hub", "Modem"], 
         "answer": "Router"},
        {"question": "What does IP stand for?", 
         "options": ["Internet Protocol", "Internal Protocol", 
                    "International Protocol", "Input Protocol"], 
         "answer": "Internet Protocol"},
        {"question": "Which protocol is used to send emails?", 
         "options": ["SMTP", "FTP", "SNMP", "HTTP"], 
         "answer": "SMTP"}
    ]
}

LEADERBOARD_FILE = "leaderboard.json"

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Quiz App")
        self.username = ""
        self.topic = ""
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.timer_seconds = 60  # 1 minute timer
        self.timer_id = None
        self.init_login_screen()

    def init_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter your name:").pack(pady=10)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)
        tk.Button(self.root, text="Continue", command=self.choose_topic).pack(pady=10)

    def choose_topic(self):
        self.username = self.name_entry.get().strip()
        if not self.username:
            messagebox.showerror("Error", "Please enter your name.")
            return
        self.clear_screen()
        tk.Label(self.root, text=f"Hello {self.username}, choose a topic:").pack(pady=10)
        for topic in quiz_data:
            tk.Button(self.root, text=topic, command=lambda t=topic: self.start_quiz(t)).pack(pady=5)

    def start_quiz(self, topic):
        self.topic = topic
        self.questions = quiz_data[topic]
        self.current_question = 0
        self.score = 0
        self.timer_seconds = 60
        self.show_question()
        self.start_timer()

    def show_question(self):
        self.clear_screen()
        if self.current_question >= len(self.questions):
            self.end_quiz()
            return

        q_data = self.questions[self.current_question]
        tk.Label(self.root, text=f"Time Left: {self.timer_seconds}s", font=("Arial", 12), fg="red").pack()
        tk.Label(self.root, text=f"Q{self.current_question+1}: {q_data['question']}", wraplength=400).pack(pady=10)

        self.selected_option = tk.StringVar()
        for opt in q_data["options"]:
            tk.Radiobutton(self.root, text=opt, variable=self.selected_option, value=opt).pack(anchor='w')

        tk.Button(self.root, text="Submit", command=self.check_answer).pack(pady=10)

    def check_answer(self):
        selected = self.selected_option.get()
        correct = self.questions[self.current_question]["answer"]
        if selected == correct:
            self.score += 1
        self.current_question += 1
        self.show_question()

    def start_timer(self):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_id = self.root.after(1000, self.start_timer)
        else:
            self.end_quiz()

    def end_quiz(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.clear_screen()
        tk.Label(self.root, text=f"{self.username}, you scored {self.score}/{len(self.questions)}").pack(pady=10)
        self.update_leaderboard()
        self.show_leaderboard()
        tk.Button(self.root, text="Try Again", command=self.init_login_screen).pack(pady=10)

    def show_leaderboard(self):
        leaderboard = self.load_leaderboard()
        tk.Label(self.root, text="Leaderboard (Top 5):").pack()
        sorted_scores = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:5]
        for name, score in sorted_scores:
            tk.Label(self.root, text=f"{name}: {score}").pack()

    def update_leaderboard(self):
        leaderboard = self.load_leaderboard()
        leaderboard[self.username] = max(self.score, leaderboard.get(self.username, 0))
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(leaderboard, f)

    def load_leaderboard(self):
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
        return {}

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")
    app = QuizApp(root)
    root.mainloop()