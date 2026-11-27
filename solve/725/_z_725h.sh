#!/bin/bash
which tor torsocks 2>/dev/null
echo "---"
echo arnold | sudo -S apt-get install -y -qq tor torsocks 2>&1 | tail -2
which tor torsocks
