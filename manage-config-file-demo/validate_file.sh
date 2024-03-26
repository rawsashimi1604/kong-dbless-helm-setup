#!/bin/bash

dockerImage="kong/deck:v1.36.1"

eval docker run --rm -v $PWD:/data $dockerImage validate -s /data/merged.yaml

# Capture the exit status of the Docker command
exitStatus=$?

if [ $exitStatus -ne 0 ]; then
    echo "Error: The command failed with exit status $exitStatus."
    exit $exitStatus
else
    echo "File valid."
fi
