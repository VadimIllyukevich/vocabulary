# -*- coding: utf-8 -*-
__version__ = 'Version:1.0'
from tkinter import *
from operator import itemgetter
import requests
import json

from nltk import sent_tokenize, word_tokenize

list_words = []
HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Accept-Charset': 'UTF-8'
    }
PARAMS = (
        ('targetType', 'pos-token'),
        ('targetType', 'spelling-correction-token'),
        ('targetType', 'syntax-relation'),
        ('apikey', 'b11e0cc09d4d7b3c4c56116688dd27beae454257'),
    )


def get_response(line, window):
    """
    Sending text to an old resource and receiving a response, as well as parsing a string.
    :param line: entered text
    :param window: window for to enter text
    :return: parsed string
    """
    line = line.replace('\n', ' ')
    data = '[ { "text" : "' + str(line) + '" } ]'
    response = requests.post('http://api.ispras.ru/texterra/v1/nlp', headers=HEADERS, params=PARAMS,
                             data=data.encode('utf-8'))
    parsed_string = json.loads(response.text)
    position = parsed_string[0]['annotations']['pos-token']
    word = parsed_string[0]['annotations']['spelling-correction-token']
    syntax = parsed_string[0]['annotations']['syntax-relation']
    word_parser(word, position, syntax)
    quitWindow(window)


def word_parser(word, position, syntax):
    """
    Parsing strings for tokens.
    :param word: list with words
    :param position: list with word position
    :param syntax: list with syntax information
    :return: parsed string
    """
    i = 0
    while i < len(word):
        name_word = word[i]['value'].lower()
        char = position[i]['value']['characters']
        if position[i]['value']['tag'] == 'PUNCT':
            i += 1
            continue
        syntax_word = syntax[i]['value']
        param = ''
        if syntax_word:
            if syntax_word['type']:
                param = syntax_word['type']
        tags = [position[i]['value']['tag']]
        for j in char:
            tags.append(j['tag'])
        if param:
            tags.append(param)
        list_words.append({'name': name_word, 'param': tags})
        i += 1

root = Tk()
root.title("Textedit " + str(__version__))
root.resizable(width=False, height=False)
root.geometry("200x130+300+300")


def inputWindow():
    """
    :return: UI for enter text
    """
    children = Toplevel(root)
    children.title('Input word and sentence')
    children.geometry("420x200+300+300")
    calculated_text = Text(children, height=10, width=50)
    scrollb = Scrollbar(children, command=calculated_text.yview)
    scrollb.grid(row=4, column=4, sticky='nsew')
    calculated_text.grid(row=4, column=0, sticky='nsew', columnspan=3)
    calculated_text.configure(yscrollcommand=scrollb.set)
    b1 = Button(children, width=25, text="Send", command=lambda: get_response(
        calculated_text.get(1.0, END), children))
    b1.grid(row=5, column=1, sticky=E, padx=5, pady=8, )


def quitWindow(window):
    """
    :param window: current window
    :return: destroy window
    """
    window.destroy()


def helpWindow():
    """
    :return: help for user
    """
    children = Toplevel(root)
    children.title('Helper')
    children.geometry("420x300+300+300")
    calculated_text = Text(children, height=15, width=50)
    scrollb = Scrollbar(children, command=calculated_text.yview)
    scrollb.grid(row=4, column=4, sticky='nsew')
    calculated_text.grid(row=4, column=0, sticky='nsew', columnspan=3)
    calculated_text.configure(yscrollcommand=scrollb.set)
    calculated_text.insert('end', 'A       прилагательное\nPR       предлог\n'
                                  'CONJ        союз\nS         существительное\n'
                                  'NUM       числительное')
    calculated_text.configure(state='disabled')


def viewWindow():
    """
    :return: UI to view parsed text
    """
    list_words.sort(key=itemgetter('name'))
    children = Toplevel(root)
    children.title('View dictionary')
    # children.geometry("420x300+300+300")
    list_box = Listbox(children, height=10, width=65)
    scrollb = Scrollbar(children, command=list_box.yview)
    scrollb.grid(row=4, column=5, sticky='nsew')
    list_box.grid(row=4, column=0, sticky='nsew', columnspan=5)
    list_box.configure(yscrollcommand=scrollb.set)
    b1 = Button(children, width=25, text="Ok", command=lambda: quitWindow(children))
    b1.grid(row=5, column=1, sticky=E, padx=5, pady=8, )
    b2 = Button(children, text="Help?", command=helpWindow)
    b2.grid(row=1, column=1, sticky=W, padx=5, pady=8, )
    label1 = Label(children, text='Лексема:')
    label1.grid(row=6, column=0)
    calculated_text1 = Text(children, height=1, width=10)
    calculated_text1.grid(row=6, column=1, sticky='nsew')
    label2 = Label(children, text='Тэги:')
    label2.grid(row=6, column=2)
    calculated_text2 = Text(children, height=1, width=10)
    calculated_text2.grid(row=6, column=3, sticky='nsew')
    b = Button(children, text="Добавить", command=lambda: add_word(calculated_text1, calculated_text2, list_box))
    b.grid(row=6, column=4, sticky=W, padx=5, pady=8, )
    i = len(list_words)-1
    while i >= 0:
        list_box.insert(0, str(list_words[i]['name']) + ' ' + str(list_words[i]['param']))
        i -= 1


def add_word(calculated_text1, calculated_text2, list_box):
    word = calculated_text1.get(1.0, END)
    tag = calculated_text2.get(1.0, END)
    list_box.insert(0, word + ' ' + tag)
    list_words.append({'name': word, 'param': tag})

b3 = Button(text="Input", width=25, command=inputWindow)
b3.grid(row=5, column=4, sticky=N, padx=5, pady=8, )
b4 = Button(text="View", width=25, command=viewWindow)
b4.grid(row=4, column=4, sticky=S, padx=5, pady=8, )

root.mainloop()
