import tkinter
import pandas as pd
import random

current_card = {}
BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}


try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title,text="French",fill="black")
    canvas.itemconfig(card_word,text=current_card["French"],fill="black")
    canvas.itemconfig(card_back,image=card_front)
    flip_timer = window.after(3000,func=flip_card)

def flip_card():
    canvas.itemconfig(card_title,text="English",fill="white")
    canvas.itemconfig(card_word,text=current_card["English"])
    canvas.itemconfig(card_background,image=card_back)

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    next_card()
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv",index=False)
    next_card()


window = tkinter.Tk()
window.title("Flashcard Program")
window.config(pady=50,padx=50,bg=BACKGROUND_COLOR)

flip_timer = window.after(3000,func=flip_card)

canvas = tkinter.Canvas(height=526,width=800)
card_front = tkinter.PhotoImage(file="images/card_front.png")
card_back = tkinter.PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400,263,image=card_front)
card_title = canvas.create_text(400,150,text="",font=('Ariel',40,"italic"))
card_word = canvas.create_text(400,263,text="",font=("Ariel",60,"bold"))
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
canvas.grid(row=0,column=0,columnspan=2)

cross_image = tkinter.PhotoImage(file="images/wrong.png")
unknown_button = tkinter.Button(image=cross_image,command=next_card)
unknown_button.config(highlightthickness=0)
unknown_button.grid(row=1,column=0)

check_image = tkinter.PhotoImage(file="images/right.png")
right_button = tkinter.Button(image=check_image,command=is_known)
right_button.config(highlightthickness=0)
right_button.grid(row=1,column=1)

next_card()




window.mainloop()