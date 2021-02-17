from tkinter import filedialog, messagebox, END, Frame, Label, Toplevel, Text, Button, Menu, WORD, Scrollbar, \
    Listbox
from tkinter.tix import Tk
from PIL import Image
from PIL import ImageTk
from nltk import word_tokenize
from pymorphy2 import MorphAnalyzer
from help import HELPTEXT
import win32api
import pickle

vocabulary = []


def newFile():
    global vocabulary
    vocabulary = []
    outputText.delete(0, END)


def saveFile():
    file_path = filedialog.asksaveasfilename()
    if file_path != "":
        f = open(file_path, 'wb')
        pickle.dump(outputText.get(0, END), f)
        f.close()


def openFile():
    global vocabulary
    file_path = filedialog.askopenfilename()
    if file_path != "":
        f = open(file_path, 'rb')
        words = pickle.load(f)
        for i in range(len(words)):
            outputText.insert(0, str(words[i]))
        f.close()


def printFile():
    file_path = filedialog.askopenfilename()
    print(file_path)
    if file_path:
        win32api.ShellExecute(0, 'print', file_path, None, '.', 0)


def cleanWord():
    global outputText
    if outputText:
        answer = messagebox.askyesno(
            title="Вопрос",
            message="Вы уверены, что хотите очистить словарь?")
        if answer:
            outputText.delete(0, END)


def addWord():
    global vocabulary
    words = {}
    analyzer = MorphAnalyzer()
    vocabulary.append(inputText.get(1.0, END))
    tokenize_sentence = word_tokenize(vocabulary[0])
    for word in tokenize_sentence:
        parse_word = analyzer.parse(word)[0]
        word_word = parse_word.word
        word_lemma = parse_word.normal_form
        word_tags = parse_word.tag.cyr_repr
        word_ending = list(set(word_word) - set(word_lemma))
        if word_word is not word_lemma:
            words.update({word_word: {'lemma': word_lemma, 'tag': word_tags, 'ending': word_ending}})
    sorted_words = sorted(words)
    for key in sorted_words:
        outputText.insert(0, str(words[key]['lemma']) + '      ' + str(words[key]['tag']) + '      ' \
                          + str(words[key]['ending']))
    vocabulary.clear()


def helpMenu():
    children = Toplevel()
    children.title('Helper')
    children.geometry("450x300+300+300")
    outputHelpText = Text(children, height=15, width=54)
    scrollb = Scrollbar(children, command=outputHelpText.yview)
    scrollb.grid(row=4, column=4, sticky='nsew')
    outputHelpText.grid(row=4, column=0, sticky='nsew', columnspan=3)
    outputHelpText.configure(yscrollcommand=scrollb.set)
    outputHelpText.insert('end', HELPTEXT)
    outputHelpText.configure(state='disabled')


def aboutProgramMenu():
    children = Toplevel()
    children.title('About program')
    lemmaLabel = Label(children, text='Я после этой ночи')
    lemmaLabel.pack()
    photo = ImageTk.PhotoImage(Image.open("about.jpg"))
    imageLabel = Label(children, image=photo)
    imageLabel.image = photo
    imageLabel.pack()


def generateForm():
    global generated_form
    analyzer = MorphAnalyzer()
    lemma_text = lemmaText.get(1.0, END).replace('\n', "")
    lemma_for_generate = analyzer.parse(lemma_text)[0]
    tags_text = tagsText.get(1.0, END).replace('\n', "")
    s = tags_text
    tags_for_generate = s.replace(',', '').split()

    if lemma_text or tags_text:
        children = Toplevel()
        children.title('Generated word')
        children.geometry("300x150+300+300")
        started_temporary_generated_form = lemma_for_generate.inflect({tags_for_generate[0]})
        for i in range(len(tags_for_generate)):
            over_temporary_generated_form = started_temporary_generated_form.inflect({tags_for_generate[i]})
            generated_form = over_temporary_generated_form
            print(generated_form)
        lemmaLabel = Label(children, text=generated_form.word)
        lemmaLabel.pack(padx=10, pady=30)
    else:
        messagebox.showerror(
            "Ошибка",
            "Заполните поля")


def generateWord():
    children = Toplevel()
    children.geometry("420x200+300+300")
    global lemmaText
    lemmaFrame = Frame(children, bd=10)
    lemmaLabel = Label(lemmaFrame, text='Лексема', width=7, height=2)
    lemmaLabel.pack(side='left')
    lemmaText = Text(lemmaFrame, height=1, width=20)
    lemmaText.pack(side='right')
    global tagsText
    tagsFrame = Frame(children, bd=10)
    tagsLabel = Label(tagsFrame, text='Тэги', width=7, height=2)
    tagsLabel.pack(side='left')
    tagsText = Text(tagsFrame, height=1, width=20)
    tagsText.pack(side='right')
    childrenFrame = Frame(children, bd=10)
    generateFormButton = Button(childrenFrame, text='Сгенерировать', width=25, height=2)
    generateFormButton.config(command=generateForm)
    generateFormButton.pack(side='right')

    children.title('Генерация слова')
    lemmaFrame.pack(side='top')
    tagsFrame.pack(side='top')
    childrenFrame.pack(side='bottom')


class App(Tk):
    def __init__(self):
        super().__init__()
        # -----------------------------------------INPUT--------------------------------------------------
        global inputText
        inputFrame = Frame(self, bd=10)
        inputText = Text(inputFrame, height=8, width=80, wrap=WORD)
        # -------------------------------------------OUTPUT------------------------------------------------
        global outputText
        outputFrame = Frame(self, bd=0)
        outputText = Listbox(outputFrame, height=10, width=120)
        scrollb = Scrollbar(outputFrame, command=outputText.yview)
        scrollb.grid(row=4, column=5, sticky='nsew')
        outputText.grid(row=4, column=0, sticky='nsew', columnspan=5)
        outputText.configure(yscrollcommand=scrollb.set)
        # ------------------------------------------MENU---------------------------------------------------
        mainMenu = Menu(self)
        fileSubMenu = Menu(mainMenu, tearoff=0)
        fileSubMenu.add_command(label="Новый файл", command=newFile)
        fileSubMenu.add_command(label="Открыть...", command=openFile)
        fileSubMenu.add_command(label="Сохранить...", command=saveFile)
        fileSubMenu.add_command(label="Печать...", command=printFile)
        fileSubMenu.add_command(label="Выход", command=self.exitFile)

        helpSubMenu = Menu(mainMenu, tearoff=0)
        helpSubMenu.add_command(label="Помощь", command=helpMenu)
        helpSubMenu.add_command(label="О программе", command=aboutProgramMenu)

        mainMenu.add_cascade(label="Файл", menu=fileSubMenu)
        mainMenu.add_cascade(label="Справка", menu=helpSubMenu)
        self.config(menu=mainMenu)
        # ------------------------------------------Buttons---------------------------------------------------
        buttonsFrame = Frame(self, bd=5)
        addWordsButton = Button(buttonsFrame, text='Добавить', width=25, height=2)
        addWordsButton.config(command=addWord)
        addWordsButton.pack(side='left')
        spaceLabel1 = Label(buttonsFrame, width=7, height=2)
        spaceLabel1.pack(side='left')
        addWordsButton = Button(buttonsFrame, text='Очистить', width=25, height=2)
        addWordsButton.config(command=cleanWord)
        addWordsButton.pack(side='left')
        spaceLabel2 = Label(buttonsFrame, width=7, height=2)
        spaceLabel2.pack(side='left')
        generateNewWordsButton = Button(buttonsFrame, text='Сгенерировать', width=25, height=2)
        generateNewWordsButton.config(command=generateWord)
        generateNewWordsButton.pack(side='left')
        self.title('Lab 1')
        outputFrame.pack()
        inputFrame.pack()
        inputText.pack()
        buttonsFrame.pack()
        self.geometry('800x400')

    def exitFile(self):
        if outputText.get(0, END) != ():
            answer = messagebox.askyesno(
                title="Вопрос",
                message="Сохранить словарь?")
            if answer:
                saveFile()
                self.destroy()
            else:
                self.destroy()
        else:
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
