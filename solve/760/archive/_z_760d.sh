#!/bin/bash
echo "=== web3 python ==="
python3 -c "import web3; print('web3', web3.__version__)" 2>&1 | tail -2
echo "=== outils ==="
for t in cast solc forge anvil node npm; do which $t 2>/dev/null || true; done
echo "=== eth-account ==="
python3 -c "import eth_account; print('eth_account ok')" 2>&1 | tail -1
