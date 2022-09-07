from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
clock_timer = None

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    window.after_cancel(clock_timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer.configure(text="Timer")
    check_label.config(text="")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global reps
    reps += 1

    work_seconds = WORK_MIN * 60
    short_break_seconds = SHORT_BREAK_MIN * 60
    long_break_seconds = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_seconds)
        timer.config(text="Break", fg=RED)

    elif reps % 2 == 0:
        count_down(short_break_seconds)
        timer.config(text="Break", fg=PINK)

    else:
        count_down(work_seconds)
        timer.config(text="Working", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
# One solution below (can't use this because of the mainloop screen "listening" for updates -> use window.after()
# import time
# count = 5
# while true:
#     time.sleep(1)
#     count -= 5

# def say_something(a, b, c):
#     print(a)
#     print(b)
#     print(c)
#
# window.after(time_in_milliseconds, function_to_execute, *args)
# window.after(1000, say_something, 3, 4, 6)


def count_down(count):
    count_min = math.floor(count / 60)  # gives us number of whole minutes
    count_sec = count % 60  # gives us remaining seconds, but at 0 seconds it says :0 instead of :00
    # Dynamic Typing:
    if 9 < count_sec < 60:
        canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")  # (the item you're configuring, and the attribute)
    elif count_sec < 10:
        canvas.itemconfig(timer_text, text=f"{count_min}:0{count_sec}")  # (the item you're configuring, and the attribute)

    if count > 0:
        global clock_timer
        clock_timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        check_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Canvas Widget -> allows us to place an image onto program and then place text on top of it
canvas = Canvas(width=200, height=300, bg=YELLOW, highlightthickness=0)  # looked at size of tomato image
tomato_img = PhotoImage(file="tomato.png")  # if image is stored in a diff folder, provide file path exactly
canvas.create_image(100, 112, image=tomato_img)  # (X position, Y position, image)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 28, "bold"))
canvas.grid(column=1, row=1)

timer = Label(text="Timer", fg=RED, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
timer.grid(column=1, row=0)

start_button = Button(text="Start", font=(FONT_NAME, 10), command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", font=(FONT_NAME, 10), command=reset_timer)
reset_button.grid(column=2, row=2)

check_label = Label(fg=RED, bg=YELLOW, highlightthickness=0, font=(FONT_NAME, 10, "bold"))
check_label.grid(column=1, row=3)


window.mainloop()

