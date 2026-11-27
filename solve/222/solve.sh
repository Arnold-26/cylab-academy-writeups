#!/bin/bash
# 222 - not crypto  (Reverse Engineering, picoMini by redpwn)
# Flag: picoCTF{c0mp1l3r_0pt1m1z4t10n_15_pur3_w1z4rdry_but_n0_pr0bl3m?}
# Write-up: ../../../writeups/reverse-engineering/222-not-crypto.md
# Script exact utilise pour produire le flag.
#
cd /tmp/cylab_eps || exit 1
cat > /tmp/hook.c <<'EOF'
#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
int memcmp(const void *a, const void *b, size_t n) {
    static int done = 0;
    if (!done && n >= 16) {
        done = 1;
        fprintf(stderr, "[HOOK] n=%zu\nA: ", n);
        fwrite(a, 1, n > 80 ? 80 : n, stderr);
        fprintf(stderr, "\nB: ");
        fwrite(b, 1, n > 80 ? 80 : n, stderr);
        fprintf(stderr, "\n");
        fprintf(stderr, "A hex: ");
        for (size_t i = 0; i < (n > 80 ? 80 : n); i++) fprintf(stderr, "%02x", ((unsigned char*)a)[i]);
        fprintf(stderr, "\nB hex: ");
        for (size_t i = 0; i < (n > 80 ? 80 : n); i++) fprintf(stderr, "%02x", ((unsigned char*)b)[i]);
        fprintf(stderr, "\n");
    }
    /* comparaison reelle */
    const unsigned char *x = a, *y = b;
    for (size_t i = 0; i < n; i++) if (x[i] != y[i]) return x[i] - y[i];
    return 0;
}
EOF
gcc -shared -fPIC -o /tmp/hook.so /tmp/hook.c 2>&1 | tail -2
chmod +x 222_not-crypto
LD_PRELOAD=/tmp/hook.so timeout 30 ./222_not-crypto AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA 2>&1 | tail -15
