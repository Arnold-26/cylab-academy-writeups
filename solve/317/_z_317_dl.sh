#!/bin/bash
set -e
B=https://challenge-files.cylabacademy.net/library/2d2c616c8d0ea08421ea63d44b20300fbfc5cf54c67e538bece57addf950e573
rm -rf /tmp/w317 && mkdir -p /tmp/w317 && cd /tmp/w317
curl -sSL -o vuln.zip "$B/vuln.zip"
ls -la
unzip -o -P academy vuln.zip
ls -la
for f in *; do file "$f"; done
