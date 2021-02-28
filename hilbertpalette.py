from __future__ import print_function

from pathlib import Path

import numpy as np
from hilbertcurve.hilbertcurve import HilbertCurve
from pgmagick import Image, Blob
from tqdm import tqdm

from palette import Palette


class HilbertPalette(Palette):
	def __init__(self, sourceDirectory, file):
		super().__init__(sourceDirectory, file)
		self.hilbert_curve = HilbertCurve(255, 3)

	def MakeNewPalette(self):
		print("Collecting palette")
		colours = {}
		local = Path(__file__).resolve().parents[0]
		photos = local / self.sourceDirectory
		total = len(list(photos.iterdir()))
		with tqdm(total=total) as pbar:
			for photo in photos.iterdir():
				with open(photo, 'rb') as file:
					image = Image(Blob(file.read()))
					try:
						colour = self.FindRegionColour(image)
						dist = self.hilbert_curve.distance_from_point(np.rint(colour[:3]).astype(int).tolist())
						colours[str(photo)] = dist
					except IndexError as e:
						print(f"Error processing {photo}: {e}")
					pbar.update(1)
		print("Sorting")
		colours = {k: v for k, v in tqdm(sorted(colours.items(), key=lambda item: item[1]))}
		self.colours = colours
		self.colKeys = list(self.colours.keys())
		self.colValues = list(self.colours.values())

	def GetClosest(self, val1, val2, target):
		if (target - val1 >= val2 - target):
			return val2
		else:
			return val1

	def FindClosestIndex(self, arr, n, target):
		if (target <= arr[0]):
			return 0
		if (target >= arr[n - 1]):
			return n - 1

		i = 0; j = n; mid = 0
		while (i < j):
			mid = (i + j) // 2
			if (arr[mid] == target):
				return mid

			if (target < arr[mid]) :

				if (mid > 0 and target > arr[mid - 1]):
					if (self.GetClosest(arr[mid - 1], arr[mid], target) == mid):
						return mid
					else:
						return mid - 1
				j = mid
			else:
				if (mid < n - 1 and target < arr[mid + 1]):
					if (self.GetClosest(arr[mid], arr[mid + 1], target) == arr[mid]):
						return mid
					else:
						return mid + 1
				i = mid + 1
		return mid

	def FindMatchingImage(self, RGB):
		rgbDist = self.hilbert_curve.distance_from_point(list(RGB[:3]))
		matchIndex = self.FindClosestIndex(self.colValues, len(self.colValues), rgbDist)
		return self.colKeys[matchIndex]
