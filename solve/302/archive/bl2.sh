#!/bin/bash
echo "##### grep regions / memory in serialization.rs"
grep -n "region\|MemoryMapping\|fn serialize_parameters\|EbpfVm\|vm\." /tmp/bl_serialization.rs | head -30
echo "##### grep in lib.rs for execute setup"
grep -n "serialize_parameters\|EbpfVm::new\|set_memory_mapping\|execute_program\|fn execute" /tmp/bl_lib.rs | head -30
echo "##### serialization.rs lines 130-240"
sed -n '130,245p' /tmp/bl_serialization.rs
