#!/bin/bash
echo "=== checker (port 11534) ==="
timeout 30 nc xebec.cylabacademy.net 11534 < /dev/null 2>&1 | head -40
