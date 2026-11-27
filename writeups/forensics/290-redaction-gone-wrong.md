# 290 — Redaction gone wrong

**Événement** : picoCTF 2022 · **Catégorie** : Forensics · **Auteur** : non précisé dans les sources consultées

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

« Maintenant vous ne me voyez plus. » Un rapport PDF (`Financial_Report_for_ABC_Labs.pdf`)
contient des données sensibles, dont certaines ont été **caviardées correctement** et d'autres
non. Il faut retrouver la clé qui n'a pas été masquée proprement.

## Analyse

Le caviardage (redaction) correct consiste à **supprimer** le texte du flux du document, pas à
le recouvrir. Ici l'auteur a dessiné des rectangles noirs **par-dessus** le texte existant :

- les glyphes sont toujours présents dans le contenu du PDF ;
- ils restent donc sélectionnables à la souris, copiables, et extractibles par n'importe quel
  outil d'extraction de texte ;
- seul le rendu visuel est masqué.

C'est exactement le type d'erreur qui a provoqué des fuites réelles dans des documents
officiels publiés en PDF.

## Solution

Extraction directe :

```bash
pdftotext Financial_Report_for_ABC_Labs.pdf out.txt
grep -o "picoCTF{.*}" out.txt
```

Variantes :

- ouverture dans un lecteur PDF puis sélection/copie de la zone « noire » ;
- `python3 -c "import fitz; print(fitz.open('rapport.pdf')[0].get_text())"` (PyMuPDF) ;
- `strings` sur le PDF pour retrouver les objets de texte non compressés.

La dernière zone caviardée du rapport correspond au flag, collé dans la continuité du texte
comptable.

## Flag

```
picoCTF{C4n_Y0u_S33_m3_fully}
```

## Sources

- https://ctftime.org/writeup/33096
- https://ctftime.org/writeup/33112
- https://www.it-sec.fail/picoctf-2022-forensics-redaction-gone-wrong/
