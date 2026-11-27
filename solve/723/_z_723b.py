import sys, json, requests, re, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
f = "academy{i_c4n_b3_0wn3r_7a45d669}"
st, b = cy.req("GET", "/api/challenges/723/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 723, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"723 Access_Control (deja={already}) -> {ok}")
if ok and not already:
    wu.write(723, "Access_Control", "Blockchain", "eth node xebec.cylabacademy.net:<port>",
             "fonction changeOwner sans controle d'acces", f,
             "Contrat Solidity 0.8 avec une fonction `changeOwner(address)` declaree **`public` sans "
             "aucun controle d'acces** (pas de `onlyOwner`) : n'importe qui peut s'attribuer la "
             "propriete, puis appeler `solve()` qui exige `msg.sender == owner` et declenche "
             "`FlagRevealed`. Deux transactions suffisent : `changeOwner(<mon adresse>)` puis "
             "`solve()`, et `getFlag()` renvoie le secret. Point technique : le noeud n'expose pas de "
             "compte deverrouille, il fallait donc signer soi-meme. J'ai ecrit `ethlight.py` : "
             "keccak-256 (pycryptodome), RLP, et ECDSA secp256k1 en Python pur, avec signature legacy "
             "EIP-155 (`v = recid + 35 + 2*chainId`, normalisation low-s et bascule du recid). "
             "Verification : l'adresse derivee de la cle privee correspond exactement a celle du "
             "joueur, ce qui valide l'implementation avant d'envoyer quoi que ce soit.")
# details de 760
for port in (29641,):
    for attempt in range(3):
        try:
            r = requests.get(f"http://xebec.cylabacademy.net:{port}/", timeout=30, verify=False)
            t = re.sub(r"<style.*?</style>", " ", r.text, flags=re.S | re.I)
            t = re.sub(r"<script.*?</script>", " ", t, flags=re.S | re.I)
            t = re.sub(r"<[^>]+>", "\n", t)
            t = html.unescape(t)
            lines = [l.strip() for l in t.split("\n") if l.strip()]
            print(f"\n=== :{port} (essai {attempt+1}) ===")
            for l in lines[:28]:
                print("  ", l[:150])
            break
        except Exception as e:
            print(port, "essai", attempt + 1, "ERR", type(e).__name__)
