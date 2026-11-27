#!/bin/bash
cd /tmp/cylab_bin || exit 1
ls -la 456_Windows_Logs.evtx
python3 -c "import Evtx; print('python-evtx ok')" 2>&1 | tail -1
which evtx_dump 2>/dev/null
which EvtxECmd 2>/dev/null
python3 - <<'EOF'
try:
    from Evtx.Evtx import Evtx
    print("import ok")
except Exception as e:
    print("import err:", e)
EOF
