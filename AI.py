import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import sqlite3

# Create and connect to SQLite database
conn = sqlite3.connect('shopping_assistant.db')
cursor = conn.cursor()

# Create tables for clothing and electronics
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clothing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        cost TEXT,
        image TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Electronics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        cost TEXT,
        image TEXT
    )
''')

# Sample data insertion into Clothing table
clothing_data = [
    ("T-shirt", "$20", r"D:\\VSPYTHON.python\\project\\mock_images\\tshirt.jpg"),
    ("Jeans", "$50", r"D:\\VSPYTHON.python\\project\\mock_images\\jeans.jpg"),
    ("Jacket", "$80", r"D:\\VSPYTHON.python\\project\\mock_images\\jacket.jpg"),
    ("Sweater", "$30", r"D:\\VSPYTHON.python\\project\\mock_images\\sweater.jpg"),
    ("Dress", "$60", r"D:\\VSPYTHON.python\\project\\mock_images\\dress.jpg")
]

cursor.executemany('INSERT INTO Clothing (name, cost, image) VALUES (?, ?, ?)', clothing_data)

# Sample data insertion into Electronics table
electronics_data = [
    ("Smartphone", "$600", r"D:\\VSPYTHON.python\\project\\mock_images\\smartphone.jpg"),
    ("Laptop", "$1200", r"D:\\VSPYTHON.python\\project\\mock_images\\laptop.jpg"),
    ("Headphones", "$150", r"D:\\VSPYTHON.python\\project\\mock_images\\headphones.jpg"),
    ("Smartwatch", "$300", r"D:\\VSPYTHON.python\\project\\mock_images\\smartwatch.jpg"),
    ("Camera", "$800", r"D:\\VSPYTHON.python\\project\\mock_images\\camera.jpg")
]

cursor.executemany('INSERT INTO Electronics (name, cost, image) VALUES (?, ?, ?)', electronics_data)

conn.commit()  # Commit the changes

# Predefined available items from database
def fetch_clothing_items():
    cursor.execute("SELECT name, cost, image FROM Clothing")
    return cursor.fetchall()

def fetch_electronics_items():
    cursor.execute("SELECT name, cost, image FROM Electronics")
    return cursor.fetchall()

clothing_items = fetch_clothing_items()
electronics_items = fetch_electronics_items()

# GUI Implementation (Same as before but using data from the database)
unrecognized_questions = []

def open_chat_window():
    chat_window = tk.Toplevel(root)
    chat_window.title("AI-Powered Virtual Personal Shopping Assistant")
    
    chat_display = scrolledtext.ScrolledText(chat_window, wrap=tk.WORD, width=50, height=20)
    chat_display.pack(pady=10)
    
    user_entry = tk.Entry(chat_window, width=40)
    user_entry.pack(pady=5)
    
    chat_display.insert(tk.END, "Bot: Hi! How can I assist you today?\n")
    
    def send_message():
        user_input = user_entry.get().strip().lower()
        chat_display.insert(tk.END, "You: " + user_input + "\n")
        user_entry.delete(0, tk.END)
        
        if user_input in ["hi", "hello"]:
            chat_display.insert(tk.END, "Bot: Hi! How can I assist you today?\n")
        elif user_input in ["i need help"]:
            chat_display.insert(tk.END, "Bot: I can only help you with problems related to clothing and electronics.\n")
        elif user_input in ["i need clothing", "show me clothing", "recommend clothing", "clothing"]:
            chat_display.insert(tk.END, "Bot: Here are the available clothing items:\n")
            for item in clothing_items:
                item_button = tk.Button(chat_window, text=item[0], command=lambda i=item: show_item_details(chat_display, i))
                chat_display.window_create(tk.END, window=item_button)
                chat_display.insert(tk.END, "\n")
        elif user_input in ["electronics", "i need electronics", "show me electronics", "recommend electronics"]:
            chat_display.insert(tk.END, "Bot: Here are the available electronics items:\n")
            for item in electronics_items:
                item_button = tk.Button(chat_window, text=item[0], command=lambda i=item: show_item_details(chat_display, i))
                chat_display.window_create(tk.END, window=item_button)
                chat_display.insert(tk.END, "\n")
        elif user_input in ["what can you do?", "how can you help me?"]:
            chat_display.insert(tk.END, "Bot: I can help you find clothing and electronics. Just ask for recommendations or browse the items you're interested in!\n")
        elif user_input in ["thank you", "thanks"]:
            chat_display.insert(tk.END, "Bot: You're welcome! If you have any more questions, feel free to ask.\n")
        elif user_input in ["goodbye", "bye"]:
            chat_display.insert(tk.END, "Bot: Goodbye! Have a great day!\n")
        else:
            unrecognized_questions.append(user_input)
            chat_display.insert(tk.END, f"Bot: I'm not sure how to respond to '{user_input}'. Please try asking for 'clothing' or 'electronics' recommendations.\n")
            with open('unrecognized_questions.txt', 'a') as f:
                f.write(f"{user_input}\n")

    send_button = tk.Button(chat_window, text="Send", command=send_message)
    send_button.pack()

def show_item_details(chat_display, item):
    chat_display.delete('1.0', tk.END)
    image_path = item[2]
    print(f"Loading image from: {image_path}")  # Debugging statement
    try:
        img = Image.open(image_path)
        img = img.resize((150, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        chat_display.image_create(tk.END, image=photo)
        chat_display.image = photo  # Keep a reference to avoid garbage collection
        chat_display.insert(tk.END, "\n")
    except FileNotFoundError:
        chat_display.insert(tk.END, "Image not found.\n")
    except Exception as e:
        chat_display.insert(tk.END, f"Error loading image: {e}\n")

    chat_display.insert(tk.END, f"Bot: You clicked on {item[0]}.\n")
    chat_display.insert(tk.END, f"Cost: {item[1]}\n")

root = tk.Tk()
root.title("Chatbot Launcher")
chatbot_button = tk.Button(root, text="💬", font=("Helvetica", 24), command=open_chat_window)
chatbot_button.pack(pady=20)
root.mainloop()

# Close the database connection when the program ends
conn.close()
