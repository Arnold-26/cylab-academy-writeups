import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{Sm4r7_OverFL0ws_ExI5t_bfaa16cd}"
st, b = cy.req("GET", "/api/challenges/760/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 760, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"760 Smart_Overflow (deja={already}) -> {ok}")
if ok and not already:
    wu.write(760, "Smart_Overflow", "Blockchain", "eth node xebec.cylabacademy.net:<port>",
             "integer overflow uint256 sur le solde (Solidity 0.6)", f,
             "Contrat `IntOverflowBank` en **Solidity `^0.6.12`** : avant 0.8, les operations sur "
             "`uint256` ne sont pas verifiees et **debordent silencieusement**. La fonction "
             "`deposit(uint256 amount)` fait `balances[msg.sender] += amount` puis teste "
             "`if (!revealed && balances[msg.sender] < amount)` pour reveler le flag, ce qui est "
             "impossible normalement. On exploite le wrap : `deposit(1)` met le solde a 1, puis "
             "`deposit(2^256 - 1)` calcule `1 + (2^256-1) = 0` modulo 2^256, donc le solde devient 0, "
             "or `0 < 2^256-1` est vrai -> `revealed = true`. `getFlag()` renvoie alors le secret. "
             "Deux transactions suffisent, sans ether (le montant est un parametre, pas une valeur "
             "envoyee). Signature maison avec `ethlight.py` (keccak + RLP + ECDSA secp256k1, EIP-155) "
             "car le noeud n'expose aucun compte deverrouille.")
