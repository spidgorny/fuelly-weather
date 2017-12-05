import numpy as np
import scipy.stats as scistats

from Temperature import Temperature
from Fuelly import Fuelly
import time
from datetime import date
from datetime import datetime
from matplotlib import pyplot as plt

f = Fuelly()
# f.show()
min_fuelup_date = f.csv.min()['fuelup_date']
min_date = datetime.strptime(min_fuelup_date, '%Y-%m-%d')
date_combined = min_date.strftime('%Y%m%d')
print('min_fuelup_date', min_fuelup_date, min_date, date_combined)
print(f.csv.describe())

t = Temperature()
# t.show()
tdata = list(t.csv)
# tdata = list(zip(*tdata))
print('before', len(tdata))
tdata = list(filter(lambda row: str(row[1]) >= date_combined, tdata))
print('after', len(tdata))
print(*tdata[0:10], sep='\n')

# get columns from tdata
columns = list(zip(*tdata))

# convert 20170101 to real date
dates = [datetime.strptime(str(item), '%Y%m%d') for item in columns[1]]
temp = columns[2]
plt.plot(dates, temp)

fuel_dates = list(f.csv['fuelup_date'])
fuel_dates = [datetime.strptime(str(item), '%Y-%m-%d') for item in fuel_dates]
fuel_values = list(f.csv['l/100km'])
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

max_temp = max(temp)
print('max_temp', max_temp, max(fuel_heights))
fuel_heights = [(-item + 0.8) * max_temp * 2 for item in fuel_heights]
# print(*list(zip(fuel_dates, fuel_values, fuel_heights)), sep='\n')
plt.plot(fuel_dates, fuel_heights)


# find correlation
both = np.array(list(zip(temp, fuel_heights)))
print(both[0:10])

# normalizing as a whole (changes correlation by nothing)
# both = both / np.linalg.norm(both)
# both = both / both.max(axis=0)
both = (both - both.min(0)) / both.ptp(0)

print(both[0:10])
cor_matrix = np.corrcoef(both[:, 0], both[:, 1])
print(cor_matrix)
print('correlation', cor_matrix[0, 1] * 100, '%')
print('spearmanr', scistats.spearmanr(both))

plt.show()
