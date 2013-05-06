#!/bin/bash

# Quick script to change all tabs to spaces in python files within the git repository

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

find . -type f -name *.py -print0 | xargs -0 sed -i 's/\t/    /g'

