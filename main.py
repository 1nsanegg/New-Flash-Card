import random
from tkinter import *
import pandas
from random import randint
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
# Read data from csv

# take data from word_to_learn file
# if file not found, take data from french_words
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# Delete the word
def is_known():
    """remove the current card from the list, save new list to word_to_learn file"""
    to_learn.remove(current_card)
    print(len(to_learn))
    new_data = pandas.DataFrame(to_learn)

    # delete index from the new file
    new_data.to_csv("data/words_to_learn.csv", index=False)

    random_word()


# Flip card
def flip_card():
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(language_source, text="English", fill="white")
    canvas.itemconfig(word,text=current_card["English"],fill="white")


# Random word
def random_word():
    # random_number = randint(1,len(data) - 1)
    # random_word = data.loc[random_number, "French"]
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    current_word = current_card["French"]
    canvas.itemconfig(card, image=card_font)
    canvas.itemconfig(language_source, text="French",fill="black")
    canvas.itemconfig(word, text=current_word, fill="black")

    flip_timer = window.after(3000, flip_card)


# UI set up
window = Tk()
window.title("Flash Card App")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)
canvas = Canvas(width=800, height=526)
card_font = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400,263,image=card_font)
canvas.grid(row=0, column=0, columnspan = 2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
language_source = canvas.create_text(400,150, fill="black", font=("Ariel", 40, "italic"))
word = canvas.create_text(400,263, fill="black", font=("Ariel", 60, "bold"))

right_img = PhotoImage(file="images/right.png")
right_btn = Button(image=right_img,highlightthickness=0,command=is_known)
right_btn.grid(row=1,column=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong_img, highlightthickness=0, command=random_word)
wrong_btn.grid(row=1, column=0)


random_word()


window.mainloop()