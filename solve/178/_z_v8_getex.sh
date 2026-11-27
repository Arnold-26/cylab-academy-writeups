#!/bin/bash
cd /tmp/v8/src
curl -s -o tf_ex.js "https://raw.githubusercontent.com/exd0tpy/CTF-browser-challenges/main/Turboflan/ex.js"
curl -s -o dh_ex.js "https://raw.githubusercontent.com/exd0tpy/CTF-browser-challenges/main/Download_Horsepower/ex.js"
echo "===== Turboflan ex.js ($(wc -c < tf_ex.js) bytes) ====="
cat tf_ex.js
echo
echo "===== Download_Horsepower ex.js ($(wc -c < dh_ex.js) bytes) ====="
cat dh_ex.js
echo
