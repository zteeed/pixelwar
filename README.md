# PixelWar Challenge

## TODO

Ce site ([http://pixelwar.h25.io/](http://pixelwar.h25.io/)) est une experience pour le stream de la quarantaine disponible ici.

Vous pouvez changer un pixel de votre choix en envoyant une requete GET sur l'endpoint /setpixel?x=...&y=...&color=...&proof=...

x et y sont compris entre 0 et 99 (le coin en haut a gauche est (0,0))
color est une string hex representant la couleur, par exemple ff9900
proof est une preuve de travail telle que SHA256("h25" + proof) commence par 00000.

Exemple de client (Python3) :

```python
import random, hashlib, requests

def setpixel(x,y,color):
    while True:
        proof = ''.join([random.choice('h25io') for _ in range(30)])
        if hashlib.sha256(('h25'+proof).encode()).hexdigest().startswith('00000'):
            params = {'x':str(x),
                      'y':str(y),
                      'color':color,
                      'proof':proof}
            r = requests.get('http://137.74.47.86/setpixel', params=params)
            print(r.text)

# exemple : setpixel(60,60,'ffffff')
```

## Résolution

On choisit de calculer autant de hash que possible avant de tout envoyer

### Compilation

```bash
g++ sha256.cpp main.cpp -o pixelwar
```

### Lancement

On lance `./pixelwar &` n fois avec n étant le nombre de coeur disponibles pour maximiser les performances. On peut observer le résultat avec:

```bash
tail -f result.txt
```
