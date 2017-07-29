import os, sys, imagehash
from PIL import Image

if len(sys.argv) < 2:
    print("Usage: python detect_duplicates.py <root-dir>")
    sys.exit(2)

rootdir = sys.argv[1]

hashes = {}

def add_to_hashes(filename,img):
    hashstr = str(imagehash.phash(img))
    if hashstr in hashes:
        hashes[hashstr].append(filename)
    else:
        hashes[hashstr] = [filename]

for subdir, dirs, files in os.walk(rootdir):
    for f in files:

        filename = subdir + '/' + f
        print("Processing " + filename + "...")
        img = Image.open(filename)
        # 0 degree hash
        add_to_hashes(filename,img)
        # 90 degree hash
        img = img.rotate(90, expand=True)
        add_to_hashes(filename,img)
        # 180 degree hash
        img = img.rotate(90, expand=True)
        add_to_hashes(filename,img)
        # 270 degree hash
        img = img.rotate(90, expand=True)
        add_to_hashes(filename,img)

        img.close()

for duplist in hashes.values():
    if len(duplist) > 1:
        print("Duplicates detected!")
        print(duplist)

