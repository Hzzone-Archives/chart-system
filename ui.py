import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import config
import utils


class ApplicationWindow(QMainWindow):
	open_file_signal = pyqtSignal()

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


		#### 绘图界面
		self.scrollArea = QScrollArea(self)
		# data = utils.read_file("/Users/HZzone/Desktop/test1.py")
		data = []
		self.canvas = Canvas(data=data, interval=config.default_interval, parent=self)
		self.scrollArea.setWidget(self.canvas)
		self.scrollArea.setWidgetResizable(False)
		self.scrollArea.widget().resize((len(data)+2)*config.default_interval, config.channels*config.min_channel_size)
		# self.scrollArea.widget().
		layout = QGridLayout(self)
		layout.addWidget(self.scrollArea, 0, 0)
		w = QWidget()
		self.slider = QSlider(Qt.Horizontal, w)
		layout.addWidget(self.slider, 1, 0)
		self.slider.valueChanged.connect(self.canvas.update_canvas)
		w.setLayout(layout)
		self.setCentralWidget(w)
		self.setMinimumHeight(config.channels*(config.min_channel_size+100))
		self.setMaximumWidth(2*config.min_channel_size)

		'''
		定义各种操作，显示在第二个通道中的图形
		'''
		options = bar.addMenu("Options")
		sin_action = QAction("sin", self)
		sin_action.triggered.connect(self.canvas.update_canvas)


		cos_action = QAction("cos", self)
		cos_action.triggered.connect(self.canvas.update_canvas)

		options.addAction(sin_action)
		options.addAction(cos_action)

		#### 退出，添加退出快捷键
		quit_menu = bar.addMenu("Quit")
		quit_action = QAction("Quit", self)
		quit_action.setShortcut(Qt.CTRL + Qt.Key_Q)
		# quit_action.triggered.connect(quit)
		quit_menu.addAction(quit_action)

		### 所有菜单栏的槽，输出按的键
		file.triggered[QAction].connect(self.processtrigger)
		options.triggered[QAction].connect(self.processtrigger)
		self.setWindowTitle("Chart System")



	def processtrigger(self, q):
		print(q.text() + " is triggered")


	def open_file(self):
		print("open file")
		fileName, filetype = QFileDialog.getOpenFileName(self,
		                                                  "选取文件",
		                                                  "C:/",
		                                                  "All Files (*);;Text Files (*.txt)")
		if fileName:
			self.canvas.data = utils.read_file(fileName)
			self.open_file_signal.connect(self.canvas.update_canvas)
			self.open_file_signal.emit()


	def save_image(self):
		print("save_image")
		formats = QImageWriter.supportedImageFormats()
		formats = map(lambda suffix: u"*." + suffix.decode(), formats)
		path = QFileDialog.getSaveFileName(self, self.tr("Save Image"),
		                                           "", self.tr("Image files (%1)"))
		print(path)
		im = self.canvas.grab()
		if path:
			im = im.scaled(im.size()/5)
			im.save(path[0])


class Canvas(QWidget):
	def __init__(self, data, interval, parent=None):
		super(Canvas, self).__init__(parent)
		### 要绘制的数据和每个点之间的间隔
		self.data = data
		### 处理后的数据
		self.new_data = None
		self.interval = interval
		self.my_sender = None

		# self.resize((len(data)+1), config.channels*300)
		self.mainlayout = QGridLayout(self)
		self.initial = True

	########画图事件，每次update都会进入，需要的是在更换间隔和数据时进行刷新
	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.resize((len(self.data)+2)*self.interval, config.channels*config.min_channel_size)

		qp.setPen(QPen(config.second_channel_point_color, config.first_channel_line_spacing))  ######可以试下画刷 setBrush,10指定点的大小
		qp.drawLine(0, 0,
		            0, config.channels * config.min_channel_size)
		qp.drawLine(0, config.min_channel_size,
		            self.width(), config.min_channel_size)
		qp.setPen(QPen(Qt.black, 5))  ######可以试下画刷 setBrush,10指定点的大小
		for index in range(0, config.min_channel_size, 20):
			qp.drawPoint(0, config.min_channel_size-index)
			qp.setFont(QFont("Decorative", config.font_size))
			qp.drawText(QRect(10, config.min_channel_size-index, 20, config.min_channel_size-index+config.font_size), Qt.AlignLeft|Qt.AlignTop, str(index))
		for index in range(0, config.min_channel_size, 20):
			qp.drawPoint(0, 2*config.min_channel_size-index)
			qp.setFont(QFont("Decorative", config.font_size))
			qp.drawText(QRect(10, 2*config.min_channel_size-index, 20, 2*config.min_channel_size-index+config.font_size), Qt.AlignLeft|Qt.AlignTop, str(index))
		for index in range(0, self.width(), int(self.interval)):
			qp.drawPoint(index, config.min_channel_size)
			qp.setFont(QFont("Decorative", config.font_size))
			qp.drawText(QRect(index, config.min_channel_size-config.font_size, index+config.font_size, config.min_channel_size), Qt.AlignLeft|Qt.AlignTop, str(index))

		if self.my_sender:
			if isinstance(self.my_sender, QSlider):
				print("滑动了")
				print(self.my_sender.value())
				val = self.my_sender.value()
				self.interval = int(config.default_interval+config.default_slider_interval*(val-config.default_slider_value))

		## 第二条线
		if self.my_sender:
			if isinstance(self.my_sender, QAction):
				if self.my_sender.text() == "sin":
					self.new_data = utils.sin(self.data)
				else:
					self.new_data = utils.cos(self.data)
			# else:
			# 	new_data = utils.sin(self.data)
		if self.new_data:
			qp.setPen(QPen(config.second_channel_point_color, config.point_size))  ######可以试下画刷 setBrush,10指定点的大小
			for index, x in enumerate(self.new_data):
				qp.drawPoint((index+1)*self.interval, 2*config.min_channel_size-x)
			qp.setPen(QPen(config.second_channel_line_color, config.second_channel_line_spacing,
						   config.second_channel_line_type))  ####前一个random是线条粗线，后一个random是线条类型
			for index, x in enumerate(self.new_data):
				if index == len(self.new_data) - 1:
					break
				qp.drawLine((index + 1) * self.interval, 2*config.min_channel_size - x, (index + 2) * self.interval,
							2*config.min_channel_size - self.new_data[index+1])

		self.drawLines(qp)######画线
		self.drawPoints(qp)  ###画点

		qp.end()

	def update_canvas(self):
		# print(QObject.sender())
		self.my_sender = self.sender()
		print(self.my_sender)
		self.update()

	def drawPoints(self, qp):
		### 绘制第一条曲线，不作任何处理
		qp.setPen(QPen(config.first_channel_point_color, config.point_size))  ######可以试下画刷 setBrush,10指定点的大小
		for index, x in enumerate(self.data):
			qp.drawPoint((index+1)*self.interval, config.min_channel_size-x)
		self.initial = True

	def drawLines(self, qp):#######画线
		qp.setPen(QPen(config.first_channel_line_color, config.first_channel_line_spacing, config.first_channel_line_type))####前一个random是线条粗线，后一个random是线条类型
		for index, x in enumerate(self.data):
			if index == len(self.data)-1:
				break
			qp.drawLine((index+1)*self.interval, config.min_channel_size-x, (index+2)*self.interval, config.min_channel_size-self.data[index+1])
		self.initial = True

def main():
	app = QApplication(sys.argv)
	ex = ApplicationWindow()
	ex.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
