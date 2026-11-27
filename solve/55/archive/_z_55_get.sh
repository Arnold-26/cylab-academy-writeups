#!/bin/bash
cd .
base=https://challenge-files.cylabacademy.net/library/3dd9b5fc772e139677d787dff53c1ca2d5319db46421cf5f1b7773adf7c3b9ff
mkdir -p _z_55 && cd _z_55
for f in sice_cream libc.so.6 ld-2.23.so; do
  [ -f "$f" ] || curl -s -o "$f" "$base/$f"
done
chmod +x sice_cream ld-2.23.so libc.so.6 2>/dev/null
ls -la
file sice_cream libc.so.6
echo "=== checksec"
readelf -h sice_cream | grep -E "Type|Entry"
readelf -lW sice_cream | grep -E "GNU_RELRO|GNU_STACK"
readelf -dW sice_cream | grep -E "BIND_NOW|NEEDED"
echo "=== libc version"
strings -a libc.so.6 | grep -m2 "GNU C Library"
echo "=== strings du binaire"
strings -a sice_cream | head -40
