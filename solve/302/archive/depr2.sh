#!/bin/bash
echo "=== finalize in bpf_loader lib.rs"
grep -n "fn finalize\|fn deploy\|bpf_verifier\|reject_unresolved_syscalls\|reject_all_writable\|from_elf\|verify_program" /tmp/bl_lib.rs | head -40
echo
grep -n "fn finalize" -A 60 /tmp/bl_lib.rs | head -90
