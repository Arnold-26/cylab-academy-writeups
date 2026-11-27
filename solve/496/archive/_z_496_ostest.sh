#!/bin/bash
set -e
cd /tmp/ostest
rm -rf * 2>/dev/null || true
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 2 -subj "/CN=admin@ses" 2>/dev/null
# inner content (what smail signs)
B1='===============0344718024407626035=='
printf -- '--%s\nContent-Type: text/plain\n\nhello\n--%s--\n' "$B1" "$B1" > inner.txt
openssl cms -sign -in inner.txt -signer cert.pem -inkey key.pem -outform SMIME -out signed.eml -md sha256 2>/dev/null
echo "=== signed.eml ==="
head -c 900 signed.eml
echo
echo "=== verify clean ==="
openssl cms -verify -in signed.eml -CAfile cert.pem -out out.txt; echo "rc=$?"
