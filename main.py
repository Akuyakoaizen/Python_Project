import os
import math
import time
import random
from datetime import datetime

USER_CREDENTIALS_FILE = 'user_credentials.txt'
USER_LOGS_FOLDER = 'user_logs'

netflix_movies = {}


def load_movies_from_file():
    global netflix_movies
    netflix_movies = {}

    if os.path.exists("listmovie.txt"):
        with open("listmovie.txt", "r") as file:
            lines = file.readlines()
            for idx, line in enumerate(lines):

                line = line.strip()
                if not line or "| Genre:" not in line or "| Year:" not in line:
                    print(f"Skipping malformed line at index {idx}: {line}")
                    continue

                try:
                    parts = line.split(" | ")
                    name = parts[0].split(": ")[1]
                    genre = parts[1].split(": ")[1]
                    year = int(parts[2].split(": ")[1])


                    netflix_movies[idx + 1] = {"name": name, "genre": genre, "year": year}
                except IndexError:
                    print(f"Skipping malformed line at index {idx}: {line}")
                    continue
    else:
        print("No existing movie data found, starting with an empty list.")



def save_movies_to_file():
    global netflix_movies  # Access the global variable
    with open("listmovie.txt", "w") as file:
        for movie_info in netflix_movies.values():
            file.write(f"Name: {movie_info['name']} | Genre: {movie_info['genre']} | Year: {movie_info['year']}\n")

# Function to search for a movie by name
def search_movie(movie_name):
    movie_name = movie_name.lower()
    matched_movies = [movie_info for movie_info in netflix_movies.values() if movie_name in movie_info["name"].lower()]
    return matched_movies

# Log search results to file
def log_search_to_file(username, movie_name, results):
    base_path = f"user_logs/{username}"

    if not os.path.exists(base_path):
        print(f"Error: User folder for {username} does not exist!")
        return

    log_file = os.path.join(base_path, "search_movies.txt")

    with open(log_file, "a") as file:
        if results:
            for movie in results:
                file.write(f"Search Query: {movie_name} - Found: {movie['name']} | Genre: {movie['genre']} | Year: {movie['year']}\n")
        else:
            file.write(f"Search Query: {movie_name} - Movie not found\n")

# Function to display all movies
def print_all_movies():
    global netflix_movies  # Access the global variable
    print("\nList of All Movies:")
    for movie_id, movie_info in netflix_movies.items():
        print(f"{movie_id}. {movie_info['name']} | Genre: {movie_info['genre']} | Year: {movie_info['year']}")

# Function to add a new movie to the dictionary
def add_movie():
    global netflix_movies  # Access the global variable
    new_id = max(netflix_movies.keys()) + 1 if netflix_movies else 1
    name = input("Enter movie name: ")
    genre = input("Enter movie genre: ")
    year = input("Enter movie year: ")
    new_movie = {
        "name": name,
        "genre": genre,
        "year": int(year)
    }
    netflix_movies[new_id] = new_movie
    print(f"\nMovie '{name}' added successfully!")

    # After adding a movie, save all movies to listmovie.txt
    save_movies_to_file()

# User search function
def user_search(username):
    movie_name = input("Enter the movie name to search: ")
    results = search_movie(movie_name)

    if results:
        for movie in results:
            print(f"Found: {movie['name']} - Genre: {movie['genre']} - Year: {movie['year']}")
    else:
        print("Movie not found!")

    log_search_to_file(username, movie_name, results)

# Main application function
def netflix_app(username):
    global netflix_movies  # Access the global variable
    print("Welcome to the Netflix app!")

    # Load the movies from the file at the start
    load_movies_from_file()

    while True:
        print("\n1. Search Movie")
        print("2. Add Movie")
        print("3. Print All Movies")
        print("4. Exit")

        choice = input("Enter choice (1-4): ")

        if choice == '1':
            user_search(username)

        elif choice == '2':
            add_movie()

        elif choice == '3':
            print_all_movies()

        elif choice == '4':
            print("Exiting the app.")
            break

        else:
            print("Invalid choice. Please try again.")



# Function to create a user folder and necessary files
def create_user_folder(username):
    folder_path = os.path.join(USER_LOGS_FOLDER, username)
    os.makedirs(folder_path, exist_ok=True)

    user_log_file = os.path.join(folder_path, 'user_log.txt')
    todo_list_file = os.path.join(folder_path, 'todo_list.txt')
    number_guessing_log_file = os.path.join(folder_path, 'number_guessing_log.txt')

    if not os.path.exists(user_log_file):
        with open(user_log_file, 'w') as f:
            f.write("User log started.\n")

    if not os.path.exists(todo_list_file):
        with open(todo_list_file, 'w') as f:
            f.write("To-Do List (incomplete tasks)\n")

    if not os.path.exists(number_guessing_log_file):
        with open(number_guessing_log_file, 'w') as f:
            f.write("Number Guessing Game Log\n")

    return folder_path

# Log user interaction with timestamp
def log_user_interaction(username, message):
    folder_path = os.path.join(USER_LOGS_FOLDER, username)
    log_file = os.path.join(folder_path, 'user_log.txt')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, 'a') as f:
        f.write(f"{current_time} - {message}\n")

# Log number guessing game result (win or loss)
def log_number_guessing_result(username, attempts, result, number):
    folder_path = os.path.join(USER_LOGS_FOLDER, username)
    log_file = os.path.join(folder_path, 'number_guessing_log.txt')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, 'a') as f:
        f.write(f"{current_time} - Game Result: {result} | Number: {number} | Attempts: {attempts}\n")

# Log a to-do list task with deadline and completion status
def log_todo_list_task(username, task, deadline, completed=False):
    folder_path = os.path.join(USER_LOGS_FOLDER, username)
    log_file = os.path.join(folder_path, 'todo_list.txt')

    with open(log_file, 'a') as f:
        status = "Completed" if completed else "Incomplete"
        f.write(f"{task} | Deadline: {deadline} | Status: {status}\n")

# Function to handle user login
def login():
    print("==========================================")
    print("|| \tLogin to your account. 👨‍💼       ||")
    print("==========================================")
    print("__________________________________________")
    username = input("Username: ")
    print("__________________________________________")
    password = input("Password: ")
    print("__________________________________________")

    try:
        with open(USER_CREDENTIALS_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                stored_username, stored_password = line.strip().split(',')
                if username == stored_username and password == stored_password:
                    print("Login successful!")
                    log_user_interaction(username, f"User {username} logged in.")
                    return username
    except FileNotFoundError:
        print("User credentials file not found. Please register first.")
    print("\n======================================")
    print("||   Invalid username or password.  ||")
    print("======================================\n\n\n\n\n")
    return None

# Function to handle user registration
def register():
    print("\n\n==========================================")
    print("||        Register Account 📝           ||")
    print("==========================================")
    print("__________________________________________")
    username = input("Choose a username: ")
    print("__________________________________________")
    password = input("Choose a password: ")
    print("__________________________________________\n\n")

    try:
        with open(USER_CREDENTIALS_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                stored_username, _ = line.strip().split(',')
                if username == stored_username:
                    print("\n\n==========================================")
                    print("||        Username already taken.       ||")
                    print("||    Please choose a different one.    ||")
                    print("==========================================\n\n")
                    return None
    except FileNotFoundError:
        pass


    with open(USER_CREDENTIALS_FILE, 'a') as f:
        f.write(f"{username},{password}\n")

    create_user_folder(username)
    print("\n\n==========================================")
    print("||      Account created successfully     ||")
    print(f"||           for {username}!           ||")
    print("========================================")
    log_user_interaction(username, f"User {username} registered an account.")
    return username

# CLI To-Do List Application
def todo_list(username):
    tasks = []
    folder_path = os.path.join(USER_LOGS_FOLDER, username)
    todo_file = os.path.join(folder_path, 'todo_list.txt')
    completed_file = os.path.join(folder_path, 'completed_task.txt')


    os.makedirs(folder_path, exist_ok=True)
    if not os.path.exists(todo_file):
        open(todo_file, 'a').close()
    if not os.path.exists(completed_file):
        open(completed_file, 'a').close()


    with open(todo_file, 'r') as f:
        tasks = f.readlines()

    while True:
        print("\n==========================================")
        print("||      Welcome to your To-Do List!     ||")
        print("==========================================")
        print("==========================================")
        print("||           [1] Add Task ➕            ||")
        print("||           [2] View Tasks 📝          ||")
        print("||           [3] Exit app 🔚            ||")
        print("==========================================")
        print("\n__________________________________________")
        choice = input("Enter choice (1-3): ")

        if choice == '1':
            task = input("Enter your task: ")
            deadline = input("Enter deadline (yyyy-mm-dd): ")
            log_todo_list_task(username, task, deadline)
            print("==========================================")
            print(f"||Task '{task}' with deadline '{deadline}'||")
            print("||          added to your list.          ||")
            print("==========================================")
        elif choice == '2':
            if not tasks:
                print("\n==========================================")
                print("||           No tasks available.         ||")
                print("==========================================")
            else:
                print("\n==========================================")
                print("||           Your To-Do List:           ||")
                print("==========================================")
                for index, task in enumerate(tasks, start=1):
                    print(f"{index}. {task.strip()}")
                print("\n_______________________________________________________________________________________________")
                task_number = int(input("Select a task number to view or update its status (0 to go back): "))

                if task_number == 0:
                    continue

                if task_number < 1 or task_number > len(tasks):
                    print("Invalid task number. Please try again.")
                    continue


                selected_task = tasks[task_number - 1].strip()
                print(f"\nSelected Task: {selected_task}")


                print("1. Mark as Completed")
                print("2. Go back to task list")
                action_choice = input("Enter your choice (1-2): ")

                if action_choice == '1':
                    task_details = selected_task.split(" | ")
                    task = task_details[0]
                    deadline = task_details[1].replace("Deadline: ", "").strip()
                    completion_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Move task to completed file
                    with open(completed_file, 'a') as cf:
                        cf.write(f"{task} | Deadline: {deadline} | Completed on: {completion_date}\n")

                    # Remove task from todo file
                    tasks.pop(task_number - 1)
                    with open(todo_file, 'w') as tf:
                        tf.writelines(tasks)

                    print(f"Task '{task}' marked as Completed and moved to 'completed_task.txt'.")
                elif action_choice == '2':
                    continue
                else:
                    print("\n==========================================")
                    print("||   Invalid choice. Please try again.    ||")
                    print("==========================================")

        elif choice == '3':
            print("\n==========================================")
            print("||      Exiting To-Do List. Goodbye!      ||")
            print("==========================================")
            break
        else:
             print("\n==========================================")
             print("||   Invalid choice. Please try again.    ||")
             print("==========================================")


# Log a to-do list task with deadline
def log_todo_list_task(username, task, deadline):
    folder_path = os.path.join(USER_LOGS_FOLDER, username)
    todo_file = os.path.join(folder_path, 'todo_list.txt')

    with open(todo_file, 'a') as f:
        f.write(f"{task} | Deadline: {deadline} | Status: Incomplete\n")






def number_guessing_game(username):
    print("\n==========================================")
    print("|| Welcome to the Number Guessing Game! ||")
    print("==========================================")

    while True:
        number = random.randint(1, 100)
        attempts = 0

        while attempts < 10:
            guess = int(input("Guess the number between 1 and 100: "))
            attempts += 1

            if guess < number:
                print("Too low! Try again.")
            elif guess > number:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                log_number_guessing_result(username, attempts, "Win", number)
                break
        else:
            print(f"Sorry, you've used all 10 attempts. The correct number was {number}.")
            log_number_guessing_result(username, attempts, "Loss", number)

        play_again = input("Do you want to play again? (y/n): ")
        if play_again.lower() != 'y':
            log_user_interaction(username, f"User {username} exited Number Guessing Game.")
            print(f"Goodbye, {username}! Thanks for playing!")
            break



def log_calculation_to_file(username, operation, num1, num2, result):
    folder_path = os.path.join(USER_LOGS_FOLDER, username)
    if not os.path.exists(folder_path):  # Ensure the directory exists
        os.makedirs(folder_path)

    todo_file = os.path.join(folder_path, 'calculation_history.txt')

    with open(todo_file, 'a') as f:
        f.write(f"{username}: {operation} | {num1} and {num2} = {result}\n")



# Calculator Application
def calculator(username):
    def add(x, y): return x + y
    def subtract(x, y): return x - y
    def multiply(x, y): return x * y
    def divide(x, y): return x / y if y != 0 else "Error! Division by zero."
    def power(x, y): return x ** y
    def square_root(x): return math.sqrt(x) if x >= 0 else "Error! Square root of negative number."

    print("\n==========================================")
    print("||    Welcome to the Calculator!🧮🔢    || ")
    print("==========================================")

    while True:
        print("\n==========================================")
        print("||   Select an operation:✖️➗➕➖🟰       ||")
        print("==========================================")
        print("||  [1]. Add (+)                        ||")
        print("||  [2]. Subtract (-)                   ||")
        print("||  [3]. Multiply (*)                   ||")
        print("||  [4]. Divide (/)                     ||")
        print("||  [5]. Power (x^y)                    ||")
        print("||  [6]. Square Root (√x)               ||")
        print("||  [7]. Exit                           ||")
        print("==========================================")

        choice = input("Enter choice (1-7): ")

        if choice == '7':
            log_calculation_to_file(username, "Exit", "N/A", "N/A", "User logged out")
            break

        if choice in ['1', '2', '3', '4', '5', '6']:
            num1 = float(input("Enter first number: "))

        if choice in ['1', '2', '3', '4', '5']:
            num2 = float(input("Enter second number: "))

        if choice == '1':
            result = add(num1, num2)
            operation = "Addition"
        elif choice == '2':
            result = subtract(num1, num2)
            operation = "Subtraction"
        elif choice == '3':
            result = multiply(num1, num2)
            operation = "Multiplication"
        elif choice == '4':
            result = divide(num1, num2)
            operation = "Division"
        elif choice == '5':
            result = power(num1, num2)
            operation = "Power"
        elif choice == '6':
            result = square_root(num1)
            operation = "Square Root"
        else:
            print("Invalid input. Please try again.")
            continue

        print(f"Result: {result}")

        log_calculation_to_file(username, operation, num1, num2 if choice != '6' else "N/A", result)


# Main menu after login
def main_menu(username):
    while True:
        print("\n\n==========================================")
        print("||           Main Menu Apps 📱          ||")
        print("==========================================")
        print("||  [1]. Calculator 📅                  ||")
        print("||  [2]. To-Do List 📝                  ||")
        print("||  [3]. Number Guessing Game 🤔        ||")
        print("||  [4]. Netflix App 🎬🍿               ||")
        print("||  [5]. Logout 🔚                      ||")
        print("==========================================")


        choice = input("Enter choice (1-6): ")

        if choice == '1':
            calculator(username)
        elif choice == '2':
            todo_list(username)
        elif choice == '3':
            number_guessing_game(username)
        elif choice == '4':
            netflix_app(username)
        elif choice == '5':
            log_user_interaction(username, f"User {username} logged out.")
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

# Main entry point
if __name__ == "__main__":
    while True:
        print("===============================================================================================================")
        print('||     M       M   OOOOOOOO   BBBBBBBB  IIIIIII     LL       EEEEEEEE           AAAAA   PPPPPPP   PPPPPPP    ||')
        print('||     MM     MM  OO      OO  BB     B     II       LL       EE                AA   AA  PP    PP  PP    PP   ||')
        print('||     M M   M M  O        O  BBBBBBB      II       LL       EEEEEEEE          AAAAAAA  PPPPPPP   PPPPPPP    ||')
        print('||     M  M M  M  OO      OO  BB     B     II       LL       EE                AA   AA  PP        PP         ||')
        print('||     M   M   M   OOOOOOOO   BBBBBBBB   IIIIIII    LLLLLLL  EEEEEEEE          AA   AA  PP        PP         ||')
        print("===============================================================================================================\n\n")
        print("==========================================")
        print("||                                      ||")
        print("||   Welcome! Please choose an option:  ||")
        print("||                                      ||")
        print("==========================================")
        print("==========================================")
        print("||                                      ||")
        print("|| \t[1] Login      🔒               ||")
        print("|| \t[2] Register   📋               ||")
        print("|| \t[3] Exit       🔚               ||")
        print("||                                      ||")
        print("==========================================")
        print("__________________________________________")
        option = input("Enter your choice (1-3): ")

        if option == '1':
            user = login()
            if user:
                main_menu(user)
        elif option == '2':
            user = register()
            if user:
                main_menu(user)
        elif option == '3':
            print("==========================================")
            print("||       Pwede na matulog? yey 😴       ||")
            print("==========================================")
            exit()
        else:
            print("==========================================")
            print("||        1 to 3 ngalang diba?          ||")
            print("||         Bigwasan kita tamo           ||")
            print("==========================================")
