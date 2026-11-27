#!/bin/bash
echo "=== strings in lld binaries for bpf"
for b in /usr/lib/llvm-21/bin/lld /usr/lib/llvm-21/bin/ld.lld /usr/bin/rust-lld; do
  [ -x "$b" ] || continue
  echo "--- $b"
  strings "$b" 2>/dev/null | grep -i "elf64bpf\|bpf" | sort -u | head -10
done
echo "=== rustc"
rustc --version
SYS=$(rustc --print sysroot)
echo "sysroot=$SYS"
ls "$SYS/lib/rustlib/x86_64-unknown-linux-gnu/bin/" 2>/dev/null
rustc --print target-list 2>/dev/null | grep -i bpf
echo "=== try rust-lld on our object"
cd ./_z_302
RL="$SYS/lib/rustlib/x86_64-unknown-linux-gnu/bin/rust-lld"
if [ -x "$RL" ]; then
  "$RL" -flavor gnu -shared -e entrypoint -o /tmp/t_rustlld.so solve.o && echo "LINK OK" && file /tmp/t_rustlld.so || echo "LINK FAILED"
  "$RL" -flavor gnu -m elf64bpf -shared -e entrypoint -o /tmp/t2.so solve.o && echo "LINK2 OK" || echo "LINK2 FAILED"
fi
