# 699 — Binary Instrumentation 3

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

## Énoncé
« The executable was designed to write the flag but it seems like a few things went wrong. Can you
find a way to get it to work? »

`bin-ins3.zip` (mot de passe `picoctf`) contient un exécutable Windows, `bin-ins3.exe`, censé écrire
le flag dans un fichier de sortie. Le fichier produit ne contient que des déchets.

## Analyse

### Constat de départ
```bash
unzip -P picoctf bin-ins3.zip
file bin-ins3.exe
./bin-ins3.exe
```

Le programme crée bien `C:\random\output_flag.txt`, mais son contenu est illisible. Un `strings` sur
le fichier ne donne ni chaîne au format du flag, ni base64 crédible : la logique utile n'est pas sur
disque.

### Le binaire est packé
Le PE n'est qu'un **stub** : il alloue de la mémoire, décompresse une charge utile, puis transfère
l'exécution à son point d'entrée. Toute la logique réelle — y compris la construction du flag — vit
dans cette image reconstruite en mémoire.

### La routine anti-dump
La raison pour laquelle la sortie est polluée est une routine d'**effacement d'en-tête** du packer,
que l'on retrouve dans IDA sous le nom `sub_1400015A0`. Juste après l'expansion du payload, elle met
à zéro les premiers octets de l'image (signature `MZ`, en-tête `PE`). Un dump naïf ne contient alors
plus d'en-tête valide, et les outils qui attendent un PE bien formé refusent de l'ouvrir.

Conséquence : la recherche statique de chaîne est condamnée. Le flag n'existe qu'en mémoire, et sous
forme **base64**.

## Solution

### Repérer le point de bascule
```bash
pip install frida-tools
frida-trace .\bin-ins3.exe -I 'bin-ins3.exe'
```

On repère l'appel qui précède immédiatement le transfert vers le payload : c'est le dernier instant où
l'image complète est encore intacte. Tout ce qui suit est trop tard.

### Dumper avant l'effacement
Le script `dump_payload.py` fait quatre choses : `spawn` du processus (et non `attach`, pour ne rien
manquer du package) ; hook de `sub_1400015A0` en `onEnter`, donc avant l'écrasement ; lecture de
`SizeOfImage` dans l'en-tête optionnel — celui-ci commence à `PE + 0x18` et `SizeOfImage` se trouve à
`+0x38`, soit `PE + 0x50` ; copie de `SizeOfImage` octets puis écriture sur disque.

```python
import frida, sys

JS = """
const base   = Module.getBaseAddress('bin-ins3.exe');
const lfanew = base.add(0x3C).readU32();
const optHdr = base.add(lfanew).add(0x18);
const size   = optHdr.add(0x38).readU32();   // SizeOfImage

Interceptor.attach(base.add(0x15A0), {       // sub_1400015A0
  onEnter() {
    const f = new File('payload_dumped.exe', 'wb');
    f.write(base.readByteArray(size)); f.flush(); f.close();
    send('dump: ' + size);
  }
});
"""

def on_message(m, d): print(m)

pid = frida.spawn(['bin-ins3.exe'])
s = frida.attach(pid)
sc = s.create_script(JS); sc.on('message', on_message); sc.load()
frida.resume(pid); sys.stdin.read()
```

```bash
python dump_payload.py
strings payload_dumped.exe | grep -i 'cGljb0'
```

Le dump est un **PE valide** : ouvrable dans un désassembleur, et ses chaînes contiennent le flag en
base64. Il ne reste qu'à décoder le fragment repéré.

### Voie statique de secours
On a aussi validé une seconde voie, sans debugger : la charge utile est stockée dans la section
`.ATOM`, compressée en **LZMA**. On la décompresse statiquement, puis on concatène les fragments
base64 émis par les constructeurs statiques du payload.

### Pourquoi ça marche
Un packer qui s'efface lui-même ne peut effacer qu'**après** avoir décompressé : il a besoin de
l'image complète pour sauter dedans. Une fenêtre existe donc forcément où l'image est intacte et
copiable. L'effacement d'en-tête n'est pas une protection cryptographique, c'est une gêne pour les
outils : il ne détruit pas la charge utile, il invalide sa description. En hookant l'appel qui
déclenche l'effacement, on prend la copie une instruction trop tôt.

## Pièges
- **Dumper trop tard** : après le transfert, l'en-tête est à zéro et le dump inutilisable. Le hook va
  sur la routine d'effacement, en `onEnter`.
- **Dumper trop court** : sans `SizeOfImage`, on copie une taille arbitraire et on tronque la dernière
  section. La valeur est dans l'en-tête optionnel, pas dans la taille du fichier.
- **`attach` au lieu de `spawn`** : le package est déjà terminé quand on se connecte.
- **Le flag n'est pas en clair** : même un dump parfait donne du base64. Sans l'étape de décodage, on
  conclut à tort que le dump a échoué.
- **Bitness de Frida** : `frida` doit être en 64 bits pour instrumenter un PE x64 ; une installation
  Python 32 bits produit une erreur d'attachement peu explicite.

## Flag

Flag validé sur la plateforme (valeur non conservée).
