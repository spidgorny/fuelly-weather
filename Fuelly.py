import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd


class Fuelly:

	def __init__(self):
		df = pd.read_csv('fuelups.csv', sep=',', quotechar='"')
		# print(df)
		# print(df.columns)
		df = df.rename(columns=lambda x: x.strip())
		# print(df.columns)
		df = df[['fuelup_date', 'l/100km']]
		df = df.iloc[::-1]
		df.index = pd.to_datetime(df['fuelup_date'])
		df = df[(df['l/100km'] > 0) & (df['fuelup_date'] != '2016-11-29') & (df['fuelup_date'] != '2016-12-13')]
		# print(df)
		self.csv = df

	def show(self):
		# plt.plot(self.csv['fuelup_date'], self.csv['1/100km'])
		# plt.show()
		self.csv.plot()
		plt.show()
