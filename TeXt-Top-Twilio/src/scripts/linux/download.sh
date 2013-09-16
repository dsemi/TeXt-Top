#!/bin/bash


if [ -z "$1" ]; then
    echo "URL not specified"
    exit 1
fi

URL=$1
FILENAME=""

if [ -n "$2" ]; then
    FILENAME='-O "$2"'
fi

if [ -n "$3" -a -d "$3" ]; then
    cd "$3"
elif [ -d "$HOME/Downloads" ]; then
    cd "$HOME/Downloads"
else
    cd "$HOME"
fi

wget $FILENAME $URL
