import numpy as np
import random
import pygame as pg
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import Constances
import math
import sys

DISTANCE_RADIUS, ALIGNMENT_RADIUS, COHESION_RADIUS = 30, 50, 100

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

class SpatialGrid:
    def __init__(self, width, height, cell_size):
        """
        Initialise la grille spatiale pour diviser l'espace en cellules.
        Chaque cellule contient les boids présents dans cette région de l'espace.

        :paramètre width: largeur totale de l'espace.
        :paramètre height: hauteur totale de l'espace.
        :paramètre cell_size: taille (côté) d'une cellule.
        """
        self.cell_size = cell_size
        self.cols = width // cell_size  # Nombre de colonnes dans la grille
        self.rows = height // cell_size  # Nombre de lignes dans la grille
        # Grille 2D, où chaque cellule est une liste qui contiendra les boids
        self.grid = [[[] for _ in range(self.cols)] for _ in range(self.rows)]

    def add(self, boid):
        """
        Ajoute un boid à la cellule correspondante dans la grille, basée sur sa position.

        :paramètre boid: un objet boid avec une position `boid.pos` (tuple ou liste [x, y]).
        """
        col = int(boid.pos[0] // self.cell_size)  # Calcul de la colonne
        row = int(boid.pos[1] // self.cell_size)  # Calcul de la ligne
        # Ajouter le boid à la cellule correspondante, si elle est dans les limites de la grille
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.grid[row][col].append(boid)

    def get_neighbors(self, boid):
        """
        Récupère tous les boids voisins d'un boid, y compris ceux dans les cellules adjacentes.

        :paramètre boid: le boid pour lequel on cherche les voisins.
        :return: une liste contenant les voisins du boid.
        """
        col = int(boid.pos[0] // self.cell_size)  # Colonne de la grille où se trouve le boid
        row = int(boid.pos[1] // self.cell_size)  # Ligne de la grille où se trouve le boid
        neighbors = []
        # Parcours des cellules environnantes (dans un carré 3x3 autour de la cellule du boid)
        for dr in [-1, 0, 1]:  # Lignes adjacentes
            for dc in [-1, 0, 1]:  # Colonnes adjacentes
                r, c = row + dr, col + dc  # Indices de la cellule voisine
                # Vérifie si la cellule est dans les limites de la grille
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    # Ajoute les boids de cette cellule aux voisins
                    neighbors.extend(self.grid[r][c])
        return neighbors

    def clear(self):
        """
        Réinitialise la grille en vidant toutes les cellules.
        Cette méthode est appelée avant de remplir la grille à nouveau.
        """
        for row in self.grid:
            for cell in row:
                cell.clear()  # Vide chaque cellule


class Boid:
    def __init__(self,width, height):
        self.pos=np.array([random.uniform(0, width), random.uniform(0, height)], dtype=np.float64)  # Utiliser une liste pour créer le tableau
        self.velocity = np.random.uniform(2,6, 2)  # Vecteur de vitesse aléatoire entre -1 et 1
        self.acceleration = np.array([0.0,0.0],dtype=np.float64)
        self.angle_of_view = 180  # Angle de rotation initial
        self.rotation_speed = 2.0 
        self.angle = math.degrees(math.atan2(self.velocity[1], self.velocity[0]))
        self.maxForce = 0.05
        self.maxSpeed = 4
        self.current_behavior = None  # Default behavior
        
    
    #Implémentation d'un écran torique
    def edges(self,width, height):
        if self.pos[0] < 0:
            self.pos[0] = width
        elif self.pos[0] > width:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = height
        elif self.pos[1] > height:
            self.pos[1] = 0
    
    #Rotation des boids pour suivre un boid ou des boids
    def rotate_towards(self, target_pos):
        # Calcul du vecteur directionnel vers la cible
        target_vector = target_pos - self.pos
        
        # Calcul de l'angle de la cible (direction du mouvement cible)
        target_angle = np.degrees(np.arctan2(target_vector[1], target_vector[0])) % 360
        self.angle = target_angle
       
            
    def vision_field(self, other):
        """
        Vérifie si le boid B est dans le champ de vision du boid A.
        
        :param pos_a: Position du boid A (numpy array ou liste [x, y]).
        :param dir_a: Direction de vision du boid A (vecteur unitaire numpy array ou liste [dx, dy]).
        :param angle_a: Angle de vision de A en radians.
        :param pos_b: Position du boid B (numpy array ou liste [x, y]).
        :return: True si B est dans le champ de vision de A, sinon False.
        """
        # Vecteur entre les deux boids
        vec_ab = np.array(other.pos) - np.array(self.pos)
        
        # Normaliser le vecteur relatif
        vec_ab_unit = vec_ab / np.linalg.norm(vec_ab)
        # Normaliser le vecteur vitesse du boid en cours
        vec_velocity = self.velocity / np.linalg.norm(self.velocity)
        # Calcul du cosinus de l'angle
        cos_angle = np.dot(vec_velocity, vec_ab_unit)
        
        # Comparer avec le seuil cosinus(angle_a / 2)
        return cos_angle >= np.cos(np.radians(self.angle_of_view / 2))

    
    def distance (self, boids):
        steering=np.array([0.0,0.0])
        total=0
        for other in boids:
            distance = np.linalg.norm(self.pos - other.pos)
            if other != self and distance < DISTANCE_RADIUS :
                diff = self.pos - other.pos
                diff /= distance
                steering+= diff
                total+=1
        if total >0:
            steering /=total
            steering = set_mag(steering, self.maxSpeed)
            steering -= self.velocity
            steering = limit(steering, self.maxForce)
        return steering
    
    def align(self, boids):
        steering = np.array([0.0, 0.0])
        total = 0
        avg_pos = np.array([0.0, 0.0])
        for other in boids:
            distance = np.linalg.norm(self.pos - other.pos)
            if other != self and distance < ALIGNMENT_RADIUS and self.vision_field(other) and distance :
                steering += other.velocity
                avg_pos += other.pos
                total += 1
        if total > 0:
            avg_pos /= total
            self.rotate_towards(avg_pos)  # Rotation vers la moyenne des voisins visibles
            steering /= total
            steering = set_mag(steering, self.maxSpeed)
            steering -= self.velocity
            steering = limit(steering, self.maxForce)
        return steering

    
    def cohesion (self, boids):
        steering=np.array([0.0,0.0])
        total=0
        for other in boids:
            distance = np.linalg.norm(self.pos - other.pos)
            if other != self and distance < COHESION_RADIUS and self.vision_field(other):
                steering+= other.pos
                total+=1
        if total >0:
            steering /=total
            self.rotate_towards(steering)  # Rotation vers la moyenne des voisins visibles
            steering -= self.pos
            steering = set_mag(steering, self.maxSpeed)
            steering -= self.velocity
            steering = limit(steering, self.maxForce)
        return steering
    
    def avoid_predator(self, predator, safe_distance):
        # Calcul de la distance au prédateur
        distance = np.linalg.norm(self.pos - predator.pos)
        if distance < safe_distance:  # Si le prédateur est proche
            # Calcul de la force d'évitement (inversement proportionnelle à la distance)
            force = self.pos - predator.pos
            force = set_mag(force, self.maxSpeed)  # Ajuster la magnitude
            steering = force - self.velocity  # Calcul du steering
            return limit(steering, self.maxForce)  # Limiter la force
        return np.zeros(2)  # Pas de force si hors de portée
    
    def update_boids(self, boids,alignement_value,cohesion_value, distance_value,predator):
        alignment = self.align(boids)
        coh = self.cohesion(boids)
        distanciaton = self.distance(boids)
        # Force d'évitement du prédateur
        if predator:
            avoidance_force = self.avoid_predator(predator, 100)


        # Pondération des forces
        alignment *= alignement_value
        coh *= cohesion_value
        distanciaton *= distance_value
        
        dominant_behavior = max(
            [(alignment, "alignment"), (coh, "cohesion"), (distanciaton, "distance")],
            key=lambda x: np.linalg.norm(x[0])
        )
        self.current_behavior = dominant_behavior[1]

        # Applique les forces
        self.acceleration += distanciaton
        self.acceleration += alignment
        self.acceleration += coh
        if predator:
            self.acceleration += avoidance_force *100
            
    
    def update(self, rotation_slider_value,speed_slider_value):
        # Modification de la vitesse de rotation
        self.rotation_speed = rotation_slider_value
        self.maxSpeed=speed_slider_value
        

        # Calculer la direction finale basée sur l'angle
        angle_radians = np.radians(self.angle)
        direction = np.array([np.cos(angle_radians), np.sin(angle_radians)])

        # Appliquer un effet directionnel à la vélocité sans écraser les forces comportementales
        self.velocity += 2 * direction  # Ajustez le facteur 0.1 pour un effet plus ou moins prononcé

        # Appliquer les forces comportementales et limiter la vitesse
        self.velocity += self.acceleration
        self.velocity = limit(self.velocity, self.maxSpeed)
        self.pos += self.velocity
        self.acceleration *= 0

        
    def show(self, screen):
        size = 15  # Taille du boid
        
        # Définir la couleur selon le comportement dominant
        if self.current_behavior == "alignment":
            color = (230, 117, 97)  # Rouge
        elif self.current_behavior == "cohesion":
            color = (45, 116, 156)  # Bleu
        elif self.current_behavior == "distance":
            color = (0, 115, 9)  # Vert
        else:
            color = (255, 255, 255)  # Blanc
            
        vision_radius = 100  # Rayon du champ de vision (distance des rayons)
        
        # Calcul de l'angle de vision en radians
        left_angle = np.radians(self.angle - self.angle_of_view / 2)
        right_angle = np.radians(self.angle + self.angle_of_view / 2)

        # Dessiner le boid (triangle)
        angle_radians = np.radians(self.angle)
        top = self.pos + np.array([np.cos(angle_radians), np.sin(angle_radians)]) * size
        left = self.pos + np.array([np.cos(angle_radians + 2.5), np.sin(angle_radians + 2.5)]) * size * 0.5
        right = self.pos + np.array([np.cos(angle_radians - 2.5), np.sin(angle_radians - 2.5)]) * size * 0.5

        pg.draw.polygon(screen, color, [top, left, right])
        
