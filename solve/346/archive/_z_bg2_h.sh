#!/bin/bash
cd /tmp/bg2
run() {
  timeout 2 ./_z_bg2 < "$1" 2>&1 | head -c 200000 > "$2"
  echo "exit=$?"
}
# test 1: two stamps in a row: lA d lB d
printf 'lAdlBd' > in1.bin
run in1.bin out1.txt
echo "--- test1: maps after each step; show row4 (5th line of each 31-line block) ---"
python3 - <<'EOF'
d=open('/tmp/bg2/out1.txt','rb').read().decode('latin1')
# split on the clear_screen escape if any; maps are 30 lines of 90 chars + last row
lines=d.split('\n')
rows=[l for l in lines if len(l)>=89 and set(l)<=set('.@XABCDEFGHijkl')]
for i in range(0,min(len(rows),60),30):
    print("MAP", i//30)
    for j in range(0,6):
        if i+j<len(rows): print(repr(rows[i+j][:30]))
EOF
