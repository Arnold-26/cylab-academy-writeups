#!/bin/bash
mkdir -p /tmp/toris && cd /tmp/toris || exit 1
cat > torrc <<'EOF'
SocksPort 9050
ExitNodes {is}
StrictNodes 1
Log notice file /tmp/toris/tor.log
DataDirectory /tmp/toris/data
EOF
rm -rf data tor.log
tor -f /tmp/toris/torrc >/dev/null 2>&1 &
TPID=$!
echo "tor pid $TPID"
for i in $(seq 1 90); do
  if grep -q "Bootstrapped 100" /tmp/toris/tor.log 2>/dev/null; then
    echo "bootstrap OK apres ${i}s"
    break
  fi
  sleep 1
done
tail -3 /tmp/toris/tor.log 2>/dev/null
echo "=== verification de l'exit ==="
curl -s -m 30 --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/api/ip 2>/dev/null | head -c 200
echo
echo "=== requete du service via Tor ==="
curl -s -m 40 --socks5-hostname 127.0.0.1:9050 -i "http://xebec.cylabacademy.net:29650/" 2>&1 | head -40
kill $TPID 2>/dev/null
