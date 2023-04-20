#! /usr/bin/env python3.11

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont  # for convenience

key = tk.Tk()
font = tkFont.Font(family='Helvetica', size=10)

key.title('On Screen Keyboard')

keylist = [
{'lc':'`',   'uc':'~',   'row':1, 'col':0, 'span':1},
{'lc':'1',   'uc':'!',   'row':1, 'col':1, 'span':1},
{'lc':'2',   'uc':'@',   'row':1, 'col':2, 'span':1},
{'lc':'3',   'uc':'#',   'row':1, 'col':3, 'span':1},
{'lc':'4',   'uc':'$',   'row':1, 'col':4, 'span':1},
{'lc':'5',   'uc':'%',   'row':1, 'col':5, 'span':1},
{'lc':'6',   'uc':'^',   'row':1, 'col':6, 'span':1},
{'lc':'7',   'uc':'&',   'row':1, 'col':7, 'span':1},
{'lc':'8',   'uc':'*',   'row':1, 'col':8, 'span':1},
{'lc':'9',   'uc':'(',   'row':1, 'col':9, 'span':1},
{'lc':'0',   'uc':')',   'row':1, 'col':10, 'span':1},
{'lc':'-',   'uc':'_',   'row':1, 'col':11, 'span':1},
{'lc':'=',   'uc':'+',   'row':1, 'col':12, 'span':1},
{'lc':'<-',  'uc':'<-',   'row':1, 'col':13, 'span':1},
{'lc':'Tab', 'uc':'Tab', 'row':2, 'col':0, 'span':2},
{'lc':'q',   'uc':'Q',   'row':2, 'col':2, 'span':1},
{'lc':'w',   'uc':'W',   'row':2, 'col':3, 'span':1},
{'lc':'e',   'uc':'E',   'row':2, 'col':4, 'span':1},
{'lc':'r',   'uc':'R',   'row':2, 'col':5, 'span':1},
{'lc':'t',   'uc':'T',   'row':2, 'col':6, 'span':1},
{'lc':'y',   'uc':'Y',   'row':2, 'col':7, 'span':1},
{'lc':'u',   'uc':'U',   'row':2, 'col':8, 'span':1},
{'lc':'i',   'uc':'I',   'row':2, 'col':9, 'span':1},
{'lc':'o',   'uc':'O',   'row':2, 'col':10, 'span':1},
{'lc':'p',   'uc':'P',   'row':2, 'col':11, 'span':1},
{'lc':'[',   'uc':'{',   'row':2, 'col':12, 'span':1},
{'lc':']',   'uc':'}',   'row':2, 'col':13, 'span':1},
{'lc':'a',   'uc':'A',   'row':3, 'col':0, 'span':1},
{'lc':'s',   'uc':'S',   'row':3, 'col':1, 'span':1},
{'lc':'d',   'uc':'D',   'row':3, 'col':2, 'span':1},
{'lc':'f',   'uc':'F',   'row':3, 'col':3, 'span':1},
{'lc':'g',   'uc':'G',   'row':3, 'col':4, 'span':1},
{'lc':'h',   'uc':'H',   'row':3, 'col':5, 'span':1},
{'lc':'j',   'uc':'J',   'row':3, 'col':6, 'span':1},
{'lc':'k',   'uc':'K',   'row':3, 'col':7, 'span':1},
{'lc':'l',   'uc':'L',   'row':3, 'col':8, 'span':1},
{'lc':';',   'uc':':',   'row':3, 'col':9, 'span':1},
{'lc':"'",   'uc':'"',   'row':3, 'col':10, 'span':1},
{'lc':'\\',  'uc':'|',   'row':3, 'col':11, 'span':1},
{'lc':'Ent', 'uc':'Ent', 'row':3, 'col':12, 'span':2},
{'lc':'Sh',  'uc':'Sh',  'row':4, 'col':0, 'span':2},
{'lc':'z',   'uc':'Z',   'row':4, 'col':2, 'span':1},
{'lc':'x',   'uc':'X',   'row':4, 'col':3, 'span':1},
{'lc':'c',   'uc':'C',   'row':4, 'col':4, 'span':1},
{'lc':'v',   'uc':'V',   'row':4, 'col':5, 'span':1},
{'lc':'b',   'uc':'B',   'row':4, 'col':6, 'span':1},
{'lc':'n',   'uc':'N',   'row':4, 'col':7, 'span':1},
{'lc':'m',   'uc':'M',   'row':4, 'col':8, 'span':1},
{'lc':',',   'uc':'<',   'row':4, 'col':9, 'span':1},
{'lc':'.',   'uc':'>',   'row':4, 'col':10, 'span':1},
{'lc':'/',   'uc':'?',   'row':4, 'col':11, 'span':1},
{'lc':'Clr', 'uc':'Clr', 'row':4, 'col':12, 'span':2},
{'lc':'SPC', 'uc':'SPC', 'row':5, 'col':4, 'span':5}
]

# entry box
equation = tk.StringVar()
Dis_entry = ttk.Entry(key, state='readonly', textvariable=equation)
Dis_entry.grid(rowspan=1, columnspan=80)

# showing all data in display
exp = " "
is_shift = False

# Necessary functions

def press(item):
    global exp
    exp = exp + str(item["text"])
    equation.set(exp)

def Backspace():
    global exp
    exp = exp[:-1]
    equation.set(exp)


def Shift():
    global is_shift
    is_shift = not is_shift
    print ("SHIFT")
    display()


def Clear():
    global exp
    exp = " "
    equation.set(exp)

def display():
    char = 'lc'
    if is_shift:
        char = 'uc'

    for row in keylist:
        btn = tk.Label(key, font=font, text=row[char], padx = 4, borderwidth=1, relief="solid")
        btn.grid(column=row['col'], row=row['row'], columnspan = row['span'], sticky="news", padx = 2, pady = 2)
        if row[char] == 'Sh':
            btn.bind("<Button-1>", lambda event, btn=btn: Shift())
        elif row[char] == 'Clr':
            btn.bind("<Button-1>", lambda event, btn=btn: Clear())
        elif row[char] == '<-':
            btn.bind("<Button-1>", lambda event, btn=btn: Backspace())
        else:
            btn.bind("<Button-1>", lambda event, btn=btn: press(btn))

    key.mainloop()
        
def force_display(): # uppercase is larger, run once to set size
    char = 'uc'
    for row in keylist:
        btn = tk.Label(key, font=font, text=row[char], padx = 4, borderwidth=1, relief="solid")
        btn.grid(column=row['col'], row=row['row'], columnspan = row['span'], sticky="news", padx = 2, pady = 2)
        if row[char] == 'Sh':
            btn.bind("<Button-1>", lambda event, btn=btn: Shift())
        elif row[char] == 'Clr':
            btn.bind("<Button-1>", lambda event, btn=btn: Clear())
        elif row[char] == '<-':
            btn.bind("<Button-1>", lambda event, btn=btn: Backspace())
        else:
            btn.bind("<Button-1>", lambda event, btn=btn: press(btn))

force_display()
display()
