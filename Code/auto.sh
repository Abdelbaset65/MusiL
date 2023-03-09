#!/bin/bash
# This script takes a directory as input
# and loops over all files in that directory
# and runs a command against each file

command="python3 remove_music.py -r"

# Check if a directory is provided as argument
if [ -z "$1" ]; then
  echo "Please provide the subclips path."
  exit 1
fi

# Loop over all files in the given directory
for file in "$1"/*; do
  # Check if it is a regular file (not a directory or other type)
  if [ -f "$file" ]; then
    # Run the command with the file name as argument
    $command "$file"
  fi
done