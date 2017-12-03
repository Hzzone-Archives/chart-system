import matplotlib.pyplot as plt
import math

'''
传入文件路径，返回一个LIST
'''
def read_file(path):
	data = []
	with open(path, "rb") as f:
		while True:
			chunk = f.read(1)
			if not chunk:
				break
			# data.append(ord(chunk))
			data.append(int.from_bytes(chunk, byteorder='little'))
	return data

'''
计算余弦值和正弦值
'''
def sin(data):
	new_data = []
	for x in data:
		new_data.append(math.sin(x/255*(math.pi/2))*255)
	return new_data

def cos(data):
	new_data = []
	for x in data:
		new_data.append(math.cos(x/255*(math.pi/2))*255)
	return new_data

if __name__ == "__main__":
	data = read_file("/Users/HZzone/Desktop/test1.py")
	fig = plt.gcf()
	fig.set_size_inches(18.5, 100)
	ax = fig.add_subplot(111)
	ax.plot(range(0, 20), data[:20])
	plt.show()
