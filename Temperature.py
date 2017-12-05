import numpy as np
import datetime
import matplotlib.pyplot as plt


class Temperature:

	def __init__(self):
		print('18700101', self.datestr2num('18700101'))
		print('24', self.tenTimes('24'))

		self.csv = np.loadtxt('temperature/TG_STAID004105.txt', comments='#', delimiter=',', skiprows=20,
						 # usecols=['SOUID', 'DATE', 'TG', 'Q_TG']
						 converters={
							 # 1: self.datestr2num,
							 2: self.tenTimes
						 },
						 dtype={
							 'names': ('souid', 'date', 'temp', 'tg'),
							 'formats': ('i4', 'i4', 'f4', 'i4')
						 }
						 )

		# self.csv = self.csv[self.csv[2] > -100]  # date is not filtered
		size = len(self.csv)
		print(size)
		self.csv = np.array(list(filter(lambda x: x[2] > -100, self.csv)))
		print(self.csv.size)
		print('removed', size - self.csv.size)

	def datestr2num(self, num):
		# print(int(num[0:4]), int(num[4:6]), int(num[6:8]))
		return datetime.date(int(num[0:4]), int(num[4:6]), int(num[6:8]))

	def tenTimes(self, num):
		return float(num) / 10.0

	def show(self):
		csv = self.csv
		print(csv.shape)
		rows = np.array(list(zip(*csv)))

		# temp.reshape((4,))
		print(rows.shape)

		x = rows[1]
		temp = rows[2]
		plt.plot(x, temp)


		# trend line
		y = temp
		z = np.polyfit(x, y, 1)
		p = np.poly1d(z)
		plt.plot(x, p(x), 'r--')

		plt.show()
		mng = plt.get_current_fig_manager()
		mng.frame.Maximize(True)
		mng.window.state('zoomed')
		mng.window.showMaximized()
		mng.resize(*mng.window.maxsize())
		mng.full_screen_toggle()




