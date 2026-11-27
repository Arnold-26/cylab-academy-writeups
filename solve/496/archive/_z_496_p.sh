#!/bin/bash
# usage: p.sh file1.eml file2.eml ...
for f in "$@"; do
  echo "### $f"
  timeout 120 node ./_z_496_parse.js "./_z_496_emls/$f" 2>&1 | head -c 3000
  echo
done
