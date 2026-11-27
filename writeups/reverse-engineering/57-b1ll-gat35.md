# B1ll_Gat35

**Catégorie** : Reverse Engineering · **Challenge** : #57 · **Résolu le** : 2026-11-25

## Énoncé

> Can you reverse this Windows Binary?

## Résolution

Méthode : **windows memory scan**.

### Le contexte qui change tout

Le binaire est un **PE 32 bits Windows**. Les notes precedentes disaient « wine32 manquant,
donc impossible » : c'etait faux, on est sur Windows, le binaire tourne **nativement**. Meme
chose pour tout ce qui est `win-exec-*.exe`, `WinAntiDbg*` et le challenge `wine`.

```powershell
"12345`n4253360`n" | .\win-exec-1.exe
```

Le PE n'importe que `KERNEL32.dll` et son `.text` fait 434 Ko (runtime embarque), donc le
desassemblage statique est une impasse : les chaines ne sont referencees par aucune adresse
absolue dans le fichier (aucun `0x7b06c` en clair). Il faut regarder **a l'execution**.

### Lire la memoire du processus, sans debugger

Pas besoin de WinDbg : `OpenProcess(PROCESS_VM_READ)` + `VirtualQueryEx` +
`ReadProcessMemory` suffisent, et un programme qui attend une entree sur `stdin` reste
bloque donc parfaitement lisible.

Le programme lit d'abord un nombre (1 a 5 chiffres), calcule une cle, puis attend la cle.
On lui donne le nombre, on **n'ecrit pas** la cle, et on aspire ses regions memoire :

```python
p = subprocess.Popen([EXE], stdin=PIPE, stdout=PIPE)
p.stdin.write(b"12345\n")
for base, blob in read_regions(p.pid):          # VirtualQueryEx / ReadProcessMemory
    for m in re.finditer(rb"The key is", blob): ...
```

On trouve dans le tas :

```
...The key is: 4253360\x00...
```

### Le piege

La valeur `4253360` seule est **refusee** (`Incorrect key. Try again.`). La comparaison porte
sur la chaine **entiere**, prefixe compris : il faut taper `The key is: 4253360`.

```text
Input a number between 1 and 5 digits: Initializing...
Enter the correct key to get the access codes: Correct input. Printing flag:
academy{These are the access codes to the vault: 1063340}
```

Le numero de coffre (`1063340`) vaut :
seul le wrapper a change.

### A retenir

- Sur un binaire Windows d'apparence obfusquee, **la memoire est plus lisible que le code**.
- Un processus bloque sur `stdin` est un snapshot gratuit.
- Quand une valeur « evidente » est refusee, tester la **chaine complete** affichee autour
  (prefixe, separateur, casse).

## Flag

```
academy{These are the access codes to the vault: 1063340}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_57a.sh`](../../solve/57/_z_57a.sh)
- [`_z_57b.py`](../../solve/57/_z_57b.py)
- [`_z_57c.sh`](../../solve/57/_z_57c.sh)
- [`_z_57d.py`](../../solve/57/_z_57d.py)
- [`_z_57e.sh`](../../solve/57/_z_57e.sh)
- [`_z_57f.py`](../../solve/57/_z_57f.py)
- [`_z_57g.py`](../../solve/57/_z_57g.py)
