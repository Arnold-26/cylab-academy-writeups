#!/bin/bash
set -e
B=https://challenge-files.cylabacademy.net/library/ace300e270d489b26f917e742f3d08fe002bbcb5eca8a7ccad4a38cfaed921df
rm -rf /tmp/s164 && mkdir -p /tmp/s164 && cd /tmp/s164
curl -sSL -o vuln "$B/vuln"
curl -sSL -o vuln.c "$B/vuln.c"
curl -sSL -o Makefile.share "$B/Makefile.share"
ls -la
echo "=== md5 plateforme ==="
md5sum vuln vuln.c Makefile.share
echo "=== md5 copie locale ==="
md5sum ./_z_164/vuln ./_z_164/vuln.c ./_z_164/Makefile.share
echo "=== diff vuln.c ==="
diff vuln.c ./_z_164/vuln.c && echo IDENTIQUE_vuln.c
echo "=== diff Makefile ==="
diff Makefile.share ./_z_164/Makefile.share && echo IDENTIQUE_makefile
