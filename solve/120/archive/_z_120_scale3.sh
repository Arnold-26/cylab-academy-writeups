#!/bin/bash
cd /tmp
echo "start $(date +%T)"
timeout 1200 python3 _z_120_toy.py 36
echo "rc=$? $(date +%T)"
