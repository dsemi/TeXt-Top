#!/bin/bash

if [ -z "$1" ]; then
    echo 'No filename specified'
fi

FILENAME="$1"
START_DIR="$HOME"
LINES=""

if [ -n "$2" ]; then
    START_DIR="$2"
fi

if [ -n "$3" ]; then
    LINES="-n $3"
fi

find "$START_DIR" -type f -iname "*$FILENAME*" | head $LINES
