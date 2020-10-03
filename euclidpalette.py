from __future__ import print_function

from pathlib import Path

from PIL import Image
from tqdm import tqdm

from palette import Palette


class EuclidPalette(Palette):
	def __init__(self, sourceDirectory, file):
		super().__init__(sourceDirectory, file)

	def MakeNewPalette(self):
		print("Collecting palette")
		colours = {}
		parent = Path(__file__).resolve().parents[1]
		photos = parent / self.sourceDirectory
		total = len(list(photos.iterdir()))
		with tqdm(total=total) as pbar:
			for photo in photos.iterdir():
				image = Image.open(photo)
				try:
					colours[str(photo)] = self.FindRegionColour(image)
				except IndexError as e:
					print(f"Error processing {photo}: {e}")
				pbar.update(1)
		self.colours = colours
		self.colKeys = list(self.colours.keys())
		self.colValues = list(self.colours.values())

	def GetDistance(self, x, y):
		return (x[0]-y[0]) ** 2 + (x[1]-y[1]) ** 2 + (x[2]-y[2]) ** 2

	def FindClosestIndex(self, arr, target):
		best = 0
		bestDist = self.GetDistance(arr[0], target)
		for i in range(1, len(arr)):
			dist = self.GetDistance(arr[i], target)
			if (dist < bestDist):
				bestDist = dist
				best = i
		return best

	def FindMatchingImage(self, RGB):
		rgb = list(RGB[:3])
		matchIndex = self.FindClosestIndex(self.colValues, rgb)
		return self.colKeys[matchIndex]
