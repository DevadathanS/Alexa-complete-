import datetime
import pyjokes
import pyttsx3
import pywhatkit
import speech_recognition as sr
import wikipedia
import webbrowser
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from vpython import *

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def wishUser():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        talk("Hi, Good Morning")
    elif 12 <= hour < 18:
        talk("Hi, Good Afternoon")
    else:
        talk("Hi, Good Evening")
    talk("I am Alexa. How can I help?")


def take_command():
    try:
        with sr.Microphone() as source:
            print("listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.capitalize()
            if "Alexa" in command:
                command = command.replace('Alexa', '')
                print(command)
    except:
        pass
    return command


def run_alexa():
    wishUser()
    command = take_command()
    print(command)
    if 'play music' in command:
        song = command.replace('play music','')
        pywhatkit.playonyt(song)
    elif 'time' in command:
        import datetime
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is ' + time)
    elif ' who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print('According to wikipedia, ' + info)
        talk('according to wikipedia, ' + info)
    elif 'joke' in command:
        j = pyjokes.get_joke()
        print(j)
        talk(j)
    elif 'who are you' in command:
        print("I am Alexa, your personal digital assistant")
        talk('I am Alexa, your personal digital assistant')
    elif 'thank' in command:
        print("It's my pleasure to work accordingly to your words")
        talk("It's my pleasure to work accordingly to your words")
    elif 'play a game' in command:
        print("Opening Surf Game...")
        talk('opening surf game')
        webbrowser.open('edge://surf')
    elif 'play a different game' in command:
        print('Opening Snake Game...')
        talk('opening snake game')
        # imports
        import turtle
        import time
        import random

        delay = 0.1

        # scores
        score = 0
        high_score = 0

        # set up screen
        wn = turtle.Screen()
        wn.title("Snake Game")
        wn.bgcolor('yellow')
        wn.setup(width=600, height=600)
        wn.tracer(0)

        # snake head
        head = turtle.Turtle()
        head.speed(0)
        head.shape("square")
        head.color("black")
        head.penup()
        head.goto(0, 0)
        head.direction = "stop"

        # snake food
        food = turtle.Turtle()
        food.speed(0)
        food.shape("square")
        food.color("red")
        food.penup()
        food.goto(0, 100)

        segments = []

        # scoreboards
        sc = turtle.Turtle()
        sc.speed(0)
        sc.shape("square")
        sc.color("black")
        sc.penup()
        sc.hideturtle()
        sc.goto(0, 260)
        sc.write("score: 0  High score: 0", align="center", font=("ds-digital", 24, "normal"))

        # Functions
        def go_up():
            if head.direction != "down":
                head.direction = "up"

        def go_down():
            if head.direction != "up":
                head.direction = "down"

        def go_left():
            if head.direction != "right":
                head.direction = "left"

        def go_right():
            if head.direction != "left":
                head.direction = "right"

        def move():
            if head.direction == "up":
                y_position = head.ycor()
                head.sety(y_position + 20)
            if head.direction == "down":
                y_position = head.ycor()
                head.sety(y_position - 20)
            if head.direction == "left":
                x_position = head.xcor()
                head.setx(x_position - 20)
            if head.direction == "right":
                x_position = head.xcor()
                head.setx(x_position + 20)

        # keyboard bindings
        wn.listen()
        wn.onkeypress(go_up, "w")
        wn.onkeypress(go_down, "s")
        wn.onkeypress(go_left, "a")
        wn.onkeypress(go_right, "d")

        # MainLoop
        while True:
            wn.update()

            # check collision with border area
            if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "stop"

                # hide the segments of body
                for segment in segments:
                    segment.goto(1000, 1000)  # out of range
                # clear the segments
                segments.clear()

                # reset score
                score = 0

                # reset delay
                delay = 0.1

                sc.clear()
                sc.write("score: {}  High score: {}".format(score, high_score), align="center",
                         font=("ds-digital", 24, "normal"))

            # check collision with food
            if head.distance(food) < 20:
                # move the food to random place
                x = random.randint(-290, 290)
                y = random.randint(-290, 290)
                food.goto(x, y)

                # add a new segment to the head
                new_segment = turtle.Turtle()
                new_segment.speed(0)
                new_segment.shape("square")
                new_segment.color("black")
                new_segment.penup()
                segments.append(new_segment)

                # shorten the delay
                delay -= 0.001
                # increase the score
                score += 10

                if score > high_score:
                    high_score = score
                sc.clear()
                sc.write("score: {}  High score: {}".format(score, high_score), align="center",
                         font=("ds-digital", 24, "normal"))

            # move the segments in reverse order
            for index in range(len(segments) - 1, 0, -1):
                x = segments[index - 1].xcor()
                y = segments[index - 1].ycor()
                segments[index].goto(x, y)
            # move segment 0 to head
            if len(segments) > 0:
                x = head.xcor()
                y = head.ycor()
                segments[0].goto(x, y)

            move()

            # check for collision with body
            for segment in segments:
                if segment.distance(head) < 20:
                    time.sleep(1)
                    head.goto(0, 0)
                    head.direction = "stop"

                    # hide segments
                    for segment in segments:
                        segment.goto(1000, 1000)
                    segments.clear()
                    score = 0
                    delay = 0.1

                    # update the score
                    sc.clear()
                    sc.write("score: {}  High score: {}".format(score, high_score), align="center",
                             font=("ds-digital", 24, "normal"))
            time.sleep(delay)
        wn.mainloop()
    elif 'play something else' in command:
        print('Opening Chicken Escape Game..')
        talk('opening chicken escape game')
        import pygame
        import random

        screen_size = [360, 600]
        screen = pygame.display.set_mode(screen_size)
        pygame.font.init()

        background = pygame.image.load('background.png')
        user = pygame.image.load('user.png')
        chicken = pygame.image.load('chicken.png')

        def display_score(score_obtained):
            font = pygame.font.SysFont('Comic Sans MS', 30)
            score_text = 'Score: ' + str(score_obtained)
            text_img = font.render(score_text, True, (0, 255, 0))
            screen.blit(text_img, [20, 10])

        def random_offset():
            return -1 * random.randint(100, 1500)

        chicken_y = [random_offset(), random_offset(), random_offset()]
        user_x = 150
        score = 0

        def crashed(idx):
            global score
            global keep_alive
            score = score - 50
            chicken_y[idx] = random_offset()
            if score < -500:
                keep_alive = False

        def update_chicken_pos(idx):
            global score
            if chicken_y[idx] > 600:
                chicken_y[idx] = random_offset()
                score = score + 5
                print('score', score)
            else:
                chicken_y[idx] = chicken_y[idx] + 5

        keep_alive = True
        clock = pygame.time.Clock()
        while keep_alive:
            pygame.event.get()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and user_x < 280:
                user_x = user_x + 10
            elif keys[pygame.K_LEFT] and user_x > 0:
                user_x = user_x - 10

            update_chicken_pos(0)
            update_chicken_pos(1)
            update_chicken_pos(2)

            screen.blit(background, [0, 0])
            screen.blit(user, [user_x, 520])
            screen.blit(chicken, [0, chicken_y[0]])
            screen.blit(chicken, [150, chicken_y[1]])
            screen.blit(chicken, [280, chicken_y[2]])

            if chicken_y[0] > 500 and user_x < 70:
                crashed(0)

            if chicken_y[1] > 500 and 80 < user_x < 200:
                crashed(1)

            if chicken_y[2] > 500 and user_x > 220:
                crashed(2)

            display_score(score)

            pygame.display.update()
            clock.tick(60)
    elif 'open clock' or 'show clock' in command:
        print('Opening Clock..')
        talk('opening clock')
        from time import strftime

        root = Tk()
        root.title("Python digital clock")

        def time():
            string = strftime('%I:%M:%S%p')
            label.config(text=string)
            label.after(1000, time)

        label = Label(root, font=("ds-digital", 80), background="black", foreground="cyan")
        label.pack(anchor="center")
        time()

        root.mainloop()
    elif 'take a screenshot' in command:
        print('Opening Screenshot taker...')
        talk('Opening Screenshot taker')
        import pyautogui
        import tkinter as tk

        root = tk.Tk()

        canvas1 = tk.Canvas(root, width=300, height=300)
        canvas1.pack()

        def takeScreenshot():
            myScreenshot = pyautogui.screenshot()
            save_path = asksaveasfilename()
            myScreenshot.save(save_path + "_screenshot.png")

        myButton = tk.Button(text="Take screenshot", command=takeScreenshot, font=10)
        canvas1.create_window(150, 150, window=myButton)
        root.title("Screenshot taker")

        root.mainloop()
    elif 'record screen' in command:
        print('Opening screen recorder...')
        talk('opening screen recorder')
        import datetime

        from PIL import ImageGrab
        import numpy as np
        import cv2
        from win32api import GetSystemMetrics

        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        file_name = f'{time_stamp}.mp4'
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        captured_video = cv2.VideoWriter(file_name, fourcc, 20.0, (width, height))

        webcam = cv2.VideoCapture(0)

        while True:
            img = ImageGrab.grab(bbox=(0, 0, width, height))
            img_np = np.array(img)
            img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            _, frame = webcam.read()
            fr_height, fr_width, _ = frame.shape
            img_final[0:fr_height, 0: fr_width, :] = frame[0: fr_height, 0: fr_width, :]
            cv2.imshow('Screen Recorder', img_final)

            # cv2.imshow('webcam', frame)

            captured_video.write(img_final)
            if cv2.waitKey(10) == ord('d'):
                break
    elif 'open mirror' in command:
        print('Opening mirror..')
        talk('opening mirror')
        import cv2
        cam = cv2.VideoCapture(0)
        while cam.isOpened():
            ret, frame = cam.read()
            if cv2.waitKey(10) == ord('h'):
                break
            cv2.imshow('Mirror', frame)
    elif 'open text editor' in command:
        print("Opening Text Editor...")
        talk('opening text editor')
        import sys
        import docx2txt

        class MainApp(QMainWindow):
            """ the main class of our app """

            def __init__(self):
                """ init things here """
                super().__init__()  # parent class initializer

                # window title
                self.title = "Google Doc Clone"
                self.setWindowTitle(self.title)

                # editor section
                self.editor = QTextEdit(self)
                self.setCentralWidget(self.editor)

                # create menubar and toolbar first
                self.create_menu_bar()
                self.create_toolbar()

                # after craeting toolabr we can call and select font size
                font = QFont('Times', 12)
                self.editor.setFont(font)
                self.editor.setFontPointSize(12)

                # stores path
                self.path = ''

            def create_menu_bar(self):
                menuBar = QMenuBar(self)

                """ add elements to the menubar """
                # App icon will go here
                app_icon = menuBar.addMenu(QIcon("doc_icon.png"), "icon")

                # file menu **
                file_menu = QMenu("File", self)
                menuBar.addMenu(file_menu)

                save_action = QAction('Save', self)
                save_action.triggered.connect(self.file_save)
                file_menu.addAction(save_action)

                open_action = QAction('Open', self)
                open_action.triggered.connect(self.file_open)
                file_menu.addAction(open_action)

                rename_action = QAction('Rename', self)
                rename_action.triggered.connect(self.file_saveas)
                file_menu.addAction(rename_action)

                pdf_action = QAction("Save as PDF", self)
                pdf_action.triggered.connect(self.save_pdf)
                file_menu.addAction(pdf_action)

                # edit menu **
                edit_menu = QMenu("Edit", self)
                menuBar.addMenu(edit_menu)

                # paste
                paste_action = QAction('Paste', self)
                paste_action.triggered.connect(self.editor.paste)
                edit_menu.addAction(paste_action)

                # clear
                clear_action = QAction('Clear', self)
                clear_action.triggered.connect(self.editor.clear)
                edit_menu.addAction(clear_action)

                # select all
                select_action = QAction('Select All', self)
                select_action.triggered.connect(self.editor.selectAll)
                edit_menu.addAction(select_action)

                # view menu **
                view_menu = QMenu("View", self)
                menuBar.addMenu(view_menu)

                # fullscreen
                fullscr_action = QAction('Full Screen View', self)
                fullscr_action.triggered.connect(lambda: self.showFullScreen())
                view_menu.addAction(fullscr_action)

                # normal screen
                normscr_action = QAction('Normal View', self)
                normscr_action.triggered.connect(lambda: self.showNormal())
                view_menu.addAction(normscr_action)

                # minimize
                minscr_action = QAction('Minimize', self)
                minscr_action.triggered.connect(lambda: self.showMinimized())
                view_menu.addAction(minscr_action)

                self.setMenuBar(menuBar)

            def create_toolbar(self):
                # Using a title
                ToolBar = QToolBar("Tools", self)

                # undo
                undo_action = QAction(QIcon("undo.png"), 'Undo', self)
                undo_action.triggered.connect(self.editor.undo)
                ToolBar.addAction(undo_action)

                # redo
                redo_action = QAction(QIcon("redo.png"), 'Redo', self)
                redo_action.triggered.connect(self.editor.redo)
                ToolBar.addAction(redo_action)

                # adding separator
                ToolBar.addSeparator()

                # copy
                copy_action = QAction(QIcon("copy.png"), 'Copy', self)
                copy_action.triggered.connect(self.editor.copy)
                ToolBar.addAction(copy_action)

                # cut
                cut_action = QAction(QIcon("cut.png"), 'Cut', self)
                cut_action.triggered.connect(self.editor.cut)
                ToolBar.addAction(cut_action)

                # paste
                paste_action = QAction(QIcon("paste.png"), 'Paste', self)
                paste_action.triggered.connect(self.editor.paste)
                ToolBar.addAction(paste_action)

                # adding separator
                ToolBar.addSeparator()
                ToolBar.addSeparator()

                # fonts
                self.font_combo = QComboBox(self)
                self.font_combo.addItems(
                    ["Courier Std", "Hellentic Typewriter Regular", "Helvetica", "Arial", "SansSerif", "Helvetica",
                     "Times", "Monospace"])
                self.font_combo.activated.connect(self.set_font)  # connect with function
                ToolBar.addWidget(self.font_combo)

                # font size
                self.font_size = QSpinBox(self)
                self.font_size.setValue(12)
                self.font_size.valueChanged.connect(self.set_font_size)  # connect with funcion
                ToolBar.addWidget(self.font_size)

                # separator
                ToolBar.addSeparator()

                # bold
                bold_action = QAction(QIcon("bold.png"), 'Bold', self)
                bold_action.triggered.connect(self.bold_text)
                ToolBar.addAction(bold_action)

                # underline
                underline_action = QAction(QIcon("underline.png"), 'Underline', self)
                underline_action.triggered.connect(self.underline_text)
                ToolBar.addAction(underline_action)

                # italic
                italic_action = QAction(QIcon("italic.png"), 'Italic', self)
                italic_action.triggered.connect(self.italic_text)
                ToolBar.addAction(italic_action)

                # separator
                ToolBar.addSeparator()

                # text alignment
                right_alignment_action = QAction(QIcon("right-align.png"), 'Align Right', self)
                right_alignment_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
                ToolBar.addAction(right_alignment_action)

                left_alignment_action = QAction(QIcon("left-align.png"), 'Align Left', self)
                left_alignment_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
                ToolBar.addAction(left_alignment_action)

                justification_action = QAction(QIcon("justification.png"), 'Center/Justify', self)
                justification_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
                ToolBar.addAction(justification_action)

                # separator
                ToolBar.addSeparator()

                # zoom in
                zoom_in_action = QAction(QIcon("zoom-in.png"), 'Zoom in', self)
                zoom_in_action.triggered.connect(self.editor.zoomIn)
                ToolBar.addAction(zoom_in_action)

                # zoom out
                zoom_out_action = QAction(QIcon("zoom-out.png"), 'Zoom out', self)
                zoom_out_action.triggered.connect(self.editor.zoomOut)
                ToolBar.addAction(zoom_out_action)

                # separator
                ToolBar.addSeparator()

                self.addToolBar(ToolBar)

            def italic_text(self):
                # if already italic, change into normal, else italic
                state = self.editor.fontItalic()
                self.editor.setFontItalic(not (state))

            def underline_text(self):
                # if already underlined, change into normal, else underlined
                state = self.editor.fontUnderline()
                self.editor.setFontUnderline(not (state))

            def bold_text(self):
                # if already bold, make normal, else make bold
                if self.editor.fontWeight() != QFont.Bold:
                    self.editor.setFontWeight(QFont.Bold)
                    return
                self.editor.setFontWeight(QFont.Normal)

            def set_font(self):
                font = self.font_combo.currentText()
                self.editor.setCurrentFont(QFont(font))

            def set_font_size(self):
                value = self.font_size.value()
                self.editor.setFontPointSize(value)

                # we can also make it one liner without writing such function.
                # by using lamba function -
                # self.font_size.valueChanged.connect(self.editor.setFontPointSize(self.font_size.value()))

            def file_open(self):
                self.path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                           "Text documents (*.text);Text documents (*.txt);All files (*.*)")

                try:
                    # with open(self.path, 'r') as f:
                    #    text = f.read()
                    text = docx2txt.process(self.path)  # docx2txt
                    # doc = Document(self.path)         # if using docx
                    # text = ''
                    # for line in doc.paragraphs:
                    #    text += line.text
                except Exception as e:
                    print(e)
                else:
                    self.editor.setText(text)
                    self.update_title()

            def file_save(self):
                print(self.path)
                if self.path == '':
                    # If we do not have a path, we need to use Save As.
                    self.file_saveas()

                text = self.editor.toPlainText()

                try:
                    with open(self.path, 'w') as f:
                        f.write(text)
                        self.update_title()
                except Exception as e:
                    print(e)

            def file_saveas(self):
                self.path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                                                           "text documents (*.text);Text documents (*.txt);All files (*.*)")

                if self.path == '':
                    return  # If dialog is cancelled, will return ''

                text = self.editor.toPlainText()

                try:
                    with open(path, 'w') as f:
                        f.write(text)
                        self.update_title()
                except Exception as e:
                    print(e)

            def update_title(self):
                self.setWindowTitle(self.title + ' ' + self.path)

            def save_pdf(self):
                f_name, _ = QFileDialog.getSaveFileName(self, "Export PDF", None, "PDF files (.pdf);;All files()")
                print(f_name)

                if f_name != '':  # if name not empty
                    printer = QPrinter(QPrinter.HighResolution)
                    printer.setOutputFormat(QPrinter.PdfFormat)
                    printer.setOutputFileName(f_name)
                    self.editor.document().print_(printer)

        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        sys.exit(app.exec_())
    elif 'play some different game' in command:
        print("Opening Guessing Game...")
        talk('opening guessing game')
        import random
        secret_number = int(random.randint(0, 10))
        guess_count = 0
        guess_limit = 3

        print("""
        Instructions and rules:
        The instructions and rules of this game are very simple;
        You just have to guess a number within three chances you got
        You will have a hint at your third chance if you couldn't guess the number at the first two chances
        If you do not want to use the hint, no problem
        You can just simply press enter if you do not need the hint
        If you are bored, enter tired or quit to exit the game
        If you win -> Congratulations 
        If not -> Try again and use the hint at your third chance
        So go on and try your luck
        """)

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

        rate = engine.getProperty('rate')
        engine.setProperty('rate', 180)
        engine.say("""
        Instructions and rules:
        The instructions and rules of this game are very simple;
        You just have to guess a number within three chances you got
        You will have a hint at your third chance if you couldn't guess the number at the first two chances
        If you do not want to use the hint, no problem
        You can just simply press enter if you do not need the hint
        If you are bored, enter tired or quit to exit the game
        If you win, Congratulations 
        If not, Try again and use the hint at your third chance
        So go on and try your luck
        """)
        engine.runAndWait()

        while guess_count < guess_limit:
            guess = int(input('Guess: '))
            guess_count += 1
            if guess == secret_number:
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[1].id)
                engine.say("You have guessed the correct number!")
                engine.say("You have won the guessing game!")
                print("You have guessed the correct number!!!")
                print("Yay! You won")
                engine.runAndWait()
                break
            elif guess_count == 1:
                engine.say("Sorry, your answer is wrong, Try again...")
                engine.say("You have only 2 chances left....")
                engine.runAndWait()
                print("Sorry, your answer is wrong.Try again...")
                print("You have only 2 chances left....")
                print("")
            elif guess_count == 2:
                engine.say("Sorry, your answer is wrong, Try again...")
                engine.say("Last and final chance for you..")
                engine.runAndWait()
                print("Sorry, your answer is wrong.Try again...")
                print("Last and final chance for you...")
                print("")
                engine.say("Type 'h' if you need one hint, Else simply press enter")
                engine.runAndWait()
                h = input("Type 'h' if you need one hint. Else simply press enter: ")
                if h == "h".lower():
                    engine.say("The secret number is divided by 2...")
                    engine.say(f"The hint number is {secret_number / 2}")
                    engine.runAndWait()
                    print("The secret number is divided by 2...")
                    print(secret_number / 2)
                print("")
            elif "quit" or "tired" in guess:
                break

        else:
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            print("Sorry, you failed!")
            print("Better luck next time!!")
            engine.say("Sorry, you have lost!!")
            engine.say("Better luck next time So try again!")
            engine.say(f"The correct number is {secret_number}")
            print(f"The correct number is {secret_number}")
            engine.runAndWait()
    elif 'open weight converter' in command:
        print('Opening Weight Converter...')
        talk('opening weight converter')
        weight = int(input("Weight: "))
        unit = input("(L)bs or (K)g: ")
        if unit.upper() == "L":
            converted = weight * 0.45
            engine.say(f"You are {converted} kilos")
            print(f"You are {converted} kilos")
            engine.runAndWait()
        elif unit.upper() == "K":
            converted = weight / 0.45
            engine.say(f"You are {converted} pounds")
            print(f"You are {converted} pounds")
        else:
            engine.say("You have entered an invalid operator!")
            print("You have entered an invalid operator!")
            engine.runAndWait()
        engine.say("Thank you for using me")
        print("Thank you for using me !")
        engine.runAndWait()
    elif 'open simple calculator' in command:
        print('Opening simple calculator...')
        talk('opening simple calcualtor')

        def add(a, b):
            result = a + b
            print(result)

        def sub(a, b):
            result = a - b
            print(result)

        def mul(a, b):
            result = a * b
            print(result)

        def div(a, b):
            result = a / b
            print(result)

        a = int(input("Enter the first number: "))
        b = int(input("Enter the second number: "))
        op = input("Enter the operator: ")

        if op == "+":
            add(a, b)
        elif op == "-":
            sub(a, b)
        elif op == "*":
            mul(a, b)
        elif op == "/":
            div(a, b)
        else:
            print("Invalid Operator")
    elif 'search' in command:
        se = command.replace('search', '')
        print('Opening Google...')
        talk('opening google')
        webbrowser.open("https://www.google.co.in/search?q=" + str(se))
    elif 'open google' in command:
        print('Opening Google...')
        talk('opening google')
        webbrowser.open('https://www.google.com')
    elif 'open youtube' in command:
        print("Opening Youtube..")
        talk('opening youtube')
        webbrowser.open('https://www.youtube.com')
    elif 'open gmail' in comamnd:
        print('Opening Gmail..')
        talk('opening gmail')
        webbrowser.open('https://www.gmail.google.com')
    elif 'open meet' in command:
        print('Opening Meet...')
        talk('opening meet')
        webbrowser.open('https://www.meet.google.com')
    elif 'open play store' in command:
        print('Opening Play Store...')
        talk('opening playstore')
        webbrowser.open('https://www.play.google.com/store')
    elif 'open whatsapp' in command:
        print('Opening Whatsapp...')
        talk('opening whatsapp')
        webbrowser.open('https://www.web.whatsapp.com')
    elif 'open telegram' in command:
        print('Opening Telegram...')
        talk('opening telegram')
        webbrowser.open("https://web.telegram.im/#/im?p=")
    elif 'open inpixio' in command:
        print("Opening Inpixio...")
        talk("opening inpixio")
        webbrowser.open('https://www.inpixio.com')
    elif 'open youtube history' in command:
        print('Opening youtube....')
        talk("opening youtube")
        webbrowser.open('https://www.youtube.com/feed/history')
    elif 'open python.org' or 'open python official website' in command:
        print('Opening python.org')
        talk('opening python.org')
        webbrowser.open('https://www.python.org')
    elif 'open pypi website' in comamnd:
        print("Opening pypi website...")
        talk('opening pypi website')
        webbrowser.open('https://pypi.org')
    elif 'open clock' or 'show clock' in command:
        print('Opening clock...')
        talk('opening clock')
        from time import strftime

        root = Tk()
        root.title("Clock")

        def time():
            string = strftime('%I:%M:%S%p')
            label.config(text=string)
            label.after(1000, time)

        label = Label(root, font=("ds-digital", 80), background="black", foreground="cyan")
        label.pack(anchor="center")
        time()

        root.mainloop()
    elif 'show donut' in command:
        print('Your donut is getting ready...')
        talk("your donut is getting ready")
        canvas(background=color.purple)
        donut = ring(radius=0.5, thickness=0.25, color=vector(400, 100, 1))
        chocolate = ring(radius=0.55, thickness=0.25, color=vector(0.4, 0.2, 0))
        rad = 0
        while True:
            rate(50)
            donut.pos = vector(3 * cos(rad), sin(rad), 0)
            chocolate.pos = vector(3 * cos(rad), sin(rad), 0)
            rad = rad + 0.03
    elif 'move mouse automatically' in command:
        print("Moving mouse automatically...")
        talk('moving mouse automatically')
        import pyautogui
        import time
        pyautogui.FAILSAFE = False
        while True:
            time.sleep(10)
            for i in range(0, 10):
                pyautogui.moveTo(0, i * 5)
            for i in range(0, 3):
                pyautogui.press('shift')
    elif 'open messenger automation' in command:
        print("Automating messenger message")
        talk("Automating messenger message")
        import pyautogui
        import time
        while True:
            time.sleep(3)
            pyautogui.typewrite('Good Evening....')
            pyautogui.press('enter')
    elif 'open python friend' in command:
        print("Opening python friend..")
        talk("opening python friend")
        import pyttsx3
        friend = pyttsx3.init()
        speech = input('Say something: ')
        friend.say(speech)
        friend.runAndWait()
    elif 'show weather forecast' in command:
        print('Opening weather forecast...')
        talk("opening weather forecast")
        import tkinter as tk
        import requests
        import time

        def getWeather(canvas):
            city = textField.get()
            api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=06c921750b9a82d8f5d1294e1586276f"

            json_data = requests.get(api).json()
            condition = json_data['weather'][0]['main']
            temp = int(json_data['main']['temp'] - 273.15)
            min_temp = int(json_data['main']['temp_min'] - 273.15)
            max_temp = int(json_data['main']['temp_max'] - 273.15)
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']
            sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600))
            sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600))

            final_info = condition + "\n" + str(temp) + "°C"
            final_data = "\n" + "Min Temp: " + str(min_temp) + "°C" + "\n" + "Max Temp: " + str(
                max_temp) + "°C" + "\n" + "Pressure: " + str(pressure) + "\n" + "Humidity: " + str(
                humidity) + "\n" + "Wind Speed: " + str(
                wind) + "\n" + "Sunrise: " + sunrise + "\n" + "Sunset: " + sunset
            label1.config(text=final_info)
            label2.config(text=final_data)

        canvas = tk.Tk()
        canvas.geometry("600x500")
        canvas.title("Weather Forecast")
        f = ("poppins", 15, "bold")
        t = ("poppins", 35, "bold")

        textField = tk.Entry(canvas, justify='center', width=20, font=t)
        textField.pack(pady=20)
        textField.focus()
        textField.bind('<Return>', getWeather)

        label1 = tk.Label(canvas, font=t)
        label1.pack()
        label2 = tk.Label(canvas, font=f)
        label2.pack()
        canvas.mainloop()

    else:
        print("I don't know that..")
        talk("I don't know that")


run_alexa()
