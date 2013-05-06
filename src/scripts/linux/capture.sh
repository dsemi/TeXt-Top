#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

streamer -c /dev/video0 -b 16 -o $HOME/Pictures/5225582522828258282822828128.jpeg > /dev/null 2>&1

python2 send\ mail.py "$1" "This is a message sent from TeXt-Top." "5225582522828258282822828128.jpeg"
