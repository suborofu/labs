from DESForm import Ui_DESForm
from KeyModeForm import Ui_KeyModeForm
from PyQt5.QtWidgets import QDialog, QMainWindow, QTableWidgetItem, QFileDialog, QApplication
from qt_material import apply_stylesheet
import sys
from datetime import datetime
from Crypto.Cipher import DES
from crc64iso.crc64iso import crc64


class DESEncoder:
    mode = DES.MODE_ECB

    @staticmethod
    def __append_last_bytes(text):
        length = 8 - len(text) % 8
        text = text.ljust(len(text) + length, length.to_bytes(1, 'big'))
        return text

    @staticmethod
    def __delete_last_bytes(text):
        length = text[-1]
        if length > 8:
            raise Exception()
        return text[:-length]

    def encrypt_des(self, text, key):
        text = self.__append_last_bytes(text)
        des = DES.new(bytes.fromhex(crc64(key)), self.mode)
        return des.encrypt(text)

    def decrypt_des(self, text, key):
        des = DES.new(bytes.fromhex(crc64(key)), self.mode)
        text = des.decrypt(text)
        return self.__delete_last_bytes(text)


class KeyModeForm(QDialog):

    def __init__(self, master):
        super().__init__()
        self.ui = Ui_KeyModeForm()
        self.ui.setupUi(self)
        self.ui.btnOK.clicked.connect(self.accept)
        self.master = master

    def accept(self):
        mode = [DES.MODE_ECB, DES.MODE_CBC, DES.MODE_CFB, DES.MODE_OFB]
        self.master.des.mode = mode[self.ui.cbMode.currentIndex()]
        self.master.key = self.ui.leKey.text()
        super().accept()


class DESForm(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_DESForm()
        self.ui.setupUi(self)
        self.ui.btnEncrypt.clicked.connect(lambda: self.encrypt_decrypt(encrypt=True))
        self.ui.btnDecrypt.clicked.connect(lambda: self.encrypt_decrypt(encrypt=False))
        self.des = DESEncoder()

    def __add_result(self, result):
        row = self.ui.tblResult.rowCount()
        self.ui.tblResult.setRowCount(row + 1)
        for i in range(len(result)):
            self.ui.tblResult.setItem(row, i, QTableWidgetItem(str(result[i])))

    def encrypt_decrypt(self, encrypt=True):
        file_path = ''
        try:
            file_path = \
                QFileDialog.getOpenFileName(self, 'Open file', filter="" if encrypt else "Encrypted files (*.enc)")[0]
            with open(file_path, 'rb') as file:
                text = file.read()
            key_form = KeyModeForm(self)
            if not key_form.exec():
                raise Exception()
            text = self.des.encrypt_des(text, self.key) if encrypt else self.des.decrypt_des(text, self.key)
            if not len(text):
                raise Exception()
            with open(file_path + '.enc' if encrypt else file_path[:-4], 'wb') as file:
                file.write(text)
            result = 'OK'
        except Exception as e:
            result = 'Failure'
            print(e)
        if file_path != '':
            self.__add_result([file_path, 'Encryption' if encrypt else 'Decryption', result,
                               datetime.now().strftime("%b %d %Y %H:%M:%S")])


class DESApp(QApplication):

    def __init__(self):
        super().__init__(sys.argv)
        self.window = DESForm()
        self.window.show()
        apply_stylesheet(self, theme='dark_blue.xml')


App = DESApp()
sys.exit(App.exec())
