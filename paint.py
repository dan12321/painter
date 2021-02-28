import argparse

parser = argparse.ArgumentParser(description='Creates a picture out of pictures')
parser.add_argument('picture', metavar='P', type=str, nargs=1, help='the location of the picture to create')
parser.add_argument('library', metavar='L', type=str, nargs=1, help='the location of the pictures to use')
parser.add_argument('--pixelsize', dest='pixelsize', default=[50], nargs=1, help='the width and height of photo used in each pixel')
parser.add_argument('-o', '--output', dest='output', nargs=1, default=['paintedpic.png'], help='the destination file (default: paintedpic.png)')
parser.add_argument('-p', '--palette', dest='palette', nargs=1, help='the location of the palette to use')
parser.add_argument('-c', '--createpalette', dest='create', action='store_true', help='whether to create a new palette')
parser.add_argument('-ds', '--dontsavepalette', dest='save', action='store_false', help='whether or not save the palette')
parser.add_argument('-nh', '--nothilbert', dest='hilbert', action='store_false', help="doesn't approximate colour using hilbert's curve")
parser.add_argument('-s', '--stats', dest='stats', action='store_true', help="turns on debugging for performance")

args = parser.parse_args()

def main():
    import cProfile
    import pstats
    if (args.hilbert):
        from hilbertpalette import HilbertPalette as Palette
    else:
        from euclidpalette import EuclidPalette as Palette
    from painter import Painter
    from pgmagick import Image, Blob

    palette = None
    profile = cProfile.Profile()
    if (args.palette != None):
        palette = Palette(args.library[0], args.palette[0])
    else:
        palette = Palette(args.library[0], "palette.txt")

    if (args.create):
        palette.MakeNewPalette()
    else:
        try:
            palette.OpenPalette()
        except:
            print("Could not open palette")
            print("Creating new palette")
            palette.MakeNewPalette()

    if (args.save):
        palette.SavePalette()
    print("Palette to hand")

    with open(args.picture[0], 'rb') as file:
        image = Image(Blob(file.read()))
        print(f"Reference picture {args.picture[0]} open")
        painter = Painter(palette)
        print(f"Painting {args.output[0]}")
        profile.enable()
        painter.PaintPixels(image, args.pixelsize[0], args.output[0])
        profile.disable()
        if (args.stats):
            ps = pstats.Stats(profile)
            ps.sort_stats('cumtime', 'calls')
            ps.print_stats()

if __name__ == "__main__":
    main()