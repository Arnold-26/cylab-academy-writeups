#!/bin/bash
echo "=== lib.rs 60-130"
sed -n '60,130p' /tmp/bl_lib.rs
echo
echo "=== syscall registry names in syscalls.rs"
grep -n "register_syscall_by_name\|fn create_syscall_registry\|fn register_syscall" /tmp/bl_syscalls.rs | head -50
