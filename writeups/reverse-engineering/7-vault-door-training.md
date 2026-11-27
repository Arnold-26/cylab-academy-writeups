# 7 — vault-door-training

**Événement** : picoCTF 2019 · **Catégorie** : Reverse Engineering · **Auteur** : Mark E. Haase

## Énoncé

Le laboratoire du Dr Evil est protégé par une série de portes blindées, chacune pilotée par un
programme Java. Les agents n'ont pas récupéré les mots de passe, mais disposent du code source de la
porte d'entraînement : `VaultDoorTraining.java`. L'indice précise que le mot de passe est visible
dans le source du programme.

## Analyse

Le fichier fait quelques dizaines de lignes. On le lit en entier plutôt que de chercher au hasard :

```java
import java.util.*;

class VaultDoorTraining {
    public static void main(String args[]) {
        VaultDoorTraining vaultDoor = new VaultDoorTraining();
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter vault password: ");
        String userInput = scanner.next();
        String input = userInput.substring(9, userInput.length()-1);  // 9 = longueur du préfixe
        if (vaultDoor.checkPassword(input)) {
            System.out.println("Access granted.");
        } else {
            System.out.println("Access denied!");
        }
    }

    public boolean checkPassword(String password) {
        return password.equals("<mot_de_passe_extrait_du_source>");
    }
}
```

Deux éléments structurent la lecture.

D'abord le découpage : `substring(9, userInput.length()-1)` retire le préfixe de neuf caractères et
l'accolade fermante. C'est donc le **contenu** du flag qui est comparé, pas la chaîne complète. Cela
indique aussi le format attendu à la saisie, et permet de reconstituer le flag en réinsérant
l'enveloppe.

Ensuite la comparaison : `checkPassword` ne calcule rien. Elle ne fait aucun hachage, aucune
transformation, aucun contrôle anti-debug : le secret est un littéral de chaîne, présent en clair
dans le source livré.

Le « reverse » se limite donc à la lecture. C'est la leçon de la série vault-door, et elle est ici
donnée sans détour : un secret embarqué dans le programme livré — ou dans son code source — est un
secret public.

## Solution

1. Récupérer le fichier `VaultDoorTraining.java` fourni par la plateforme.

2. Localiser la comparaison sans lire tout le fichier :

```bash
grep -n "equals" VaultDoorTraining.java
```

3. Extraire la valeur comparée :

```bash
grep -o 'equals("[^"]*")' VaultDoorTraining.java
```

4. Reconstituer le flag en replaçant la valeur extraite entre le préfixe de l'événement et une
   accolade fermante.

5. Vérification fonctionnelle, utile pour confirmer que le format de saisie est le bon :

```bash
javac VaultDoorTraining.java
java VaultDoorTraining
# Enter vault password: <flag reconstitué>
# Access granted.
```

6. Contrôle croisé sur le fichier compilé, sans passer par le source :

```bash
javap -c VaultDoorTraining.class | grep -A3 equals
strings VaultDoorTraining.class | grep -i -E 'vault|access'
```

Le littéral apparaît dans la constante du pool de la classe : le compiler ne protège rien.

## Pièges

- **Comparer le flag complet au lieu du contenu.** `checkPassword` reçoit la chaîne déjà amputée du
  préfixe et de l'accolade : passer le contenu seul est correct, passer le flag entier échoue à
  cause des neuf caractères retirés.
- **`scanner.next()` et non `nextLine()`.** La lecture s'arrête au premier blanc : un mot de passe
  contenant une espace serait tronqué. Ici il n'y en a pas, mais le réflexe vaut pour les portes
  suivantes de la série.
- **Croire à une obfuscation.** Aucune chaîne n'est construite dynamiquement ni encodée en base64 :
  chercher un décodage à appliquer est une fausse piste.
- **Négliger le contrôle final.** Une valeur mal recopiée (un caractère, une casse) échoue
  silencieusement ; le `javac`/`java` local tranche en une seconde.

**Pourquoi ça marche.** La vérification est une égalité de chaînes exécutée sur la machine de
l'utilisateur, avec la valeur attendue présente dans le fichier remis. Le canal de livraison du
programme est aussi celui du secret : toute la protection tient à la supposition que personne ne
lira le code. Un `grep` suffit à la renverser.

## Flag

Flag validé sur la plateforme (valeur non conservée).
