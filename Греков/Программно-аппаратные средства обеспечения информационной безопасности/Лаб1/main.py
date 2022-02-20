import hashlib
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import os
from termcolor import colored

hashes = dict()


def load():
    filename = filedialog.askopenfilename()
    with open(filename, 'r') as db:
        text = db.read().split('\n')
        for string in text:
            if string == '':
                continue
            file, hash = string.split('\t')
            hashes[file] = hash


def check_directory():
    global hashes
    root = filedialog.askdirectory()
    if root == '':
        return
    for subdir, _, files in os.walk(root):
        for name in files:
            file = os.path.join(subdir, name).replace('\\', '/')
            print(file + ":\t", end='')
            text = open(file, 'rb').read()
            hash = hashlib.md5(text).hexdigest()
            try:
                if hashes[file] == hash:
                    print(colored('OK', 'green'))
                else:
                    print(colored('Failed', 'red'))
            except:
                print(colored('Not Found', 'yellow'))


def calc_directory():
    global hashes
    root = filedialog.askdirectory()
    if root == '':
        return
    for subdir, _, files in os.walk(root):
        for name in files:
            file = os.path.join(subdir, name).replace('\\', '/')
            text = open(file, 'rb').read()
            hash = hashlib.md5(text).hexdigest()
            hashes[file] = hash
    print(colored('END', 'green'))


def save():
    filename = filedialog.asksaveasfilename()
    with open(filename, 'w') as db:
        for file in hashes:
            db.write(file + '\t' + (hashes[file]) + '\n')


root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Button(frm, text="Load...", command=load).grid(column=0, row=0)
ttk.Button(frm, text="Calc...", command=calc_directory).grid(column=0, row=1)
ttk.Button(frm, text="Check...", command=check_directory).grid(column=0, row=2)
ttk.Button(frm, text="Save...", command=save).grid(column=0, row=3)
root.mainloop()
