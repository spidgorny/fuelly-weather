from datetime import datetime
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

	def getDateCombined(self):
		# f.show()
		min_fuelup_date = self.csv.min()['fuelup_date']
		min_date = datetime.strptime(min_fuelup_date, '%Y-%m-%d')
		date_combined = min_date.strftime('%Y%m%d')
		print('min_fuelup_date', min_fuelup_date, min_date, date_combined)
		print(self.csv.describe())
		return date_combined

	def getDates(self):
		fuel_dates = list(self.csv['fuelup_date'])
		fuel_dates = [datetime.strptime(str(item), '%Y-%m-%d') for item in fuel_dates]
		return fuel_dates

	def getHeights(self, fuel_dates, max_temp):
		fuel_values = list(self.csv['l/100km'])
		# print(*fuel_values, sep='\n')
		min_consumption = min(fuel_values)
		max_consumption = max(fuel_values)
		range_consumption = max_consumption - min_consumption
		print('min_consumption', min_consumption, 'max_consumption', max_consumption, range_consumption)
		fuel_heights = [(float(item) - min_consumption) / range_consumption for item in fuel_values]

		# remove 0 because of division by zero on the next line
		# fuel_values = filter(lambda x: x != 0.0, fuel_values)	#  wrong number of fuel_dates then
		for i, item in enumerate(fuel_heights):
			if item == 0.0:
				del fuel_values[i]
				del fuel_heights[i]
				del fuel_dates[i]

		print('max_temp', max_temp, max(fuel_heights))
		fuel_heights = [(-item + 0.8) * max_temp * 2 for item in fuel_heights]
# print(*list(zip(fuel_dates, fuel_values, fuel_heights)), sep='\n')
		return fuel_dates, fuel_heights
