# Painter
Replaces each pixel of a photo with a photo of as similar colour possible

The paint.py script can be used to create a picture out of other pictures. This is a work in progress so I would recommend using duplicates of photos as a precaution.
The script works by first creating a “palette” from a directory filled with images. The palette contains a dictionary of the pictures with their predominant colours. By default colours are mapped onto a Hilbert’s curve so that when searching the palette for a colour a binary search can be used. Then the program goes through the pixels of the image to recreate and adds the picture with the closest predominant colour to the corresponding place in the image being created.

## Usage
Palettes can be saved so you don’t have to create a new one each time.

Colours don’t have to be mapped to Hilbert’s curve. The alternative goes through each image to find the one with the closest Euclidean distance instead. Not using Hilbert’s curve leads to slightly more accurate results but with a limited colour palette (tested with 180 photos) the results tend to look less creepy with inaccuracies and with large colour palettes (tested with 5000 photos) this method is unusably slow.

Running `python3 ./Painter/paint.py -h` will provide a full list of options.

## Performance
I’ve been making this on a laptop with an i7 and 8GB of RAM.

For large libraries of images it is clearly more efficient to use Hilbert’s curve. To create an image with 344960 pixels from ~5000 images took 54 minutes using Hilbert’s curve but without only got to 9% completion after an hour. For small libraries of images there is not much difference when using Hilbert’s curve, usually taking around 8 minutes to create a picture with 174592 pixels from 183 images.

Currently when making the palette k-means is used to find the separate colours and then the cluster with the most data-points in it is the predominant one. Other methods to identify the clusters could be faster:
- I imagine LDA would be more efficient but I'd need to test to see if nested clusters are common enough for there to be an issue.
- QDA is also fast but cannot be great depending on the shapes of the clusters.
- Random forest would be even slower.
- I haven't done anything with multicluster SVMs before. Given the principle with 2 distinct clusters I would expect it would also have the issue of not identifying nested clusters. I'd need to look into the pros and cons.

One of the largest bottlenecks is opening an image to put it onto the image being created. Currently I am using the PILLOW library for handling images but it sounds like there are others that would be faster for my usage.

## Results
Here are some results using the sample image below from MSCOCO. The photos generated are screen shots because the original files were very large, to the point where it would take a long time to show the details after zooming.

![Sample photo from MSCOCO](https://github.com/dan12321/painter/blob/main/examples/BoatFromMSCOCO2017.jpg)

With 5000 diverse images from MSCOCO the results are good. The noise from the colours within the pictures give a more painting like feel in places:

![Boat made using 5000 from MSCOCO](https://github.com/dan12321/painter/blob/main/examples/ResultFrom5000MSCOCOPhotos.JPG)

When zoomed in to the lifesaver you can see how the photos make up the image:

![Boat made using 5000 from MSCOCO zoomed](https://github.com/dan12321/painter/blob/main/examples/ResultFrom5000MSCOCOPhotosZoomed.JPG)

With 180 images that are not very diverse in colour the results look odd. Shapes can be made out but a lot of close shades become the same and green is clearly missing giving an uncanny look:

![Boat made using 180 pictues](https://github.com/dan12321/painter/blob/main/examples/ResultFrom183Photos.JPG)


Things to implement/fix:
- Currently the image library is relative to the path the script is in but other properties don’t have this issue.
- A lot of error handling is to be added so it assumes the library of photos only contains photos.
- I intend to look into making this more efficient.
- Look into better algorithms to make the Euclid Palette useful as opposed to a naïve approach to compare against.
