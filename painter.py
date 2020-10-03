from __future__ import print_function

from pathlib import Path

import strict
from PIL import Image
from tqdm import tqdm


class Painter:
	def __init__(self, palette):
		self.palette = palette

	def MakePixel(self, width, height, RGB):
		pixelPath = self.palette.FindMatchingImage(RGB)
		pixel = Image.open(pixelPath)
		pixel = pixel.resize((width, height))
		return pixel

	def PaintPixels(self, image, pixelSize, output):
		pxl = image.load()
		width, height = image.size
		print("Generating canvas...")
		newImage = Image.new('RGB', (width * pixelSize, height * pixelSize), (0,0,0,0))
		print("Blank canvas made")
		print("Painting pixels")
		with tqdm(total=width*height) as pbar:
			for i in range(width):
				for j in range(height):
					rgb = pxl[i, j]
					block = self.MakePixel(pixelSize, pixelSize, rgb)
					box = (i*pixelSize, j*pixelSize, (i+1)*pixelSize, (j+1)*pixelSize)
					newImage.paste(block, box)
					block.close()
					pbar.update(1)
		print(f"Saving {output}...")
		newImage.save(output)
		print("Image Saved")
		newImage.close()
