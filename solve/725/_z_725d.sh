#!/bin/bash
which tor torsocks 2>/dev/null
tor --version 2>/dev/null | head -2
echo "--- test de connectivite au port 9050 ---"
(echo > /dev/tcp/127.0.0.1/9050) 2>/dev/null && echo "tor deja en ecoute" || echo "pas de tor actif"
