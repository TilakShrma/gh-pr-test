#!/bin/bash
set -e

# Make sure the locally installed node executables are available to the script
export PATH=$PATH:./node_modules/.bin

# Run whatever command was passed to the script.
eval $@