import pygame
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageEnhance
import numpy as np
import colorsys


# Initialisation de pygame
pygame.init()

# Initialiser le module mixer
pygame.mixer.init()

# Paramètres de la fenêtre
LARGEUR= 800
HAUTEUR = 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("")

# Changer l'icône de la fenêtre
  


# Police de texte
font = pygame.font.Font(None, 36)

# Définition des variables des couleurs à utiliser dans le programme
BLEU = (116, 208, 241)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)

taille=128



# Charger une image et la redimensionner 
imagefond = pygame.image.load("data/fond2.png")
imagefond = pygame.transform.scale(imagefond, (LARGEUR, HAUTEUR))


# Charger les sons
# Charger un effet sonore 

# Charger une musique de fond 

# Si vous voulez jouer une seule fois la musique mettez 1 dans les parenthèses, 2 pour la jouer 2 fois ... et -1 pour jouer en boucle 


# Variables de jeu
input_active = False
scene = "debut"

def quick_sort(arr):
    global indicervb
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2][indicervb]  # Choisir un pivot (ici le milieu de la liste)
        left = [x for x in arr if x[indicervb] < pivot]  # Comparer uniquement la composante R
        middle = [x for x in arr if x[indicervb] == pivot]  # Comparer uniquement la composante R
        right = [x for x in arr if x[indicervb] > pivot]  # Comparer uniquement la composante R

        # Appliquer récursivement Quick Sort aux sous-listes
        return quick_sort(left) + middle + quick_sort(right)

def matricing(source):
    img = Image.open(source)
    img = img.convert("RGB")
    width, height = img.size
    pixelmat = []


    # Parcourir chaque pixel et obtenir sa valeur RGB
    for y in range(height):
        row = []  # Chaque ligne sera une liste de tuples (R, G, B)
        for x in range(width):
            # Obtenir la valeur RGB du pixel (x, y)
            r, g, b = img.getpixel((x, y))
            row.append((r, g, b))  # Ajouter le tuple (R, G, B) à la ligne
        pixelmat.append(row)

    for r in pixelmat :
        print (r)
        

# Fonction pour pixeliser l'image
def pixeliser_image(image_path, pixel_size):
    # Ouvrir l'image
    image = Image.open(image_path)

    # Réduire la taille de l'image
    small_image = image.resize(
        (image.width // pixel_size, image.height // pixel_size),
        resample=Image.NEAREST
    )

    # Redimensionner l'image à sa taille d'origine
    pixelized_image = small_image.resize(image.size, Image.NEAREST)

    return pixelized_image


def choisir_image():
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    file_path = filedialog.askopenfilename(
        title="Sélectionner une image",
        filetypes=[("Fichiers image", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")]
    )
    return file_path

def afficher_texte(texte, x, y, couleur):
    """
    Cette fonction permet d'afficher du texte dans une fenêtre Pygame à partir d'une position donnée (x, y). Si une ligne de texte dépasse
    la largeur de la fenêtre, elle est automatiquement coupée et continuée à la ligne suivante.

    Paramètres :
    -----------
        texte(str) : Le texte à afficher.
        
        x(int) : La position en pixels sur l'axe des abscisses (horizontal) où le texte commence à être affiché.
        
        y(int) : La position en pixels sur l'axe des ordonnées (vertical) où le texte commence à être affiché.
        
        couleur(tuple): Une couleur définie sous forme de tuple (R, G, B) pour la couleur du texte.
    """
    mots = texte.split(' ')
    ligne_actuelle = ''
    y_offset = 0  

    for mot in mots:
        # Vérifie si on peut ajouter le mot à la ligne actuelle
        if font.size(ligne_actuelle + mot)[0] <= LARGEUR - x:
            ligne_actuelle += mot + ' '
        else:
            # Dessine la ligne actuelle et réinitialise pour la nouvelle ligne
            fenetre.blit(font.render(ligne_actuelle.strip(), True, couleur), (x, y + y_offset))
            ligne_actuelle = mot + ' '
            y_offset += font.get_height()  # Augmente l'offset pour la prochaine ligne

    # Dessine la dernière ligne si elle n'est pas vide
    if ligne_actuelle:
        fenetre.blit(font.render(ligne_actuelle.strip(), True, couleur), (x, y + y_offset))


def apply_chrominance_effect(img, hue_shift=-0.1, saturation_factor=0.5, lightness_factor=1.2):
    img = Image.open('result.png')
    img = img.convert("RGB")
    pixels = img.load()

    width, height = img.size
    total_pixels = width * height

    start_time = time.time()  # Début du chrono

    # Boucle pour traiter chaque pixel
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]

            # Convertir la couleur RGB en HSV
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

            # Appliquer les ajustements de teinte et de saturation
            h = (h + hue_shift) % 1.0
            s = max(0, min(1, s * saturation_factor))
            v = max(0, min(1, v * lightness_factor))

            # Convertir de nouveau en RGB
            r, g, b = colorsys.hsv_to_rgb(h, s, v)

            # Réassigner les nouvelles valeurs RGB
            pixels[i, j] = (int(r * 255), int(g * 255), int(b * 255))

    

    # Calculer le temps total
    end_time = time.time()
    duration = end_time - start_time
    print(f"\nTemps total de traitement : {duration:.2f} secondes")
    print(f"Temps estimé par pixel : {duration / total_pixels:.6f} secondes")

    return img



def dessiner_bouton(texte, x, y, largeur, hauteur, couleur1, couleur2, couleurtexte, action=None):
    """
    Cette fonction dessine un bouton interactif dans une fenêtre Pygame. Le bouton change de couleur lorsque la souris le survole,
    et exécute une action si l'utilisateur clique dessus.

    Paramètres :
    -----------
        texte (str) : Le texte à afficher à l'intérieur du bouton.

        x (int) : La position en pixels sur l'axe des abscisses (horizontal) où le bouton commence à être dessiné.

        y (int) : La position en pixels sur l'axe des ordonnées (vertical) où le bouton commence à être dessiné.

        largeur (int) : La largeur souhaitée du bouton. La largeur réelle sera ajustée en fonction de la taille du texte.

        hauteur (int) : La hauteur souhaitée du bouton. La hauteur réelle sera ajustée en fonction de la taille du texte.

        couleur1 (tuple) : La couleur du bouton sous forme de tuple (R, G, B) lorsque la souris n'est pas dessus.

        couleur2 (tuple) : La couleur du bouton sous forme de tuple (R, G, B) lorsque la souris survole le bouton.

        couleurtexte (tuple) : La couleur du texte du bouton sous forme de tuple (R, G, B).

        action (fonction, optionnel) : Une fonction à exécuter lorsque le bouton est cliqué. Par défaut, aucune action n'est exécutée.
    """
    
    # Calculer la taille du texte
    largeur_texte, hauteur_texte = font.size(texte)
    largeur_bouton = max(largeur, largeur_texte + 20)  # Ajouter un peu de marge
    hauteur_bouton = max(hauteur, hauteur_texte + 10)  # Ajouter un peu de marge

    souris = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()

    # Détection de survol de la souris
    if x + largeur_bouton > souris[0] > x and y + hauteur_bouton > souris[1] > y:
        pygame.draw.rect(fenetre, couleur2, (x, y, largeur_bouton, hauteur_bouton))
        if clic[0] == 1 and action is not None:
            time.sleep(0.2)
            action()
    else:
        pygame.draw.rect(fenetre, couleur1, (x, y, largeur_bouton, hauteur_bouton))

    # Dessiner le texte centré dans le bouton
    texte_surface = font.render(texte, True, couleurtexte)
    texte_rect = texte_surface.get_rect(center=(x + largeur_bouton // 2, y + hauteur_bouton // 2))
    fenetre.blit(texte_surface, texte_rect)

#Change de scène lorsqu'on clique sur le bouton de gauche
def choix_gauche():
    """
    Cette fonction permet de changer de scene lorsqu'on a choisi le bouton de gauche. 

    """
    global scene
    
    if scene=="debut":
        scene="choix"
    elif scene=="effet":
        scene="chrominance"
        
#Change de scène lorsqu'on clique sur le bouton de droite
def choix_droite():
    """
    Cette fonction permet de changer de scene lorsqu'on a choisi le bouton de droite. 

    """
    global scene
    
    if scene=="effet":
        scene="vert"

#Change de scène lorsqu'on clique sur le bouton en bas à gauche
def choix_bas_gauche():
    global scene
    
    if scene=="effet":
        scene="vert"

#Change de scène lorsqu'on clique sur le bouton en bas à droite
def choix_bas_droit():
    global scene
    
    if scene=="effet":
        scene="rouge"

   
a=0
indicervb=0
def jeu():
    global scene
    global a
    global indicervb
    prenom_joueur = ""
    fin = False

    # Boucle principale du jeu, tant que le jeu n'est pas fini on continue
    while fin == False:

        # Boucle de gestion des évènements dans la fenêtre 
        for event in pygame.event.get():

            # Si l'utilisateur appuie sur la croix en haut à droite, cela met fin au jeu et ferme pygame 
            if event.type == pygame.QUIT:
                fin = True
                pygame.quit()
                  
        if scene=="debut":
            fenetre.blit(imagefond, (0, 0))
            
            afficher_texte("Bienvenue. Dans ce logiciel vous pourrez appliquer les effets souhaités à une image de votre choix. Veuillez entrer une image",30,100,BLANC)
            dessiner_bouton("Choisir une image",300,300,100,100,GRIS,BLANC,NOIR,choix_gauche)
        
        #Choix de l'image
        elif scene=="choix":
            fenetre.blit(imagefond,(0,0))
            image_path = choisir_image()
            from PIL import Image
            # Open image
            img = Image.open(image_path)

            # Resize smoothly down to 16x16 pixels
            imgSmall = img.resize((taille,taille), resample=Image.Resampling.NEAREST)

            # Scale back up using NEAREST to original size
            result = imgSmall.resize(img.size, Image.Resampling.NEAREST)

            # Save
            result.save('result.png')
            image_choisi = pygame.image.load('result.png')
            image_choisi = pygame.transform.scale(image_choisi, (600, 400))
            scene="effet"
            
        elif scene=="effet":
            #Choix du pixel sorter
            fenetre.blit(imagefond,(0,0))
            fenetre.blit(image_choisi,(100,100))
            afficher_texte("Voici votre image pixelisée. Vous avez plusieurs choix d'effets pixel sorter, choisissez-en un.",50,20,NOIR)
            dessiner_bouton("Appliquer la chrominance",100,500,25,25,GRIS,BLANC,NOIR,choix_gauche)
            dessiner_bouton("Trier par bleus",500,500,25,25,GRIS,BLANC,NOIR,choix_droite)
            dessiner_bouton("Trier par verts",100,540,25,25,GRIS,BLANC,NOIR,choix_bas_gauche)
            dessiner_bouton("Trier par rouges",500,540,25,25,GRIS,BLANC,NOIR,choix_bas_droit)
                        
                              
        #Tri sur la valeur rgb bleu
        elif scene=="bleu":
            while a<1:
                img = Image.open('result.png')
                img = img.convert("RGB")
                width, height = img.size
                pixelmat = []
                # Parcourir chaque pixel et obtenir sa valeur RGB
                for y in range(height):
                    row = []  # Chaque ligne sera une liste de tuples (R, G, B)
                    for x in range(width):
                        # Obtenir la valeur RGB du pixel (x, y)
                        r, g, b = img.getpixel((x, y))
                        row.append((r, g, b))  # Ajouter le tuple (R, G, B) à la ligne
                    pixelmat.append(row)

                img.show()
                RES = []
                indicervb = 2
                for ligne in range(len(pixelmat)) :
                    RES.append(quick_sort(pixelmat[ligne]))


                matric = np.array(RES, dtype=np.uint8)
                imageres = Image.fromarray(matric)
                imageres.show()
                a+=1
                pygame.quit()
         
        #Tri sur la valeur rgb rouge 
        elif scene=="rouge":
            while a<1:
                img = Image.open('result.png')
                img = img.convert("RGB")
                width, height = img.size
                pixelmat = []
                # Parcourir chaque pixel et obtenir sa valeur RGB
                for y in range(height):
                    row = []  # Chaque ligne sera une liste de tuples (R, G, B)
                    for x in range(width):
                        # Obtenir la valeur RGB du pixel (x, y)
                        r, g, b = img.getpixel((x, y))
                        row.append((r, g, b))  # Ajouter le tuple (R, G, B) à la ligne
                    pixelmat.append(row)

                img.show()
                RES = []
                indicervb = 0
                for ligne in range(len(pixelmat)) :
                    RES.append(quick_sort(pixelmat[ligne]))


                matric = np.array(RES, dtype=np.uint8)
                imageres = Image.fromarray(matric)
                imageres.show()
                a+=1
                pygame.quit()
         
        #Tri sur la valeur rgb verte 
        elif scene=="vert":
            while a<1:
                img = Image.open('result.png')
                img = img.convert("RGB")
                width, height = img.size
                pixelmat = []
                # Parcourir chaque pixel et obtenir sa valeur RGB
                for y in range(height):
                    row = []  # Chaque ligne sera une liste de tuples (R, G, B)
                    for x in range(width):
                        # Obtenir la valeur RGB du pixel (x, y)
                        r, g, b = img.getpixel((x, y))
                        row.append((r, g, b))  # Ajouter le tuple (R, G, B) à la ligne
                    pixelmat.append(row)

                img.show()
                RES = []
                indicervb = 1
                for ligne in range(len(pixelmat)) :
                    RES.append(quick_sort(pixelmat[ligne]))


                matric = np.array(RES, dtype=np.uint8)
                imageres = Image.fromarray(matric)
                imageres.show()
                a+=1
                pygame.quit()
        
        #Applique un effet de chrominance
        elif scene=="chrominance":
            while a<1:
                apply_chrominance_effect(img, hue_shift=-0.1, saturation_factor=0.5, lightness_factor=1.2).show()
                a+=1
                pygame.quit()
            
        
        
            
            
            
        
        
        # Mise à jour de l'affichage
        pygame.display.flip()

# Lance le jeu
jeu()
# On attend 5 secondes
time.sleep(5)
# La fenêtre de jeu se ferme
pygame.quit()
