# Secret of the Polyglot

**Catégorie** : Forensics · **Challenge** : #423

## Énoncé

> The Network Operations Center (NOC) of your local institution picked up a
> suspicious file, they're getting conflicting information on what type of file
> it is. They've brought you in as an external expert to examine the file. Can
> you extract all the information from this strange file?
>
> Download the suspicious file [here](https://challenge-files.cylabacademy.net/library/70f90e64dbbf4b6c6da7c0cd024663e66eb3fecf36dde7c7947c96debe14885a/flag2of2-final.pdf).

## Résolution

Le fichier est un PNG (police 200×40) qui contient aussi un PDF. OCR du PNG (`tesseract`) donne `academy{f1u3n7_`, `pdftotext` donne `1n_pn9_&_pdf_2f8da0be}`.

## Flag

```
academy{f1u3n7_1n_pn9_&_pdf_2f8da0be}
```

## Ce qu'il faut retenir

Un polyglotte se lit avec **deux** lecteurs différents.
