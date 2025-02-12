import threading
import numpy as np
import pygame as pg
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from boid import Boid
from boid import SpatialGrid
import Constances
from predator import Predator
import math

import sys
from tkinter import messagebox, simpledialog, Tk

flock = []
flock1=[]
width, height = Constances.widthOfSimulation, Constances.heightOfSimulation
is_paused = False

# Fonction pour afficher une boîte de message dans le thread principal
def show_message(message):
    root = Tk()
    root.withdraw()  # Cache la fenêtre principale
    messagebox.showinfo("Info", message)
    root.quit()  # Fermeture de Tkinter sans bloquer

# Fonction pour demander la réinitialisation dans un thread
def reset_in_thread():
    def reset_thread():
        # Demander à l'utilisateur de choisir l'option de réinitialisation
        user_choice = messagebox.askquestion("Réinitialiser", "Souhaitez-vous supprimer tous les boids (aucun boid) ou réinitialiser avec un nombre spécifique de boids ?", icon='question')

        if user_choice == 'yes':  # Remettre tout à zéro
            if flock:
                flock.clear()
            reset_message_timer("Tous les boids ont été supprimés!")
        else:  # Réinitialiser avec un nombre de boids spécifique
            try:
                num_boids = simpledialog.askinteger("Réinitialisation", "Combien de boids voulez-vous créer ?", minvalue=1, maxvalue=10000)
                if num_boids is not None:
                    # Réinitialiser avec le nombre de boids spécifié
                    if flock:
                        flock.clear()
                    for _ in range(num_boids):
                        flock.append(Boid(width, height))
                    reset_message_timer(f"Réinitialisation avec {num_boids} boids!")
            except ValueError:
                reset_message_timer("Veuillez entrer un nombre valide de boids.")

    # Lancer le thread pour exécuter la réinitialisation
    threading.Thread(target=reset_thread, daemon=True).start()

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    pause_button.setText("Resume" if is_paused else "Pause")

def add_boid():
    flock.append(Boid(width, height))
    display_message("Boid ajouté avec succès!")

def display_message(message):
    global message_text
    message_text = message
    pg.time.set_timer(pg.USEREVENT, 3000)  # Le message disparaît après 3 secondes

def check_boid_click(flock, mouse_pos):
    """Vérifie si un boid a été cliqué et le supprime si nécessaire."""
    to_remove = []
    for boid in flock:
        # Calculer la distance entre le curseur et le boid
        distance = np.linalg.norm(boid.pos - mouse_pos)
        if distance < 10:  # Si le boid est cliqué (rayon de 10 pixels)
            to_remove.append(boid)  # Ajouter à la liste des boids à supprimer
    return to_remove

# Initialisation de Pygame
pg.init()
control_panel_height = 100
extra_panel_height = 100  # Hauteur de la nouvelle zone pour les sliders et boutons
screen = pg.display.set_mode((width, height + control_panel_height + extra_panel_height))
pg.display.set_caption("Boids Simulation")

# Barre de contrôle pour les sliders et boutons
control_rect = pg.Rect(0, height, width, control_panel_height)
extra_panel_rect = pg.Rect(0, height + control_panel_height, width, extra_panel_height)

# Initialisation des sliders
alignment_slider = Slider(screen, 50, height + 5, 200, 20, min=0, max=5, step=0.1)
cohesion_slider = Slider(screen, 50, height + 40, 200, 20, min=0, max=5, step=0.1)
separation_slider = Slider(screen, 560, height + 5, 200, 20, min=0, max=5, step=0.1)
speed_rotation_slider = Slider(screen, 560, height + 40, 200, 20, min=0.1, max=5, step=0.1)
speed_slider=Slider(screen,450, height + 77, 200, 20, min=4, max=50, step=4)

# Ajout de labels pour les sliders
alignment_label = TextBox(screen, 285, height + 0, 190, 30, fontSize=20)
cohesion_label = TextBox(screen, 285, height + 35, 190, 30, fontSize=20)
separation_label = TextBox(screen, 800, height + 0, 190, 30, fontSize=20)
speed_rotation_label = TextBox(screen, 800, height + 35, 190, 30, fontSize=20)
speed_label = TextBox(screen, 700, height + 72, 190, 30, fontSize=20)

# Désactiver les labels comme champs de texte
alignment_label.disable()
cohesion_label.disable()
separation_label.disable()
speed_rotation_label.disable()
speed_label.disable()

# Création des boids
for _ in range(500):  # création de 90 boids
    flock.append(Boid(width, height))
# création du prédateur
for _ in range(1): #création de 1 predateur
    flock1.append(Predator(width,height))
predator=flock1[0] if flock1 else None   
# Initialisation de la grille spatiale    
grid = SpatialGrid(Constances.widthOfSimulation, Constances.heightOfSimulation, 20)  # Taille des cellules : 50x50 pixels
 
# Initialisation des boutons
reset_button = Button(screen, 600, height + control_panel_height + 25, 100, 40, text='Reset', onClick=reset_in_thread)
pause_button = Button(screen, 750, height + control_panel_height + 25, 100, 40, text='Pause', onClick=toggle_pause)
add_button = Button(screen, 900, height + control_panel_height + 25, 100, 40, text='Add Boid', onClick=add_boid)

# Charger et redimensionner l'image
image = pg.image.load('xptt.png')  # Remplacez par le chemin de votre image
image = pg.transform.scale(image, (200, 100))  # Ajustez la taille de l'image

# Message texte
message_text = ""

# Dans la boucle principale, gérer l'événement pour effacer le message après 1 seconde
running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            # Vérifier si un boid a été cliqué
            mouse_pos = np.array(pg.mouse.get_pos())
            boids_to_remove = check_boid_click(flock, mouse_pos)
            if boids_to_remove:
                # Supprimer les boids de la liste principale
                for boid in boids_to_remove:
                    flock.remove(boid)
                # Afficher le message
                display_message(f"Boids supprimés. Il en reste {len(flock)}.")

        if event.type == pg.USEREVENT:
            message_text = ""  # Effacer le message après 1 seconde
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:  # Si la touche espace est pressée
                flock1.append(Predator(width, height))  # Ajouter un nouveau prédateur
                print(f"Attention nouveau prédateur ajouté ! Total : {len(flock1)}") 
            if flock1:
                if event.key == pg.K_d:  # Si la touche 'd' est pressée pour supprimer
                    if len(flock1) > 1:  # Vérifier qu'il y a plus d'un prédateur
                        flock1.pop()  # Supprimer le dernier prédateur
                        print(f"Prédateur supprimé. Restants : {len(flock1)}")
                else:
                    print("Impossible de supprimer. Il doit rester au moins un prédateur !")

    # Mise à jour des labels avec les valeurs des sliders
    alignment_label.setText(f"R_Alignment: {alignment_slider.getValue():.1f}")
    cohesion_label.setText(f"R_Cohesion: {cohesion_slider.getValue():.1f}")
    separation_label.setText(f"R_distanciation: {separation_slider.getValue():.1f}")
    speed_rotation_label.setText(f"Speed_rotation: {speed_rotation_slider.getValue():.1f}")
    speed_label.setText(f"speed_V0: {speed_slider.getValue():.1f}")

    # Dessine la simulation
    screen.fill((195, 223, 240 ))
    
    if not is_paused:
        
        # Mise à jour des boids dans la simulation
        grid.clear()  # Réinitialiser la grille avant chaque mise à jour

        # Ajout des boids dans leurs cellules respectives
        for boid in flock:
            grid.add(boid)
        # Calcul des comportements des boids
        for boid in flock:
            # Récupération des voisins via la grille spatiale
            neighbors = grid.get_neighbors(boid)
            #Ecran torique
            boid.edges(width, height)
            for pr in flock1:
                # Mise à jour des forces d'alignement, cohésion et distanciation en fonction des voisins
                boid.update_boids(neighbors,alignment_slider.getValue(),
                    cohesion_slider.getValue(),
                    separation_slider.getValue(),pr)    
                
            # Mise à jour de la position et de la rotation du boid
            boid.update(speed_rotation_slider.getValue(),speed_slider.getValue())
            boid.show(screen)
        # Met à jour le prédateur
        for pr in flock1:
            pr.move()
            pr.edges(width, height)
            pr.show(screen)    
    else:
        for bd in flock:
            bd.show(screen)  # Utilisez la couleur correspondant à leur comportement actuel
        for pr in flock1:
            pr.show(screen)

    # Dessine les barres de contrôle
    pg.draw.rect(screen, (181, 214, 232 ), control_rect)

    # Dessine la nouvelle zone pour les sliders et les boutons
    pg.draw.rect(screen, (144, 136, 161 ), extra_panel_rect)

    # Affiche l'image dans la zone des boutons et sliders
    screen.blit(image, (width // 2 - image.get_width() // 2 - 460, height + control_panel_height + extra_panel_height - image.get_height()))

    # Affiche le message
    if message_text:
        font = pg.font.SysFont(None, 36)
        text = font.render(message_text, True, (0, 0, 0))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    # Met à jour les widgets
    pygame_widgets.update(events)
    pg.display.flip()
pg.quit()
