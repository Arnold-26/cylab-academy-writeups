#!/bin/bash
set -u
REF=v1.10.0
BASE="https://raw.githubusercontent.com/solana-labs/solana/$REF/sdk/bpf/c/inc"
DEST=./_z_302/c/inc
mkdir -p "$DEST/sol"
cd "$DEST"

# top-level header
curl -sfL "$BASE/solana_sdk.h" -o solana_sdk.h && echo "ok solana_sdk.h" || echo "FAIL solana_sdk.h"

FILES="types.h entrypoint.h pubkey.h log.h mem.h memops.h string.h deserialize.h invoke.h \
parameters.h return_data.h allocator.h sha256.h keccak.h blake3.h secp256k1.h secp256k1_recover.h \
alt_bn128.h poseidon.h stable_log.h sysvar.h curve25519.h ed25519.h big_mod_exp.h"

for f in $FILES; do
  if curl -sfL --max-time 30 "$BASE/sol/$f" -o "sol/$f"; then
    echo "ok sol/$f ($(wc -c < sol/$f) bytes)"
  else
    echo "MISS sol/$f"
    rm -f "sol/$f"
  fi
done

echo "=== includes referenced by solana_sdk.h"
grep -o '#include *[<"][^>"]*[>"]' solana_sdk.h | sort -u
echo "=== files present"
ls -la sol/
