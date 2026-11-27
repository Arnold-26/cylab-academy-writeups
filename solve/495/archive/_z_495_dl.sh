#!/bin/bash
set -e
B=https://challenge-files.cylabacademy.net/library/93a1a0358261c4586ade91082cecc590ead0208df1c4ea1a67ab5f06ab635fd5
rm -rf /tmp/r495 && mkdir -p /tmp/r495 && cd /tmp/r495
for f in radio_interface.py robot.py robotcontroller.py crypto.py; do curl -sSL -o "$f" "$B/$f"; done
ls -la
for f in *.py; do echo "===== $f ====="; wc -l "$f"; done
