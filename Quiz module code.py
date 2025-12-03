#Name: Meghna Tiwari
#Enrollment: 0103IS231109
#Batch: 5
#Batch Time: 10:30 a.m. to 12:10 p.m.

#3rd_assignment

import json
import os
import random
from datetime import datetime

# file names
user_file = "students.txt"
score_file = "scores.txt"

# global variables
logged_in = False
admin_mode = False
current_user = ""
user_data = {}

# load users
def load_users():
    global user_data
    if os.path.exists(user_file):
        try:
            with open(user_file, "r") as f:
                text = f.read().strip()
                if text:
                    user_data = json.loads(text)
                else:
                    user_data = {}
        except:
            user_data = {}
    else:
        user_data = {}

# save users
def save_users():
    with open(user_file, "w") as f:
        json.dump(user_data, f, indent=2)

# save score
def save_score(line):
    with open(score_file, "a") as f:
        f.write(line + "\n")

# read scores
def read_scores():
    if not os.path.exists(score_file):
        return []
    with open(score_file, "r") as f:
        return [x.strip() for x in f.readlines() if x.strip()]

# 10 python questions
python_quiz = [
    {"q": "Which keyword is used to make a function in Python?",
     "opt": ["func", "define", "def", "lambda"], "ans": "C"},
    {"q": "What will len('Python') return?",
     "opt": ["5", "6", "7", "Error"], "ans": "B"},
    {"q": "Which data type is immutable?",
     "opt": ["list", "tuple", "set", "dict"], "ans": "B"},
    {"q": "How are comments written in Python?",
     "opt": ["//", "#", "/*", "--"], "ans": "B"},
    {"q": "Output of 2 ** 4 is?",
     "opt": ["8", "12", "16", "Error"], "ans": "C"},
    {"q": "Which function is used to take input from user?",
     "opt": ["scan()", "input()", "get()", "enter()"], "ans": "B"},
    {"q": "Correct file extension for Python file is?",
     "opt": [".p", ".py", ".pt", ".python"], "ans": "B"},
    {"q": "Which symbol is used for floor division?",
     "opt": ["/", "//", "%", "**"], "ans": "B"},
    {"q": "Which keyword handles errors?",
     "opt": ["catch", "try", "except", "throw"], "ans": "C"},
    {"q": "Which function prints output in Python?",
     "opt": ["echo()", "display()", "show()", "print()"], "ans": "D"}
]

# 1. Registration
def register():
    print("\nStudent Registration ")
    uname = input("Create username: ").strip()
    if uname in user_data or uname.lower() == "admin":
        print("Username already exists.\n")
        return
    pwd = input("Create password: ").strip()
    name = input("Full Name: ")
    roll = input("Enrollment / Roll No: ")
    branch = input("Branch: ")
    year = input("Year: ")
    email = input("Email: ")
    phone = input("Phone: ")

    user_data[uname] = {
        "password": pwd,
        "name": name,
        "roll": roll,
        "branch": branch,
        "year": year,
        "email": email,
        "phone": phone
    }
    save_users()
    print("\nRegistration successful!\n")

# 2. Login (User/Admin)
def login():
    global logged_in, admin_mode, current_user
    print("\n Login ")
    uname = input("Username: ").strip()
    pwd = input("Password: ").strip()

    if uname == "admin" and pwd == "admin123":
        logged_in = True
        admin_mode = True
        current_user = "admin"
        print("\nAdmin logged in successfully.\n")
        return

    if uname in user_data and user_data[uname]["password"] == pwd:
        logged_in = True
        admin_mode = False
        current_user = uname
        print(f"\nWelcome {user_data[uname]['name']}!\n")
    else:
        print("Invalid username or password.\n")

# 3.2 Attempt Quiz
def attempt_quiz():
    if not logged_in or admin_mode:
        print("Login first as student.\n")
        return

    print("\nAttempting Python Quiz \n")
    random.shuffle(python_quiz)
    score = 0
    for i, q in enumerate(python_quiz, start=1):
        print(f"Q{i}. {q['q']}")
        for j, opt in zip(["A", "B", "C", "D"], q["opt"]):
            print(f"  {j}. {opt}")
        ans = input("Your answer (A/B/C/D): ").strip().upper()
        if ans == q["ans"]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! Correct answer: {q['ans']}\n")

    print(f"Quiz finished. You got {score}/10\n")
    roll = user_data[current_user]["roll"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{roll}\tPython\t{score}/10\t{time}"
    save_score(line)
    print("Your result has been saved.\n")

# 3.3 Score
def view_scores():
    if not logged_in or admin_mode:
        print("Login first as student.\n")
        return
    lines = read_scores()
    print("\n Your Scores ")
    roll = user_data[current_user]["roll"]
    found = False
    for l in lines:
        parts = l.split("\t")
        if len(parts) >= 4 and parts[0] == roll:
            found = True
            print(f"{parts[0]} | {parts[1]} | {parts[2]} | {parts[3]}")
    if not found:
        print("No score record found.\n")
    else:
        print()

# 3.4 Logout
def logout():
    global logged_in, admin_mode, current_user
    if logged_in:
        print(f"{current_user} logged out.\n")
    logged_in = False
    admin_mode = False
    current_user = ""

# 3.5 Update profile
def update_profile():
    if not logged_in or admin_mode:
        print("Login first as student.\n")
        return
    data = user_data[current_user]
    print("\n Update Profile  (press Enter to skip)")
    for key in ["name", "email", "branch", "year", "phone"]:
        new = input(f"{key.capitalize()} ({data[key]}): ").strip()
        if new != "":
            data[key] = new
    save_users()
    print("Profile updated successfully!\n")

# 3.6 Profile
def show_profile():
    if not logged_in or admin_mode:
        print("Login first as student.\n")
        return
    data = user_data[current_user]
    print("\n Profile ")
    for k, v in data.items():
        if k != "password":
            print(f"{k.capitalize()}: {v}")
    print()

# Admin View (for simplicity)
def admin_panel():
    print("\nAdmin Panel ")
    print("Registered Students:")
    for u, d in user_data.items():
        print(f"{u} - {d['name']} ({d['roll']})")
    print("\nAll Scores:")
    lines = read_scores()
    for l in lines:
        print(l)
    print()

# 3. Quiz Menu (All 3.x functions)
def quiz_menu():
    if not logged_in:
        print("Please login first.\n")
        return
    while logged_in and not admin_mode:
        print("\n Quiz Menu ")
        print("3.2 Attempt Quiz")
        print("3.3 View Score")
        print("3.4 Logout")
        print("3.5 Update Profile")
        print("3.6 View Profile")
        choice = input("Choose option (3.2 - 3.6): ").strip()
        if choice == "3.2":
            attempt_quiz()
        elif choice == "3.3":
            view_scores()
        elif choice == "3.4":
            logout()
            break
        elif choice == "3.5":
            update_profile()
        elif choice == "3.6":
            show_profile()
        else:
            print("Invalid choice.\n")

# 4. Exit
def exit_program():
    print("Thank you for using the Quiz App.")
    exit()

# Main Program
def main():
    load_users()
    while True:
        print("\nQUIZ APP with FILE HANDLING ")
        print("1. Registration")
        print("2. Login (User/Admin)")
        print("3. Quiz Menu")
        print("4. Exit")
        choice = input("Choose option (1-4): ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            login()
            if admin_mode:
                admin_panel()
        elif choice == "3":
            quiz_menu()
        elif choice == "4":
            exit_program()
        else:
            print("Invalid option. Try again.\n")

main()



