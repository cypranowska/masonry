from PIL import Image
import os, sys

if len(sys.argv) < 3:
    print("Usage: python image_resize.py <root-dir> <size in pixels>")
    sys.exit(2)

rootdir = sys.argv[1]
size = int(sys.argv[2])

for subdir, dirs, files in os.walk(rootdir):
    for f in files:

        img = Image.open(subdir+'/'+ f)
        newimg = img.resize((size, size))
        newimg.save(subdir+'/'+ f,img.format)
        img.close()
