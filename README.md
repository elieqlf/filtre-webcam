# filtre-webcam

### Fatine Mourid
fatine.mourid@univ-lyon.2fr

### Calvière Elie
elie.calviere@univ-lyon2.fr

A ajouter dans la note d'intention : 

### Objectif du projet
L’objectif de ce projet est de mettre en pratique les notions de traitement d’images et de vidéos vues en cours à travers une application interactive utilisant une webcam.
Le projet repose sur la détection de visages, l’application de filtres, l’incrustation d’images et l’ajout d’objets interactifs animés.

### Thème choisi : le déguisement
Nous avons choisi le thème du déguisement, inspiré des filtres utilisés sur les réseaux sociaux.

### Fonctionnement de l’application
- Récupération du flux vidéo et détection du visage

Le flux vidéo est récupéré en temps réel à partir de la webcam.
Les visages sont détectés à l’aide d’une cascade de Haar (haarcascade_frontalface_alt.xml)
Chaque visage détecté est représenté par un rectangle, utilisé comme référence pour les incrustations.

- Manipulations sur l’image vidéo
a) Filtre global
Un filtre en niveaux de gris peut être appliqué à l’image entière. Ce filtre est activable/désactivable via le menu interactif.

b) Incrustation d’images
Deux images PNG avec transparence sont incrustées :
Un chapeau positionné au-dessus du visage
un masque positionnés au niveau des yeux
Les images sont redimensionnées dynamiquement en fonction de la taille du visage détecté.

- Incrustation interactive dans le fond
a) Objet animé
Un objet rond est affiché dans le fond de la vidéo.

b) Interaction avec la tête
Lorsque le rond intersecte la zone du visage, sa couleur change en vert.

c) Interaction avec le sourire
Le sourire est détecté à l’aide d’une cascade de Haar dédiée (haarcascade_smile.xml).

Lorsqu’un sourire est détecté :
le rond change de couleur
de nouveaux petits ronds animés apparaissent à l’écran

### Menu interactif
Un menu interactif permet d’activer ou désactiver les fonctionnalités suivantes simultanément :
g : filtre gris
h : chapeau
m : masque
d : rond animé
s : détection du sourire
r : effet miroir
q : quitter l’application
Le menu est affiché directement sur la vidéo.

### Difficultés rencontrées
Plusieurs difficultés ont été rencontrées durant le développement :
- Positionnement précis des incrustations
Ajuster correctement la position du chapeau et des lunettes en fonction de la taille et de la position du visage a nécessité plusieurs essais.
- Détection du sourire
La détection du sourire peut être sensible à l’éclairage et à l’orientation du visage.
Il a fallu ajuster les paramètres de la cascade pour obtenir un résultat satisfaisant.
- Gestion des interactions en temps réel
Faire fonctionner simultanément la détection, les animations et le menu interactif sans ralentissement a demandé une bonne organisation du code.
