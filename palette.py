from __future__ import print_function

from pathlib import Path

import numpy as np
import helpermethods as hm
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
		reWidth = region.columns()
		reHieght = region.rows()
		sampleWidth = int(reWidth*resizeRatio)
		sampleHieght = int(reHieght*resizeRatio)
		region.scale(str(sampleWidth) + 'X' + str(sampleHieght))
		pxls = region.getPixels(0, 0, sampleWidth, sampleHieght)
		rgbPxls = hm.pixelsToRgbs(pxls)

		codes, dist = cluster.vq.kmeans(rgbPxls, numClusters)
		vecs, dist = cluster.vq.vq(rgbPxls, codes)
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
