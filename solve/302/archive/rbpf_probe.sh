#!/bin/bash
# Inspect solana_rbpf elf loader: does it accept ET_REL?
cd /tmp
for tag in v0.2.14 v0.2.16 v0.2.18 v0.3.0; do
  code=$(curl -s -o /tmp/elf_$tag.rs -w "%{http_code}" https://raw.githubusercontent.com/solana-labs/rbpf/$tag/src/elf.rs)
  echo "$tag -> $code $(stat -c%s /tmp/elf_$tag.rs 2>/dev/null)"
done
F=/tmp/elf_v0.2.14.rs
if [ -s "$F" ]; then
  echo "=== e_type / ET_DYN checks"
  grep -n "e_type\|ET_DYN\|ET_REL\|WrongELF\|ELFError" "$F" | head -40
  echo "=== EM_BPF / machine"
  grep -n "e_machine\|EM_BPF\|UnsupportedElfHeader\|Unsupported" "$F" | head -30
fi
