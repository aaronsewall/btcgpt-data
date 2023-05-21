#!/bin/bash
# Run this script to extract all the historical output.json files to content-dumps
# Adapted from https://stackoverflow.com/a/60480966 
file=output.json
n=0   
mkdir -p content-dumps
git log --pretty= --diff-filter=d --raw -- $file |
while read m1 m2 h1 h2 rest; do
 redirto=content-dumps/$((n++))_$h2.$file; git show $h2 > $redirto
done
