# Boids Simulation

## Description

Cette simulation implémente le modèle des **Boids** pour la simulation du comportement d'un groupe d'oiseaux ou d'autres agents mobiles dans un environnement en 2D. Elle inclut un système de prédateurs et d'algorithmes de comportements pour la séparation, la cohésion et l'alignement des boids. Cette version utilise la bibliothèque `Pygame` pour la gestion de l'interface graphique et des événements en temps réel.

Les agents (boids) interagissent entre eux selon trois principes :
- **Cohésion** : Les boids se déplacent vers le centre de masse de leurs voisins.
- **Séparation** : Les boids évitent la collision avec leurs voisins.
- **Alignement** : Les boids s'alignent avec les directions de leurs voisins proches.

Les utilisateurs peuvent interagir avec la simulation à l'aide de boutons et de sliders pour ajuster les paramètres en temps réel.

## Fonctionnalités

- **Contrôles interactifs** : Ajustez les paramètres des boids avec des sliders.
- **Ajout/Suppression de boids** : Ajoutez des boids ou réinitialisez la simulation.
- **Prédateurs** : Ajoutez des prédateurs qui chassent les boids.
- **Message dynamique** : Des messages sont affichés pour informer des actions (par exemple, suppression de boids).
- **Grille spatiale** : Optimisation des comportements des boids en utilisant une grille spatiale pour les recherches de voisins.

## Prérequis

- Python 3.6+
- Bibliothèque `pygame`
- Bibliothèque `pygame_widgets`
- Bibliothèque `numpy`

## Installation

1. Clonez ce dépôt ou téléchargez les fichiers.
2. Installez les dépendances nécessaires avec `pip` :
    ```bash
    pip install pygame pygame_widgets numpy
    ```

## Utilisation

1. Exécutez le script principal `main.py` :
    ```bash
    python boids_simulation.py
    ```
2. Vous serez accueilli avec une fenêtre de simulation où vous pourrez :
    - Utiliser les **sliders** pour ajuster les comportements de vos boids (alignement, cohésion, séparation, vitesse, etc.).
    - Cliquer sur les **boids** pour les supprimer.
    - Ajouter ou supprimer des **prédateurs** en appuyant sur la barre d'espace ou la touche 'd'.
    - Appuyer sur **Pause** pour suspendre ou reprendre la simulation.
    - **Réinitialiser** les boids via un bouton et choisir un nombre de boids à ajouter.

## Détails Techniques

- **Boids** : Les boids sont des agents mobiles qui suivent les trois règles mentionnées ci-dessus. Chaque boid est un objet contenant sa position, sa vitesse, et ses forces résultant des comportements.
- **Prédateurs** : Les prédateurs sont des agents qui se déplacent de manière indépendante et interagissent avec les boids en les chassant.
- **Grille Spatiale** : Pour améliorer l'efficacité des calculs de voisins, une grille spatiale est utilisée pour diviser l'espace en cellules.

### Classes principales

- `Boid` : Représente un boid dans la simulation. Il possède des méthodes pour gérer les comportements, la mise à jour de la position, et l'affichage.
- `Predator` : Représente un prédateur qui chasse les boids.
- `SpatialGrid` : Permet de diviser l'espace en une grille pour optimiser la recherche de voisins.

## Capture d'écran

![Capture d'écran de la simulation](https://github.com/NOWKENcoop/boids-simul/blob/master/xptt.png)

## Auteurs

- **Nom de l'auteur** - *Initials* - [nowken](https://github.com/NOWKENcoop)

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
