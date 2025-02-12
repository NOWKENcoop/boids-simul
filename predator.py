import numpy as np
import random
import pygame as pg


# Fonction pour limiter un vecteur
def limit(vector, max_value):
    magnitude = np.linalg.norm(vector)  # Norme du vecteur
    if magnitude > max_value:  # Si la norme dépasse max_value
        return (vector / magnitude) * max_value  # Normaliser et limiter
    return vector  # Sinon, retourner le vecteur inchangé

def set_mag(vector, magnitude):
    norm = np.linalg.norm(vector)  # Calcul de la norme du vecteur
    if norm == 0:  # Si le vecteur est nul, on retourne un vecteur nul
        return np.zeros_like(vector)
    return (vector / norm) * magnitude  # Normaliser le vecteur et le multiplier par la magnitude souhaitée


class Predator:
    def __init__(self, width, height):
        self.pos = np.array([random.uniform(0, width), random.uniform(0, height)], dtype=np.float64)
        self.velocity = np.random.uniform(2, 6, 2)
        self.acceleration = np.array([0.0, 0.0], dtype=np.float64)
        self.maxSpeed = 30  # Le prédateur est plus rapide que les boids normaux
        self.maxForce = 0.1  # Force maximale appliquée

    def move(self):
        # Variation progressive de direction
        random_turn = np.random.uniform(-0.2, 0.2)  # Angle de rotation aléatoire
        rotation_matrix = np.array([
            [np.cos(random_turn), -np.sin(random_turn)],
            [np.sin(random_turn), np.cos(random_turn)]
        ])
        self.velocity = np.dot(rotation_matrix, self.velocity)  # Modifier la direction de la vélocité

        # Lissage du mouvement avec une cible virtuelle
        target_direction = np.random.uniform(-1, 1, 2)  # Génère une direction cible aléatoire
        target_direction = set_mag(target_direction, self.maxSpeed)  # Ajuster la magnitude de la direction cible
        steering = target_direction - self.velocity  # Calcul de la force de steering
        steering = limit(steering, self.maxForce/20)  # Limiter la force

        # Appliquer la force de steering
        self.acceleration += steering

        # Mettre à jour la vélocité et la position
        self.velocity += self.acceleration
        self.velocity = limit(self.velocity, self.maxSpeed)  # Limiter la vitesse
        self.pos += self.velocity
        self.acceleration *= 0  # Réinitialiser l'accélération

    def edges(self, width, height):
        if self.pos[0] < 0:
            self.pos[0] = width
        elif self.pos[0] > width:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = height
        elif self.pos[1] > height:
            self.pos[1] = 0

    def show(self, screen):
        size = 7  # Taille du prédateur, légèrement plus grand
        pg.draw.circle(screen, (255, 246, 234), self.pos.astype(int), size)  # Cercle rouge pour le prédateur
       
