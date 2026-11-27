#!/bin/bash
D=~/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana_rbpf-0.2.19
echo "=== SyscallObject trait"
grep -n "pub trait SyscallObject" -A 15 "$D/src/vm.rs"
echo "=== SyscallFunction type"
grep -n "pub type SyscallFunction" -A 3 "$D/src/vm.rs"
echo "=== from_elf in elf.rs"
grep -n "pub fn from_elf" -A 12 "$D/src/elf.rs"
echo "=== verifier::check signature"
grep -n "pub fn check" -A 6 "$D/src/verifier.rs" | head -20
echo "=== Config fields all"
sed -n '/pub struct Config {/,/^}/p' "$D/src/vm.rs" | grep "pub "
