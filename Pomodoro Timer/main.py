import tkinter as tk
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#f4775a"
GREEN = "#4ba559"
YELLOW = "#f7f5dd"
WHITE = "#ffffff"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
phase = 0
work_session = 0
timer = 'pending'
paused = False
count = 0


def pomodoro():

    # ---------------------------- RESET MECHANISM ------------------------------- #

    def reset_timer():
        global phase
        global work_session
        global paused
        global count
        canvas.itemconfig(timer_text, text=f"00:00")
        paused = False
        phase = 0
        work_session = 0
        window.after_cancel(timer)
        action.config(text="Press Start")
        start_button.config(text="Start", command=initial_start)

    # ---------------------------- TIMER MECHANISM ------------------------------- #

    def initial_start():
        start_button.config(text="Pause", command=pause_timer)
        start_timer()

    def start_timer():
        global phase
        global work_session
        global count
        global paused
        window.attributes('-topmost', 1)
        window.attributes('-topmost', 0)
        if paused:
            paused = False
            start_button.config(text="Pause", command=pause_timer)
            countdown()
        else:
            phase += 1
            if phase == 9:
                phase = 0
                work_session = 0
            if phase % 2 == 1:
                count = WORK_MIN * 60
                countdown()
                action.config(text="Work", fg=GREEN)
            else:
                action.config(text="Break", fg=RED)
                if phase == 8:
                    count = LONG_BREAK_MIN * 60
                    countdown()
                    work_session += 1
                    show_checkmark.config(text=checkmark * work_session)
                else:
                    count = SHORT_BREAK_MIN * 60
                    countdown()
                    work_session += 1
                    show_checkmark.config(text=checkmark * work_session)

    def pause_timer():
        global paused
        window.after_cancel(timer)
        start_button.config(text="Resume", command=start_timer)
        paused = True

    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

    def countdown():
        global timer
        global count
        canvas.itemconfig(timer_text, text=f"{math.floor(count / 60):02d}:{count % 60:02d}")
        if count > 0:
            count -= 1
            timer = window.after(1000, countdown)
        else:
            start_timer()

    # ---------------------------- UI SETUP ------------------------------- #

    window = tk.Tk()
    window.title("Pomodoro Timer")
    window.config(padx=50, pady=25, bg=YELLOW)
    window.geometry('500x440')

    canvas = tk.Canvas(width=205, height=224, bg=YELLOW, highlightthickness=0)
    tomato_img = tk.PhotoImage(file="tomato.png")
    canvas.create_image(100, 112, image=tomato_img)
    timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

    checkmark = "🗸"
    show_checkmark = tk.Label(text='', bg=YELLOW, fg=GREEN, font=(FONT_NAME, 20, "bold"))

    action = tk.Label(text="Press Start", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, "bold"))

    start_button = tk.Button(text="Start", bg=GREEN, font=(FONT_NAME, 10, "bold"),
                             highlightthickness=0, command=initial_start)
    reset_button = tk.Button(text="Reset", bg=GREEN, font=(FONT_NAME, 10, "bold"),
                             highlightthickness=0, command=reset_timer)

    # ---visual layout--- #
    window.rowconfigure(index=0, weight=1)
    window.rowconfigure(index=1, weight=1)
    window.rowconfigure(index=2, weight=1)
    window.rowconfigure(index=3, weight=1)
    window.columnconfigure(index=0, weight=1)
    window.columnconfigure(index=1, weight=1)
    window.columnconfigure(index=2, weight=1)

    canvas.grid(column=1, row=1)
    show_checkmark.grid(column=1, row=3)
    start_button.grid(column=0, row=2, columnspan=2, sticky='nw')
    reset_button.grid(column=1, row=2, columnspan=2, sticky='ne')
    action.grid(column=0, row=0, columnspan=3, pady=10)

    window.mainloop()


if __name__ == "__main__":
    pomodoro()
