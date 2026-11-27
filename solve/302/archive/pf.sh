#!/bin/bash
cd /tmp
rm -rf pf && mkdir pf && cd pf
curl -sL -o pf.crate "https://crates.io/api/v1/crates/poc-framework/0.1.4/download"
echo "size: $(stat -c%s pf.crate)"
tar xzf pf.crate
ls
D=$(find . -maxdepth 1 -type d -name 'poc-framework*')
echo "=== dir: $D"
ls "$D/src"
echo "=== deploy_program"
grep -rn "fn deploy_program" -A 40 "$D/src" | head -70
