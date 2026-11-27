#!/bin/bash
cd /tmp/toris 2>/dev/null || { mkdir -p /tmp/toris && cd /tmp/toris; }
cat > torrc <<'EOF'
SocksPort 9050
ExitNodes {is}
StrictNodes 0
Log notice file /tmp/toris/tor.log
DataDirectory /tmp/toris/data
EOF
rm -rf data tor.log
tor -f /tmp/toris/torrc >/dev/null 2>&1 &
TPID=$!
for i in $(seq 1 240); do
  if grep -q "Bootstrapped 100" /tmp/toris/tor.log 2>/dev/null; then
    echo "BOOTSTRAP OK apres ${i}s"; break
  fi
  if ! kill -0 $TPID 2>/dev/null; then echo "tor est mort a ${i}s"; break; fi
  sleep 1
done
echo "--- dernieres lignes ---"
tail -6 /tmp/toris/tor.log
echo "--- exit ip ---"
curl -s -m 40 --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/api/ip | head -c 200
echo
echo "--- requete service ---"
curl -s -m 45 --socks5-hostname 127.0.0.1:9050 "http://xebec.cylabacademy.net:29650/" | head -c 600
echo
kill $TPID 2>/dev/null
