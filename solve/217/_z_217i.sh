#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
print_flag="academy{TESTLOCAL123}"
echo "$print_flag" > flag.txt
run() {
  printf '%s\n' "$1" > /tmp/bef.txt
  echo -n "[$2] -> "
  timeout 10 ./217_homework < /tmp/bef.txt 2>&1 | tail -c 120 | tr -d '\0'
  echo
}
# ligne 1 : rows=64 (v=64, x=0, y=50) puis lecture (col=8, row=52) et print
run '88*0 55*2*p8 55*2*2+g,@' "rows=64 puis g(8,52) avec ordre v,x,y"
run '88*055*2*0p8 55*2*2+g,@' "variante sans espace"
run '8 55*2*2+g,@' "lecture seule sans set rows"
