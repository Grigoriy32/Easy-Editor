#создай тут фоторедактор Easy Editor!



import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, # Диалог открытия файлов (и папок)
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка
 
from PIL import Image

from PIL import ImageFilter


app = QApplication([])
win = QWidget()

def filter(files, extesions):
    result = list()
    for filename in files:
        for ext in extesions:
            if filename.endswith(ext):
                result.append(filename)
    return result

workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenameList():
    extesions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extesions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)



papka = QPushButton('Папка')
picture = QLabel("Картинка")
lw_files = QListWidget()

left = QPushButton('Лево')
right = QPushButton('Право')
mirror = QPushButton('Зеркало')
resk = QPushButton('Резкость')
bw = QPushButton('Ч/б')

win.resize(700,500)

layout1 = QVBoxLayout()
layout2 = QVBoxLayout()
layout3 = QHBoxLayout()


#lain1.addWidget(quet, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
layout1.addWidget(papka)
layout1.addWidget(lw_files)
layout2.addWidget(picture, 95)

layout_buttons = QHBoxLayout()

layout_buttons.addWidget(left)
layout_buttons.addWidget(right)
layout_buttons.addWidget(mirror)
layout_buttons.addWidget(resk)
layout_buttons.addWidget(bw)


layout2.addLayout(layout_buttons)

layout3.addLayout(layout1,20)
layout3.addLayout(layout2,80)

win.setLayout(layout3)


def showChosenImage():
    if lw_files.currentRow() >= 0:
       filename = lw_files.currentItem().text()
       workimage.loadImage(workdir, filename)
       image_path = os.path.join(workimage.dir, workimage.filename)
       workimage.showImage(image_path)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    def loadImage(self, dir, filename):
    #при загрузке запоминаем путь и имя файла
       self.dir = dir
       self.filename = filename
       image_path = os.path.join(dir, filename)
       self.image = Image.open(image_path)
    def do_bw(self):
       self.image = self.image.convert("L")
       self.saveImage()
       image_path = os.path.join(self.dir, self.save_dir, self.filename)
       self.showImage(image_path)
 
    def saveImage(self):
       ''' сохраняет копию файла в подпапке '''
       path = os.path.join(self.dir, self.save_dir)
       if not(os.path.exists(path) or os.path.isdir(path)):
           os.mkdir(path)
       image_path = os.path.join(path, self.filename)
       self.image.save(image_path)
    def showImage(self, path):
        picture.hide()
        pixmapimage = QPixmap(path)
        w, h = picture.width(), picture.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        picture.setPixmap(pixmapimage)
        picture.show()        
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_resk(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)






workimage = ImageProcessor()

lw_files.currentRowChanged.connect(showChosenImage)

resk.clicked.connect(workimage.do_resk)
mirror.clicked.connect(workimage.do_mirror)
right.clicked.connect(workimage.do_right)
left.clicked.connect(workimage.do_left)
bw.clicked.connect(workimage.do_bw)
papka.clicked.connect(showFilenameList)
win.show()
app.exec()


















































