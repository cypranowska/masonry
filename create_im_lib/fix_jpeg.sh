#!/bin/bash

if [[ -z $1 ]]; then
    echo "Usage: ./fix-jpeg.sh <dir>"
    exit 2
fi

for file in $(find $1 -name "*.jpeg"); do
    if [[ $(identify $file | cut -f2 -d' ') != "JPEG" ]]; then
        echo $file is not a JPEG. Converting...
        mv $file $file.old
        convert $file.old $file
        rm $file.old
    fi
done
