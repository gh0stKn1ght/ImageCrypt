from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QWidget)
from cryptography.fernet import Fernet
from binascii import hexlify, unhexlify
import sys, os

if sys.platform == 'win32':
    slash = '\\'
else:
    slash = '/'


def decrypt(key, ciphertext):
    plaintext = Fernet(key).decrypt(ciphertext)
    return plaintext


def encrypt(key, plaintext):
    ciphertext = Fernet(key).encrypt(plaintext)
    return ciphertext


def export_key(file, key):
    if file == '': file = 'sym_key'
    key = open(file, 'wb').write(key)


def import_key(file):
    if file == '': file = 'sym_key'
    if not os.path.isfile(file): export_key(file, generate_sym_key())
    key = open(file, 'rb').read()
    return key


def generate_sym_key():
    key = Fernet.generate_key()
    return key


def write_jpeg(jpeg, file, key):
    data = hexlify(open(jpeg, 'rb').read()).decode()
    base_length = hex(len(data))[2:]
    if len(base_length) < 10:
        base_length = '0' * (10 - len(base_length)) + base_length
    base_length = base_length.encode()
    filename = encrypt(key, file.split(slash)[-1].encode())
    filename_length = hex(len(hexlify(filename)))[2:]
    if len(filename_length) < 10:
        filename_length = '0' * (10 - len(filename_length)) + filename_length
    filename_length = filename_length.encode()
    hidden_data = encrypt(key, open(file, 'rb').read())
    data = unhexlify(data.encode())
    new_data = data + hidden_data + filename + unhexlify(base_length) + unhexlify(filename_length)
    open(jpeg + '-old.jpeg', 'wb').write(data)
    open(jpeg, 'wb').write(new_data)


def read_jpeg(path, key):
    data = hexlify(open(path, 'rb').read()).decode()
    base_length = int(data[-20:-10], 16)
    filename_length = int(data[-10:], 16)

    hidden_data = decrypt(key, unhexlify(data[base_length:-20 - filename_length]))
    filename = decrypt(key, unhexlify(data[len(data) - filename_length - 20:-20]))

    open(filename, 'wb').write(hidden_data)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 400)
        MainWindow.setMaximumSize(QSize(900, 400))
        MainWindow.setMinimumSize(QSize(900, 400))
        font = QFont()
        font.setFamilies([u"Noto Mono"])
        font.setPointSize(18)
        font1 = QFont()
        font1.setFamilies([u"Noto Mono"])
        font1.setPointSize(15)
        MainWindow.setFont(font1)
        MainWindow.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(440, 0, 20, 390))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.mergeButton = QPushButton(self.centralwidget)
        self.mergeButton.setObjectName(u"mergeButton")
        self.mergeButton.setEnabled(True)
        self.mergeButton.setGeometry(QRect(20, 295, 410, 90))
        self.mergeButton.setFont(font)
        self.mergeButton.clicked.connect(self.merge)
        self.extractButton = QPushButton(self.centralwidget)
        self.extractButton.setObjectName(u"extractButton")
        self.extractButton.setGeometry(QRect(470, 295, 410, 90))
        self.extractButton.setFont(font)
        self.extractButton.clicked.connect(self.extract)
        self.imgPath = QLineEdit(self.centralwidget)
        self.imgPath.setObjectName(u"imgPath")
        self.imgPath.setGeometry(QRect(20, 55, 410, 60))
        self.payloadPath = QLineEdit(self.centralwidget)
        self.payloadPath.setObjectName(u"payloadPath")
        self.payloadPath.setGeometry(QRect(20, 135, 410, 60))
        self.keyPath = QLineEdit(self.centralwidget)
        self.keyPath.setObjectName(u"keyPath")
        self.keyPath.setGeometry(QRect(20, 215, 410, 60))
        self.keyPath_1 = QLineEdit(self.centralwidget)
        self.keyPath_1.setObjectName(u"keyPath_1")
        self.keyPath_1.setGeometry(QRect(470, 195, 410, 60))
        self.imgPath_1 = QLineEdit(self.centralwidget)
        self.imgPath_1.setObjectName(u"imgPath_1")
        self.imgPath_1.setGeometry(QRect(470, 75, 410, 60))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ImageCrypt launcher", None))
        self.mergeButton.setText(QCoreApplication.translate("MainWindow", u"Merge files", None))
        self.extractButton.setText(QCoreApplication.translate("MainWindow", u"Extract files", None))
        self.keyPath.setPlaceholderText('Key file("sym_key" for default)')
        self.keyPath_1.setPlaceholderText('Key file("sym_key" for default)')
        self.imgPath.setPlaceholderText('Path to .jpeg image')
        self.imgPath_1.setPlaceholderText('Path to .jpeg image')
        self.payloadPath.setPlaceholderText('File to hide in image')
    
    def merge(self):
        k_path = self.keyPath.text()
        key = import_key(k_path)
        img = self.imgPath.text()
        payload = self.payloadPath.text()
        if img == '' or payload == '':
            return
        try:
            write_jpeg(img, payload, key)
        except Exception as e:
            try:
                print('Merge failed:' + str(e))
            except:
                pass

    def extract(self):
        k_path = self.keyPath_1.text()
        key = import_key(k_path)
        img = self.imgPath_1.text()
        if img == '':
            return
        try:
            read_jpeg(img, key)
        except Exception as e:
            try:
                print('Extraction failed:' + e)
            except:
                pass


app = QApplication(sys.argv)
app_skeleton = QMainWindow()
main_window = Ui_MainWindow()
main_window.setupUi(app_skeleton)
main_window.retranslateUi(app_skeleton)
app_skeleton.show()
app.exec()