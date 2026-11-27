# 290 — Redaction gone wrong

**Événement** : picoCTF 2022 · **Catégorie** : Forensics

## Énoncé

« Maintenant vous ne me voyez plus. » Un rapport PDF (`Financial_Report_for_ABC_Labs.pdf`) contient des données sensibles, dont certaines ont été **caviardées correctement** et d'autres non. Il faut retrouver la clé qui n'a pas été masquée proprement.

## Analyse

Le caviardage correct consiste à **supprimer** le texte du flux du document, pas à le recouvrir. Ici l'auteur a dessiné des rectangles noirs **par-dessus** le texte existant :

- les glyphes sont toujours présents dans le contenu du PDF ;
- ils restent sélectionnables à la souris, copiables, et extractibles par n'importe quel outil d'extraction de texte ;
- seul le rendu visuel est masqué.

C'est exactement le type d'erreur qui a provoqué des fuites réelles dans des documents officiels diffusés au format PDF : l'image de la page montre un rectangle, mais la couche texte conserve tout.

Conséquence pratique : la zone « noire » n'a pas besoin d'être repérée visuellement. On extrait tout le texte du document et on cherche la valeur qui ne devrait pas s'y trouver.

Un PDF est une collection d'objets : des dictionnaires de page, des polices, et surtout des flux de contenu qui portent les instructions de dessin du texte. Les rectangles noirs sont des opérateurs de remplissage ajoutés dans un flux ; le texte, lui, reste dans le flux d'origine. C'est cette séparation entre ce qui est dessiné et ce qui est écrit qui rend l'extraction possible.

## Solution

### Extraction directe

```bash
pdftotext Financial_Report_for_ABC_Labs.pdf out.txt
grep -aoE "[A-Za-z0-9_]*\{[^}]*\}" out.txt
```

`pdftotext` reconstruit la couche texte page par page ; le motif générique isole le flag.

### Variantes

- ouverture dans un lecteur PDF puis sélection et copie de la zone « noire » ;
- extraction par bibliothèque :

```bash
python3 -c "import fitz; print(''.join(p.get_text() for p in fitz.open('Financial_Report_for_ABC_Labs.pdf')))"
```

- `strings` sur le PDF, efficace seulement si les objets de texte ne sont pas compressés.

La dernière zone caviardée du rapport correspond au flag, collé dans la continuité du texte comptable.

En cas de doute sur la bonne occurrence, on isole les passages qui contiennent une accolade et on compare leur structure : le flag est la chaîne la plus courte et la plus régulière du lot.

### Pourquoi ça marche

Le caviardage a été fait au niveau du rendu, pas du contenu. Le lecteur PDF affiche les rectangles parce qu'ils sont dessinés après le texte, mais rien n'a été retiré du document : le texte est toujours là, simplement recouvert.

Toute extraction qui lit la couche texte plutôt que l'image de la page retrouve donc la valeur intacte.

## Pièges

- **`strings` seul** : les flux de contenu PDF sont souvent compressés en Flate, donc `strings` ne montre rien. `pdftotext` décompresse.
- **Faire une capture d'écran** : la zone noire reste noire ; c'est la couche texte qu'il faut lire, pas l'image.
- **Copier dans le lecteur sans chercher** : le texte copié est mélangé à la mise en page ; un `grep` sur le fichier extrait est plus fiable.
- **Croire que toutes les zones sont récupérables** : celles qui ont été réellement supprimées ne le sont pas ; seules les zones recouvertes le sont.
- **N'extraire qu'une page** : le rapport en compte plusieurs, l'extraction doit porter sur l'ensemble du document.
- **Oublier l'espacement** : `pdftotext` conserve la mise en page et peut insérer des espaces dans la valeur ; le motif générique reste le plus sûr.
- **Passer par un OCR** : inutile ici, le texte est natif et parfaitement extractible.
- **Sauter les métadonnées** : `pdfinfo` donne le nombre de pages et la version du format, utile pour savoir si l'extraction a bien couvert tout le document.
- **Négliger l'encodage** : si `pdftotext` sort des caractères bizarres, un `-enc UTF-8` explicite règle le problème.
- **Valider sur une seule occurrence** : plusieurs chaînes du rapport ressemblent à des identifiants, seule celle qui porte le format du flag est la bonne.

## Flag

Flag validé sur la plateforme (valeur non conservée).
