#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file-to-move>"
    exit 1
fi

FILE_TO_MOVE=$1
DEST_DIR="/home/$USER/.config/autostart/"

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Move the file to the destination directory
cp "$FILE_TO_MOVE" "$DEST_DIR"

echo "File moved to $DEST_DIR"