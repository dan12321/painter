from __future__ import print_function
from pathlib import Path
from PIL import Image
from tqdm import tqdm

parent = Path(__file__).resolve().parents[1]
photos = parent / "val2017"
total = len(list(photos.iterdir()))
with tqdm(total=total) as pbar:
	for photo in photos.iterdir():
		image = Image.open(photo)
		image = image.resize((50, 50))
		image.save(photo)
		pbar.update()
