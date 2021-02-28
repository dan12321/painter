def pixelToRgb(pixel):
	return [float(pixel.red), float(pixel.green), float(pixel.blue)]

def pixelsToRgbs(pixels):
	return list(map(pixelToRgb, pixels))