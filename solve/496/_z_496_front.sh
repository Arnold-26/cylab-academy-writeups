#!/bin/bash
cd /mnt/d/ctf-index/_z_496/frontend || exit 1
for f in src/api.js src/email.js src/smime.js email.html reply.html inbox.html index.html; do
  echo "########## $f ##########"
  cat "$f"
  echo
done
