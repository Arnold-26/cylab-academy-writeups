#!/bin/bash
free -g | head -2
nproc
cd /tmp
echo "=== dp_bits=36 (L=2^18)"
/usr/bin/time -v timeout 1200 python3 _z_120_toy.py 36 2>&1 | grep -E "toy:|deg|multipoint|facteur|temps|Maximum resident|Elapsed" 
