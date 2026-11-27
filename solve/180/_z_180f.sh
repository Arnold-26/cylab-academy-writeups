#!/bin/bash
B="http://xebec.cylabacademy.net:38430"
for p in /admin.phps /index.phps; do
  echo "########## $p ##########"
  curl -s -m 15 "$B$p"
  echo
done
