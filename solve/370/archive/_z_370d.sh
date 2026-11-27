#!/bin/bash
cd . || exit 1
echo "=== envoi du warrior Gnat ==="
timeout 120 nc xebec.cylabacademy.net 40588 < _z_gnat.red 2>&1 | tail -30
