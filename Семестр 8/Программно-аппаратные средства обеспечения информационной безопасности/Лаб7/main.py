from Crypto.Cipher import DES
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import ctypes


class DESEncoder:
    mode = None

    def __init__(self):
        self.mode = DES.MODE_ECB

    @staticmethod
    def __append_last_bytes(text):
        length = 8 - len(text) % 8
        text = text.ljust(len(text) + length, length.to_bytes(1, 'big'))
        return text

    @staticmethod
    def __delete_last_bytes(text):
        length = text[-1]
        return text[:-length]

    def encrypt_des(self, text, key):
        text = self.__append_last_bytes(text)
        des = DES.new(key, self.mode)
        return des.encrypt(text)

    def decrypt_des(self, text, key):
        des = DES.new(key, self.mode)
        text = des.decrypt(text)
        return self.__delete_last_bytes(text)


class DESForm(Tk):
    des = None
    key = None

    class KeyModeForm(Toplevel):
        key = None
        mode = None

        def __init__(self, master=None):
            super().__init__(master=master)

            self.title("Enter Key and Mode")
            self.geometry("220x100")
            frm = ttk.Frame(self, padding=10)
            frm.grid()
            ttk.Label(frm, text="Key", width=10).grid(column=0, row=0)
            self.key = ttk.Entry(frm, show="*", width=20)
            self.key.grid(column=1, row=0)
            ttk.Label(frm, text="Mode", width=10).grid(column=0, row=1)
            self.mode = ttk.Combobox(frm, values=["ECB", "CBC", "CFB", "OFB"], width=17)
            self.mode.current(0)
            self.mode.grid(column=1, row=1)
            ttk.Button(frm, text="Apply", width=20, command=self.destroy).grid(column=1, row=2)

        def destroy(self):
            mode = {"ECB": DES.MODE_ECB, "CBC": DES.MODE_CBC, "CFB": DES.MODE_CFB, "OFB": DES.MODE_OFB}
            self.master.des.mode = mode[self.mode.get()]
            self.master.key = self.key.get()
            super().destroy()

    def __init__(self, screenName=None, baseName=None, className='DESForm',
                 useTk=True, sync=False, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title("DES Encoder")
        frm = ttk.Frame(self, padding=10)
        frm.grid()
        ttk.Button(frm, text="Encrypt File...", width=50, command=self.encrypt).grid(column=0, row=0)
        ttk.Button(frm, text="Decrypt File...", width=50, command=self.decrypt).grid(column=0, row=1)

        self.des = DESEncoder()

    @staticmethod
    def __message(title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    def encrypt(self):
        try:
            file_path = filedialog.askopenfilename()
            with open(file_path, 'rb') as file:
                text = file.read()
            key_form = self.KeyModeForm(master=self)
            while key_form is not None:
                self.update()
            text = self.des.encrypt_des(text, self.key)
            with open(file_path + '.enc', 'wb') as file:
                file.write(text)
            self.__message('Complete', 'File has been encrypted', 64)
        except Exception as e:
            self.__message('Error', 'File cannot be encrypted', 16)

    def decrypt(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.enc")])
            with open(file_path, 'rb') as file:
                text = file.read()
            self.KeyModeForm(master=self)
            self.wait_window(self.KeyModeForm)
            text = self.des.decrypt_des(text, self.key)
            with open(file_path[:-4], 'wb') as file:
                file.write(text)
            self.__message('Complete', 'File has been decrypted', 64)
        except:
            self.__message('Error', 'File cannot be decrypted', 16)


des = DESForm()
des.mainloop()
