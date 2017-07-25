from PIL import Image
from resizeimage import resizeimage
import os, sys

if len(sys.argv) < 3:
    print("Usage: python image_resize.py <root-dir> <size in pixels>")
    sys.exit(2)

rootdir = sys.argv[1]
size = int(sys.argv[2])

for subdir, dirs, files in os.walk(rootdir):
    for f in files:

        img = Image.open(subdir+'/'+ f)
        img = resizeimage.resize_thumbnail(img, [size, size])
        img.save(subdir+'/'+ f,img.format)
        img.close()
