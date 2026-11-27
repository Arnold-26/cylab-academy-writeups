# 7 — vault-door-training

**Événement** : picoCTF 2019 · **Catégorie** : Reverse Engineering · **Auteur** : Mark E. Haase

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Le laboratoire du Dr Evil est protégé par une série de portes blindées, chacune pilotée par un
programme Java. Les agents n'ont pas récupéré les mots de passe, mais disposent du code source de
la porte d'entraînement : `VaultDoorTraining.java`. L'indice précise que le mot de passe est
visible dans le source du programme.

## Analyse

Le `main` lit une chaîne au clavier, en extrait la partie utile, puis la compare au secret :

```java
String input = userInput.substring("picoCTF{".length(), userInput.length()-1);
if (vaultDoor.checkPassword(input)) { ... }
```

Le `substring(9, len-1)` retire le préfixe `picoCTF{` et l'accolade fermante : c'est bien le
contenu du flag qui est comparé. La méthode `checkPassword` ne calcule rien, elle contient le
secret en clair :

```java
public boolean checkPassword(String password) {
    return password.equals("w4rm1ng_Up_w1tH_jAv4_eec0716b713");
}
```

Aucune obfuscation, aucun chiffrement, aucun contrôle anti-debug : le « reverse » se limite à la
lecture du source. C'est la leçon de la série vault-door — un secret embarqué dans le programme
livré (ou dans son source) est un secret public, et une comparaison en clair se lit en trois
secondes avec `strings` ou un simple `grep`.

## Solution

1. Récupérer le fichier `VaultDoorTraining.java` fourni par la plateforme.
2. Localiser la comparaison :

```bash
grep -n "equals" VaultDoorTraining.java
```

3. Reconstituer le flag en réinsérant le préfixe et l'accolade : `picoCTF{` + valeur + `}`.
4. Vérification fonctionnelle (optionnelle) :

```bash
javac VaultDoorTraining.java
java VaultDoorTraining
# Enter vault password: picoCTF{w4rm1ng_Up_w1tH_jAv4_eec0716b713}
# Access granted.
```

## Flag

`picoCTF{w4rm1ng_Up_w1tH_jAv4_eec0716b713}`

## Sources

- https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/master/picoCTF_2019/Reverse_Engineering/vault-door-training.md — énoncé, code source complet, valeur du mot de passe et lien vers la fiche CyLab Academy n° 7
