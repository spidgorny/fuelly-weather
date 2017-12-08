import numpy as np
import scipy.stats as scistats
from Temperature import Temperature
from Fuelly import Fuelly
from matplotlib import pyplot as plt


def combine_both(temp, fuel_heights):
	both = np.array(list(zip(temp, fuel_heights)))
	print(both[0:10])

	# normalizing as a whole (changes correlation by nothing)
	# both = both / np.linalg.norm(both)
	# both = both / both.max(axis=0)
	both = (both - both.min(0)) / both.ptp(0)

	print(both[0:10])
	return both


def main():
	f = Fuelly()
	date_combined = f.getDateCombined()

	t = Temperature()
	# t.show()
	tdata = t.limitByDate(date_combined)

	dates, temp = t.splitInTwo(tdata)
	plt.plot(dates, temp)

	fuel_dates = f.getDates()
	fuel_dates, fuel_heights = f.getHeights(fuel_dates, max(temp))
	plt.plot(fuel_dates, fuel_heights)

	# find correlation
	both = combine_both(temp, fuel_heights)
	cor_matrix = np.corrcoef(both[:, 0], both[:, 1])
	print(cor_matrix)
	print('correlation', cor_matrix[0, 1] * 100, '%')
	print('spearmanr', scistats.spearmanr(both))

	plt.show()


main()
