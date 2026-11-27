#!/bin/bash
# Build + link the eBPF solver (clang -> ET_REL, mklink.py -> ET_DYN for rbpf)
set -e
cd /mnt/d/ctf-index/_z_302
CC=${CC:-/usr/bin/clang-21}
echo "clang: $($CC --version | head -1)"
# NOTE: -mcpu=v1 is mandatory. clang's default (v3) emits JMP32 (opcode 0x56),
# which solana_rbpf 0.2.19's verifier rejects: UnknownOpCode(86, 43) -> deploy
# panics and the service closes the socket before sending the pubkeys.
$CC -target bpf -mcpu=v1 -O2 -fPIC -nostdlib -c -I c/inc \
    -mllvm -bpf-stack-size=4096 -Wno-everything \
    solve.c -o solve.o
echo "--- object: $(stat -c%s solve.o) bytes"
python3 mklink.py solve.o solve.so
echo "--- verify"
file solve.so
readelf -h solve.so | grep -E 'Type|Machine|Entry|program headers'
readelf -SW solve.so
readelf -sW --dyn-syms solve.so
readelf -rW solve.so
readelf -dW solve.so
readelf -lW solve.so
