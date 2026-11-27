#!/bin/bash
echo "=== does upstream lld have BPF?"
for ref in main release/14.x release/15.x release/16.x release/17.x release/18.x; do
  c=$(curl -s -o /dev/null -w "%{http_code}" "https://raw.githubusercontent.com/llvm/llvm-project/$ref/lld/ELF/Arch/BPF.cpp")
  echo "$ref lld/ELF/Arch/BPF.cpp -> $c"
done
echo "=== rust gcc-ld dir"
SYS=$(rustc --print sysroot)
ls -la "$SYS/lib/rustlib/x86_64-unknown-linux-gnu/bin/gcc-ld/" 2>/dev/null
echo "=== apt candidates for lld"
apt-cache policy lld-14 lld-15 lld-16 lld-17 lld-18 lld-19 2>/dev/null | grep -E '^(lld|  Candidate)' | head -20
echo "=== throughput test on real asset (20MB range)"
timeout 120 curl -sL -r 0-20000000 -o /tmp/spd2.bin -w "size=%{size_download} time=%{time_total} speed_Bps=%{speed_download}\n" \
  https://github.com/solana-labs/solana/releases/download/v1.10.31/solana-release-x86_64-unknown-linux-gnu.tar.bz2
