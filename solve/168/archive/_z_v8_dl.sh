#!/bin/bash
set -x
mkdir -p /tmp/v8/{135,168,178}
cd /tmp/v8/135
curl -sL -o d8 "https://challenge-files.cylabacademy.net/library/e54854c91dd94b9dcb7daca4b2f828ee3a3caa48e88a9c0b4855277576ed0c19/d8"
curl -sL -o source.tar.gz "https://challenge-files.cylabacademy.net/library/e54854c91dd94b9dcb7daca4b2f828ee3a3caa48e88a9c0b4855277576ed0c19/source.tar.gz"
curl -sL -o server.py "https://challenge-files.cylabacademy.net/library/e54854c91dd94b9dcb7daca4b2f828ee3a3caa48e88a9c0b4855277576ed0c19/server.py"
cd /tmp/v8/168
curl -sL -o d8 "https://challenge-files.cylabacademy.net/library/59e51a5b7346fe4e519eb904782d00d5f61d4dfec7dfb73838a98ee1a2fbae21/d8"
curl -sL -o source.tar.gz "https://challenge-files.cylabacademy.net/library/59e51a5b7346fe4e519eb904782d00d5f61d4dfec7dfb73838a98ee1a2fbae21/source.tar.gz"
curl -sL -o server.py "https://challenge-files.cylabacademy.net/library/59e51a5b7346fe4e519eb904782d00d5f61d4dfec7dfb73838a98ee1a2fbae21/server.py"
cd /tmp/v8/178
curl -sL -o d8 "https://challenge-files.cylabacademy.net/library/3d1baa1df25f41c90d4cb5cff8d559ef06a27e58fbb0ef5d1877e7c69bfd31b6/d8"
curl -sL -o source.tar.gz "https://challenge-files.cylabacademy.net/library/3d1baa1df25f41c90d4cb5cff8d559ef06a27e58fbb0ef5d1877e7c69bfd31b6/source.tar.gz"
curl -sL -o server.py "https://challenge-files.cylabacademy.net/library/3d1baa1df25f41c90d4cb5cff8d559ef06a27e58fbb0ef5d1877e7c69bfd31b6/server.py"
chmod +x /tmp/v8/*/d8
ls -la /tmp/v8/135 /tmp/v8/168 /tmp/v8/178
file /tmp/v8/*/d8
