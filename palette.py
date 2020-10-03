from __future__ import print_function

from pathlib import Path

import numpy as np
import scipy
import scipy.cluster as cluster


class Palette:
	def __init__(self, sourceDirectory, file):
		self.colours = {}
		self.sourceDirectory = sourceDirectory
		self.file = file
		self.colValues = []
		self.colKeys = []

	def FindRegionColour(self, region, resizeRatio = 1, numClusters = 5):
		reWidth, reHieght = region.size
		region = region.resize((int(reWidth*resizeRatio), int(reHieght*resizeRatio)))
		ar = np.asarray(region)
		shape = ar.shape
		ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

		codes, dist = cluster.vq.kmeans(ar, numClusters)
		vecs, dist = cluster.vq.vq(ar, codes)
		counts, bins = scipy.histogram(vecs, len(codes))

		index_max = scipy.argmax(counts)
		peak = codes[index_max]
		return peak

	def SetDirectory(self, sourceDirectory):
		self.sourceDirectory = sourceDirectory

	def SetSaveFile(self, saveFile):
		self.file = saveFile

	def SavePalette(self):
		saveFile = open(self.file, "w")
		saveFile.write(str(self.colours))
		saveFile.close()

	def OpenPalette(self):
		saveFile = open(self.file, "r")
		strColours = saveFile.read()
		colours = eval(strColours)
		for colour in colours:
			self.colours[Path(colour)] = np.asarray(colours[colour])
		saveFile.close()
		self.colKeys = list(self.colours.keys())
		self.colValues = list(self.colours.values())
