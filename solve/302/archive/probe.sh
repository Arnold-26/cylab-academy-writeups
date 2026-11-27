#!/bin/bash
for c in clang clang-21 clang-15 clang-14 ld.lld lld llvm-objdump cargo rustc gcc python3 nc objdump readelf file git curl; do
  if command -v "$c" >/dev/null 2>&1; then echo "$c -> $(command -v $c)"; else echo "$c -> MISSING"; fi
done
echo "=== clang version"
clang --version 2>/dev/null | head -3
echo "=== bpf target"
clang -print-targets 2>/dev/null | grep -i bpf
echo "=== uname"
uname -a
echo "=== net test"
timeout 10 curl -sSI https://github.com 2>&1 | head -3
