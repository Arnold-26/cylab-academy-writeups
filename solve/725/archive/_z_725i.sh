#!/bin/bash
U=$(cat ./_z_725url.txt)
echo "URL=$U"
echo "=== direct (doit dire 'No flag in this region') ==="
curl -s -m 25 -i "$U/" | head -12
echo
echo "=== demarrage tor (exit IS) ==="
cd /tmp/toris || exit 1
cat > torrc <<'EOF'
SocksPort 9050
ExitNodes {is}
StrictNodes 0
Log notice file /tmp/toris/tor.log
DataDirectory /tmp/toris/data
EOF
pkill -f "tor -f /tmp/toris/torrc" 2>/dev/null
rm -rf data tor.log
tor -f /tmp/toris/torrc >/dev/null 2>&1 &
TPID=$!
for i in $(seq 1 300); do
  grep -q "Bootstrapped 100" /tmp/toris/tor.log 2>/dev/null && { echo "tor pret en ${i}s"; break; }
  kill -0 $TPID 2>/dev/null || { echo "tor mort"; break; }
  sleep 1
done
echo "=== requete via Tor ==="
curl -s -m 60 --socks5-hostname 127.0.0.1:9050 -i "$U/" | head -25
kill $TPID 2>/dev/null
