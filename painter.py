from __future__ import print_function

from pathlib import Path

import strict
import helpermethods as hm
from pgmagick import Blob, Geometry, Image, CompositeOperator as co
from tqdm import tqdm


class Painter:
	def __init__(self, palette):
		self.palette = palette

	def MakePixel(self, width, height, RGB):
		pixelPath = self.palette.FindMatchingImage(RGB)
		with open(pixelPath, 'rb') as file:
			pixel = Image(Blob(file.read()), Geometry(width, height))
			return pixel

	def PaintPixels(self, image, pixelSize, output):
		width = image.columns()
		height = image.rows()
		pxls = image.getPixels(0, 0, width, height)
		print("Generating canvas...")
		newImage = Image(Geometry(width * pixelSize, height * pixelSize), 'transparent')
		print("Blank canvas made")
		print("Painting pixels")
		with tqdm(total=width*height) as pbar:
			for i in range(width):
				for j in range(height):
					rgb = hm.pixelToRgb(pxls[width * j + i])
					block = self.MakePixel(pixelSize, pixelSize, rgb)
					newImage.composite(block, i*pixelSize, j*pixelSize, co.OverCompositeOp)
					pbar.update(1)
		print(f"Saving {output}...")
		newImage.write(output)
		print("Image Saved")
