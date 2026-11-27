import io, sys

p = r".\flags.md"
raw = open(p, "rb").read()
text = raw.decode("utf-8")
lines = text.split("\n")

row = ("| 2026-11-27 | solfire (302) | pwn/solana | `academy{c9d4c62a}` | "
       "eBPF Solana sans toolchain : `clang -target bpf -mcpu=v1` + linker BPF maison "
       "(`mklink.py` : ET_DYN/EM_BPF, `sh_addr==sh_offset`, `.dynsym` collee a `.dynstr`, "
       "`DT_REL/SYMTAB/STRTAB`, appels `imm=-1` + reloc 8 pour rodata). Deux pieges mesures : "
       "clang 21 (v3) emet JMP32 0x56 -> `verifier::check` de solana_rbpf 0.2.19 = "
       "`UnknownOpCode(86,43)` -> panic au deploiement, socket fermee AVANT les pubkeys "
       "(fix: `-mcpu=v1`) ; et l'off-by-one de `handle_withdraw` n'est exploitable qu'avec un "
       "ledger de **0 octet** owner=solfire cree par NOTRE PDA (`invoke_signed`, `space=0`). "
       "`EbpfVm::new` mappe tout le buffer d'entrees comme UNE region `MM_INPUT_START`, donc "
       "`data+0x280*0x10` lit hors du padding 0x2800 (au lieu de faulter) -> depots bidons -> "
       "0x10000 lamports (user 10->65546, vault 934464). `accounts[0]` = "
       "`C1ock111111111111111111111111111111111111111` (compte inexistant -> data+0x20 = 0 < "
       "0x6230b800). Nonce vault obligatoire (invoke_signed `[\"vault\",nonce]`) |")

last = max(i for i, l in enumerate(lines) if l.startswith("|"))
lines.insert(last + 1, row)
out = "\n".join(lines).encode("utf-8")
open(p, "wb").write(out)
print("inserted after line", last + 1)
print("\n".join(lines[max(0, last - 2):last + 3]))
