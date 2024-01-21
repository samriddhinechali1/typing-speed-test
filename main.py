from tkinter import *
from tkinter import messagebox
import random
import keyboard
BACKGROUND_COLOR = "#1A374D"
BUTTON_COLOR = "#6998AB"
TEXT_COLOR = "#B1D0E0"
EXTRA_COLOR = "#406882"


class MainScreen:

    def __init__(self):
        # Main Window
        self.window = Tk()
        self.window.title("Typing Speed Test App")
        self.window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

        # Application widgets
        self.label = Label()
        self.generated_text = Text()
        self.entry_field = Entry()
        self.user_entry = Entry()
        self.mistake_value = Label()
        self.wpm_value = Label()
        self.cpm_value = Label()

        # Application's variables
        self.timer_text = None
        self.time = None
        self.points = 0
        self.time_start = False
        self.set_of_words = []
        self.written_words = []
        self.text = ""
        self.entry_text = ""
        self.spelling = []
        self.spelling_points = 0
        self.mistakes = 0
        self.words_points = 0
        self.net_wpm = 0
        self.difference = 0

        # Creates the screen at the very start
        self.start_page()
        self.window.mainloop()

    def start_page(self):
        # Starting Page that shows the instruction on what to do next

        self.main_label = Label(text="Test your typing speed abilities", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Arial", 25))
        self.main_label.grid(column=0, row=0, columnspan=3, pady=20, padx=50)

        start = Button(text="Start test", bg="#85E6C5", fg=BACKGROUND_COLOR, highlightthickness=0,
                            font=("Arial", 20), command=lambda: [self.create_text(), start.destroy(), info.destroy()])
        start.grid(column=1, row=2, pady=50, padx=20)

        info = Button(text="INSTRUCTION", bg=BUTTON_COLOR, fg=BACKGROUND_COLOR,
                      font=("Arial", 18, "bold"), command=lambda: [self.show_info(),
                                                                   start.destroy(), info.destroy()])
        info.grid(column=1, row=1, pady=50)

    def show_info(self):
        self.main_label.config(text="Welcome to Typing Speed Test!")
        text_info = Label(font=("Arial", 18), bg=BACKGROUND_COLOR, fg=TEXT_COLOR, anchor=W, justify="left",
                          text="This app allows you to check your typing speed.\n"
                               "Press on start test to commence forward.\n"
                               "Once you start typing, the timer will start.\n"
                               "After each word, type a SINGLE SPACE.\n"
                               "After you write the texts in the screen, the test \n"
                               "will end after the timer hits a minute \n"
                               "and the app will count and provide you with the results.\n"
                               "The app saves the highest score automatically.\n"
                               "WPM - Words Per Minute, CPM - Characters per minute, \n"
                               "NET WPM - WPM with counted mistakes.\n"
                               "Hard - This takes you to the difficult level.")
        text_info.grid(column=0, row=1, pady=20)

        msg_luck = Label(text="HAPPY TYPING", font=("Arial", 20, "bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        msg_luck.grid(column=0, row=2, pady=20)

        go_back = Button(text="GO BACK", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=("Arial", 18),
                         command=lambda: [self.clear_screen(),
                                          self.start_page(),
                                          text_info.destroy(),
                                          go_back.destroy(), msg_luck.destroy(),
                                          self.main_label.config(text="Test your typing speed abilities")])
        go_back.grid(column=0, row=3)

    def create_text(self):
        self.main_label.config(text="Type away!!")
        self.clear_screen()
        self.create_widgets()

        with open('common_words.txt', "r") as text:
            all_text = text.read()
            words = list(map(str, all_text.split()))

            for word in range(30):
                self.set_of_words.append(random.choice(words).lower())
            self.generated_text = Text(self.window, fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Arial", 20, "bold"),
                                       height=4, width=60, wrap="word")
            self.generated_text.grid(column=0, row=1, columnspan=9, pady=30)
            self.generated_text.insert(END, self.change_into_text(self.set_of_words).lower())

    def change_into_text(self, list_of_words):
        text = ' '.join(list_of_words)
        self.text = text
        return text

    def clear_screen(self):

        # Clears the screen and destroys the widgets
        self.main_label.destroy()
        self.set_of_words.clear()
        self.generated_text.destroy()
        self.spelling.clear()
        self.entry_field.delete(0, END)
        self.spelling_points = 0
        self.set_of_words.clear()
        self.text = ""
        self.window.update()

    def text_callback(self, var, index, mode):
        """Calls methods which checks spelling, updates Screen Board and
        start timer, by tracing an input in an Entry Widget"""

        self.entry_text = self.entry_field.get()
        # self.check_spelling()

        self.start_timer()
        self.check_spelling()
        self.update_scoreboard()

    def count_points(self):
        points = 0
        for check in self.spelling:
            if check == "correct":
                points += 1
            else:
                pass
        if len(self.spelling) == 0:
            points = 0
        return points

    def count_mistakes(self):
        mistakes = 0
        for check in self.spelling:
            if check == "wrong":
                mistakes += 1
            else:
                pass
        if len(self.spelling) == 0:
            mistakes = 0
        return mistakes

    def show_error(self, difference):
        """Changes a wrongly typed letter to the color red"""
        len_entry = len(self.entry_text) - 1 - difference
        self.generated_text.tag_config("#ff0000", foreground='#ff0000')
        letter = self.entry_text[len_entry]
        self.generated_text.delete(f"1.{len_entry}", f"1.{len_entry + 1}")
        self.generated_text.insert(f"1.{len_entry}", letter)
        self.generated_text.tag_add('#ff0000', f"1.{len_entry}")

    def show_correct(self, difference):
        """Changes a correctly typed letter to the color green"""
        len_entry = len(self.entry_text) - 1 - difference
        self.generated_text.tag_config("#65B741", foreground="#65B741")
        letter = self.entry_text[len_entry]
        self.generated_text.delete(f"1.{len_entry}", f"1.{len_entry + 1}")
        self.generated_text.insert(f"1.{len_entry}", letter)
        self.generated_text.tag_add("#65B741", f"1.{len_entry}")

    def show_real_text(self, difference):
        """Shows original letter in white color when backspace is pressed"""
        self.generated_text.tag_config("#fafafa", foreground="#fafafa")
        letter = self.text[len(self.entry_text)]
        self.generated_text.delete(f"1.{len(self.entry_text)}")
        self.generated_text.insert(f"1.{len(self.entry_text)}", letter)
        self.generated_text.tag_add("#fafafa", f"1.{self.entry_text}")

    def check_spelling(self):
        letters = []
        string_letters = ""
        number = -1
        self.points = 0
        try:
            for letter in self.entry_text.lower():
                if letter != " ":
                    self.points += 1
                    number += 1
                    # print(letter)
                else:
                    number = -1
                letters.append(letter)
                string_letters = ''.join(letters)
            self.written_words = string_letters.split(" ")
            self.words_points = len(self.written_words)
            if len(self.written_words[self.words_points - 1]) > len(self.set_of_words[self.words_points - 1]):
                number -= 1
                self.difference = len(self.written_words[self.words_points - 1])\
                - len(self.set_of_words[self.words_points - 1])
                self.written_words.pop()
                self.written_words.append(self.written_words[self.words_points -1][:-self.difference])

            if keyboard.read_key() != "backspace":
                # Stops the program after it hits 60 seconds and also disables the entry field
                if self.timer_text['text'] == 60:
                    self.time_start = False
                    self.entry_field.config(state='disabled')
                    self.count_score()
                if self.written_words[self.words_points - 1][number] == self.set_of_words[self.words_points - 1][number]:
                    self.spelling.append("correct")
                    self.show_correct(self.difference)
                    self.spelling_points = self.count_points()
                    self.mistakes = self.count_mistakes()
                else:
                    self.spelling.append("wrong")
                    self.show_error(self.difference)
                    self.spelling_points = self.count_points()
                    self.mistakes = self.count_mistakes()
            else:
                self.show_real_text()
        except IndexError:
            pass

    def restart(self):
        """Restarts the whole app to the main screen"""
        try:
            self.window.destroy()
            self.window.after_cancel(self.time)
            MainScreen()
        except ValueError:
            MainScreen()

    def count_down(self, count):
        if self.time_start:
            self.time = self.window.after(1000, self.count_down, count + 1)
            self.timer_text['text'] = count

    def start_timer(self):
        if len(self.entry_text) == 1:
            self.time_start = True
            self.count_down(0)
        elif len(self.entry_text) == 0:
            self.time_start = False
        # Disallow users to write after 1 minute
        # if self.timer_text['text'] == 60:
        #     self.time_start = False
        #     self.entry_field.config(state='disabled')

    def update_scoreboard(self):
        """Updates all the scoreboard as time changes"""
        self.cpm_value['text'] = self.points
        if int(self.timer_text['text']) > 0:
            self.net_wpm = int(self.points / 5 - ((self.mistakes * int(self.timer_text['text'])) / 60) /
                               (int(self.timer_text['text'])/ 60))
            self.wpm_value['text'] = f"{int((self.points / 5) - (int(self.timer_text['text'])/60))}/" \
                                     f"{self.net_wpm}"
        self.mistake_value['text'] = self.mistakes
        if int(self.mistake_value['text']) > 0:
            self.mistake_value.config(fg="#ff0000")
        elif int(self.mistake_value['text']) == 0:
            self.mistake_value.config(fg="#fafafa")

    def count_score(self):
        """Shows the end scores and accuracy in a messagebox after a minute is up"""
        self.time_start = False
        cpm = int(self.points)
        wpm = int((self.points / 5) / ((int(self.timer_text['text']))/ 60))
        net_wpm = (int(((self.points / 5) - (self.mistakes * ((int(self.timer_text['text'])) / 60))) /
                       ((int(self.timer_text['text'])) / 60)))
        accuracy = (net_wpm * 100) / wpm
        messagebox.showinfo("End", f"CPM is: {cpm}.\n"
                                   f"WPM is: {wpm}, \n"
                                   f"Net WPM is: {net_wpm}.\n"
                                   f"Accuracy is: {'%.2f' % accuracy}.")

    def create_widgets(self):
        # characters per minute
        cpm_label = Label(text=f"CPM: ", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Arial", 14))
        cpm_label.grid(column=2, row=0, sticky=E)
        self.cpm_value = Label(text="0", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Arial", 14))
        self.cpm_value.grid(column=3, row=0, sticky=W)

        # words per minute

        wpm_label = Label(text=f"WPM: ", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Arial", 14))
        wpm_label.grid(column=4, row=0, sticky=E)
        self.wpm_value = Label(text="0", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Arial", 14))
        self.wpm_value.grid(column=5, row=0, sticky=W)

        # Mistakes

        mist_label = Label(text=f"MISTAKES: ", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Arial", 14))
        mist_label.grid(column=6, row=0, sticky=E)
        self.mistake_value = Label(text="0", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Arial", 14))
        self.mistake_value.grid(column=7, row=0, sticky=W)

        # Timer

        timer_label = Label(text=f"TIME: ", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Arial", 14))
        timer_label.grid(column=0, row=0, sticky=E)
        self.timer_text = Label(text="0", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Arial", 14))
        self.timer_text.grid(column=1, row=0, sticky=W)

        # Entry field
        entry_label = Label(text=f"WRITE BELOW: ", width=15, fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Arial", 14))
        entry_label.grid(column=1, row=5)
        self.user_entry = StringVar()

        self.user_entry.trace_add('write', self.text_callback)
        self.entry_field = Entry(self.window, width=95, textvariable=self.user_entry, bg=EXTRA_COLOR, fg=TEXT_COLOR,
                                 font=("Arial", 12, "bold"))
        self.entry_field.grid(column=1, row=6, columnspan=8, pady=15)
        self.entry_field.bind("<BackSpace>")

        # restart Button
        restart = Button(text="RESTART", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Arial", 14)
                         , command=self.restart)
        restart.grid(column=8, row=7)


screen = MainScreen()
