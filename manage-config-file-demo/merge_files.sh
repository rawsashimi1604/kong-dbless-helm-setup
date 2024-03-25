#!/bin/bash

dockerImage="kong/deck:v1.36.1"
outputFormat="yaml"

# Find all yaml files in the directories and store them in arrays
globalFiles=(./global/*.yaml)
serviceFiles=(./services/*.yaml)

# Echo the files for logging
echo "Global Files:"
printf "%s\n" "${globalFiles[@]}"
echo "Service Files:"
printf "%s\n" "${serviceFiles[@]}"

# Use Docker to run the deck command. Each file path needs to be passed individually to the docker run command.
# Start the docker command
dockerCmd="docker run --rm -v $PWD:/data $dockerImage file render"

# Add each global file to the command
for file in "${globalFiles[@]}"; do
  dockerCmd+=" /data/${file#./}"
done

# Add each service file to the command
for file in "${serviceFiles[@]}"; do
  dockerCmd+=" /data/${file#./}"
done

# Finish constructing the command
dockerCmd+=" -o /data/merged.$outputFormat --format $outputFormat --analytics=false"

# Execute the command
eval $dockerCmd
echo "File generated: merged.$outputFormat"
