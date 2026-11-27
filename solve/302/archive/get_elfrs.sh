#!/bin/bash
curl -sL -o /tmp/elf_0219.rs https://raw.githubusercontent.com/solana-labs/rbpf/v0.2.19/src/elf.rs
echo "size: $(stat -c%s /tmp/elf_0219.rs)"
cp /tmp/elf_0219.rs ./_z_302/rbpf_elf_0.2.19.rs
grep -n "fn load\|e_type\|ET_DYN\|e_machine\|EM_BPF\|fn relocate\|R_BPF_64_32\|R_BPF_64_64\|syscall\|\.text\|\.rodata\|\.dynsym\|\.dynstr\|\.rel.dyn\|\.rel.text\|sh_offset\|e_entry" /tmp/elf_0219.rs | head -80
