# Painter
Replaces each pixel of a photo with a photo of as similar colour possible

The paint.py script can be used to create a picture out of other pictures. This is a work in progress so I would recommend using duplicates of photos as a precaution.
The script works by first creating a “palette” from a directory filled with images. The palette contains a dictionary of the pictures with their predominant colours. By default colours are mapped onto a Hilbert’s curve so that when searching the palette for a colour a binary search can be used. Then the program goes through the pixels of the image to recreate and adds the picture with the closest predominant colour to the corresponding place in the image being created.

## Usage
Palettes can be saved so you don’t have to create a new one each time.

Colours don’t have to be mapped to Hilbert’s curve. The alternative goes through each image to find the one with the closest Euclidean distance instead. Not using Hilbert’s curve leads to slightly more accurate results but with a limited colour palette (tested with 180 photos) the results tend to look less creepy with inaccuracies and with large colour palettes (tested with 5000 photos) this method is unusably slow.

Running  `python3 ./Painter/paint.py -h` will provide a full list of options.

## Performance
I’ve been making this on a laptop with an i7 and 8GB of RAM.

For large libraries of images it is clearly more efficient to use Hilbert’s curve. To create an image with 344960 pixels from ~5000 images took 54 minutes using Hilbert’s curve but without only got to 9% completion after an hour. For small libraries of images there is not much difference when using Hilbert’s curve with both usually taking around 8 minutes to create a picture with 174592 pixels from 183 images.

One of the largest bottlenecks is opening an image to fill put it onto the image being created. Currently I am using the PILLOW library for handling the images but it sounds like there are others that would be faster for my usage.

## Results
With 180 images that are not very diverse in colour the results look odd. Shapes can be made out but a lot of close shades become the same giving an uncanny look.
With 5000 images the result become much better. The noise from the colours within the pictures give a more painting like feel.
To do: Add an examples folder. This will likely be screen grabs and not whole images because the increase in width and height leads to pictures that are about 1GB in size.

Things to implement/fix:
- Currently the image library is relative to the path the script is in but other properties don’t have this issue.
- A lot of error handling is to be added so it assumes the library of photos only contains photos.
- I intend to look into making this more efficient.
- Look into better algorithms to make the Euclid Palette useful as opposed to a naïve approach to compare against.
