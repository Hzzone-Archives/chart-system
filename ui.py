import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ApplicationWindow(QMainWindow):
	def __init__(self, parent=None):
		super(ApplicationWindow, self).__init__(parent)

		'''
		菜单栏UI
		'''
		bar = self.menuBar()
		file = bar.addMenu("File")

		open_file_action = QAction("Open", self)
		file.addAction(open_file_action)
		## 设置open按钮的槽
		open_file_action.triggered.connect(self.open_file)

		save_image_action = QAction("Save", self)
		## 添加快捷键
		save_image_action.setShortcut("Ctrl+S")
		file.addAction(save_image_action)
		#### 槽
		save_image_action.triggered.connect(self.save_image)


		'''
		定义各种操作，显示在第二个通道中的图形
		'''
		options = bar.addMenu("Options")
		differential_action = QAction("Differential", self)
		differential_action.triggered.connect(self.differential)

		options.addAction(differential_action)

		#### 退出，添加退出快捷键
		quit_menu = bar.addMenu("Quit")
		quit_action = QAction("Quit", self)
		quit_action.setShortcut(Qt.CTRL + Qt.Key_Q)
		# quit_action.triggered.connect(quit)
		quit_menu.addAction(quit_action)

		### 所有菜单栏的槽，输出按的键
		file.triggered[QAction].connect(self.processtrigger)
		options.triggered[QAction].connect(self.processtrigger)
		self.setWindowTitle("Chart system")

	def processtrigger(self, q):
		print(q.text() + " is triggered")


	def open_file(self):
		print("open file")

	def save_image(self):
		print("save_image")

	def differential(self):
		print("differential options")

def main():
	app = QApplication(sys.argv)
	ex = ApplicationWindow()
	ex.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
