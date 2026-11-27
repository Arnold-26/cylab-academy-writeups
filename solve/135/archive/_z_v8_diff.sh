#!/bin/bash
for id in 135 168 178; do
  cd /tmp/v8/$id
  mkdir -p source_x && tar xzf source.tar.gz -C source_x
  echo "############ $id REVISION ############"
  cat source_x/source/REVISION
  echo
  echo "############ $id patch ############"
  cat source_x/source/patch
  echo
done
echo "############ server.py 178 ############"
cat /tmp/v8/178/server.py
