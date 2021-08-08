#!/bin/sh

EDITOR=nvim
TEMPFILE=/tmp/blog_entry.md

$EDITOR $TEMPFILE

NAME=src/$(head -1 $TEMPFILE | cut -d" " -f2-).md

cp $TEMPFILE "$NAME"
rm $TEMPFILE
python build.py

./sync.sh
