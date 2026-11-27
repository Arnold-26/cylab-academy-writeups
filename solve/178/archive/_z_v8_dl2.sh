#!/bin/bash
mkdir -p /tmp/v8/135 /tmp/v8/168 /tmp/v8/178
cd /tmp/v8
for pair in "135 e54854c91dd94b9dcb7daca4b2f828ee3a3caa48e88a9c0b4855277576ed0c19" \
            "168 59e51a5b7346fe4e519eb904782d00d5f61d4dfec7dfb73838a98ee1a2fbae21" \
            "178 3d1baa1df25f41c90d4cb5cff8d559ef06a27e58fbb0ef5d1877e7c69bfd31b6"; do
  set -- $pair
  id=$1; h=$2
  curl -s -o $id/source.tar.gz   "https://challenge-files.cylabacademy.net/library/$h/source.tar.gz"
  curl -s -o $id/server.py       "https://challenge-files.cylabacademy.net/library/$h/server.py"
done
ls -la /tmp/v8/135 /tmp/v8/168 /tmp/v8/178
for id in 135 168 178; do
  echo "===== $id source.tar.gz ====="
  cd /tmp/v8/$id && tar tzf source.tar.gz 2>&1 | head -20
done
