import pygame
import time
import ast
import math
import os

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('NOT much of a GAME')
clock = pygame.time.Clock()

# ===================== Fichiers de sauvegarde =====================

def readgametoplayerpos():
    """Ouvre le txt contenant la position de la caméra."""
    save_path = os.path.join(os.path.dirname(__file__), "Save", "cvaluessaves.txt")
    with open(save_path, 'r') as f:
        save = f.read().replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "").replace(" ", "").split(",")
    return save

def savegametoplayerpos(contenu):
    """Sauvegarde la position de la caméra dans un fichier txt."""
    save_path = os.path.join(os.path.dirname(__file__), "Save", "cvaluessaves.txt")
    with open(save_path, 'w') as f:
        f.write(str(contenu))

def readgametoressources(line_number):
    """Ouvre le txt contenant les ressources."""
    save_path = os.path.join(os.path.dirname(__file__), "Save", "ressources.txt")
    with open(save_path, 'r') as f:
        lines = f.readlines()
        data_dict = ast.literal_eval(lines[line_number - 1].strip())
    return data_dict

def savegametoressources(contenu):
    """Sauvegarde les ressources dans un fichier txt."""
    save_path = os.path.join(os.path.dirname(__file__), "Save", "ressources.txt")
    with open(save_path, 'r') as f:
        lines = f.readlines()
    
    for i in range(len(contenu)):
        lines[i] = str(contenu[i]) + '\n'
    
    with open(save_path, 'w') as file:
        file.writelines(lines)

def extract_data_from_file(savefile, line_number, key):
    """Extrait une donnée spécifique d'une ligne du fichier."""
    with open(savefile, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if line_number < 1 or line_number > len(lines):
            return None
        data_dict = ast.literal_eval(lines[line_number - 1].strip())
        return data_dict.get(key)

def pre_render_map(savefile):
    """Prérend la carte pour des performances optimisées."""
    map_surface = pygame.Surface((MAP_SIZE * TILE_SIZE, MAP_SIZE * TILE_SIZE))
    for i in range(MAP_SIZE * MAP_SIZE):
        tile_type = extract_data_from_file(savefile, i + 1, 'type')
        if tile_type is None:
            break
        if tile_type in tile_images:
            x = (i % MAP_SIZE) * TILE_SIZE
            y = (i // MAP_SIZE) * TILE_SIZE
            map_surface.blit(tile_images[tile_type], (x, y))
    return map_surface

# ===================== Variables globales =====================

savefile = os.path.join(os.path.dirname(__file__), "Save", "game_info.txt")
PLAYER_POSX, PLAYER_POSY, PLAYER_SPEED = int(readgametoplayerpos()[0]), int(readgametoplayerpos()[1]), 1
RESSOURCE_TOT = {**readgametoressources(1), **readgametoressources(2), **readgametoressources(3), **readgametoressources(4)}

def update_ressources(RESSOURCE_TOT):
    """Met à jour les ressources totales."""
    RESSOURCES1 = {'Bois': RESSOURCE_TOT['Bois'], 'Fer': RESSOURCE_TOT['Fer'], 'Pierre': RESSOURCE_TOT['Pierre']}
    RESSOURCES2 = {'Planches': RESSOURCE_TOT['Planches'], 'Lingots De Fer': RESSOURCE_TOT['Lingots De Fer']}
    RESSOURCES3 = {'Viande': RESSOURCE_TOT['Viande'], 'Boissons': RESSOURCE_TOT['Boissons']}
    RESSOURCES4 = {'Vetements Hiver': RESSOURCE_TOT['Vetements Hiver'], 'Outils En Cuivre': RESSOURCE_TOT['Outils En Cuivre']}
    return RESSOURCES1, RESSOURCES2, RESSOURCES3, RESSOURCES4

RESSOURCES1, RESSOURCES2, RESSOURCES3, RESSOURCES4 = update_ressources(RESSOURCE_TOT)

# Variables de jeu
FONT = pygame.font.Font(None, 36)
FONT2 = pygame.font.Font(None, 24)
FPS = 240
TIME1, TIME2, temp = 0, 0, 0
TILE_SIZE = 90
MAP_SIZE = 64
OLDMOUSE_X, OLDMOUSE_Y = -1, -1
key_type = ['ceuilleur',
            'herbe',
            'arbre', 
            'baies',
            'pierre',
            'fer',
            'chemin0',
            'chemin1',
            'chemin2',
            'chemin3',
            'maison1',
            'maison2',
            'maison3',
            ]


# Chargement des images
img_maison1 = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "maison", "maison1.png")).convert(), 0, 0.075)
img_maison2 = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "maison", "maison2.png")).convert(), 0, 0.075)
img_maison3 = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "maison", "maison3.png")).convert(), 0, 0.075)

img_ceuilleur = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "maison", "ceuilleur.png")).convert(), 0, 0.075)

img_chemin0 = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "chemin", "chemin.png")).convert(), 0, 0.075)
img_chemin90, img_chemin180, img_chemin270 = pygame.transform.rotate(img_chemin0, 90), pygame.transform.rotate(img_chemin0, 180), pygame.transform.rotate(img_chemin0, 270)

img_herbe = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "chemin", "herbe.png")).convert(), 0, 0.075)
img_arbre = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "arbres", "arbre.png")).convert(), 0, 0.075)
img_baies = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "arbres", "baies.png")).convert(), 0, 0.075)
img_pierre = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "arbres", "pierre.png")).convert(), 0, 0.075)
img_fer = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "arbres", "fer.png")).convert(), 0, 0.075)
# Image de menu
img_menu_rien = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "icones", "rien.png")).convert(), 0, 0.04)

img_menu_logement = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "icones", "logements.png")).convert(), 0, 0.04)
img_menu_maison1 = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "icones", "maison1.png")).convert(), 0, 0.04)
img_menu_maison2 = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "icones", "maison2.png")).convert(), 0, 0.04)
img_menu_maison3 = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "icones", "maison3.png")).convert(), 0, 0.04)

img_menu_nourriture = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "icones", "nourriture.png")).convert(), 0, 0.04)
img_menu_ceuilleur = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "icones", "ceuilleur.png")).convert(), 0, 0.04)

img_menu_production = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "icones", "production.png")).convert(), 0, 0.04)

img_menu_combat = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "icones", "combat.png")).convert(), 0, 0.04)

img_menu_commerce = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "icones", "commerce.png")).convert(), 0, 0.04)
img_menu_chemin = pygame.transform.rotozoom(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "icones", "chemin.png")).convert(), 0, 0.04)

tile_images = {
    "chemin0": img_chemin0 ,
    "chemin1": img_chemin90,
    "chemin2": img_chemin180,
    "chemin3": img_chemin270,
    "herbe": img_herbe,
    "arbre": img_arbre,
    "baies": img_baies,
    "pierre": img_pierre,
    "fer": img_fer,
    "maison1": img_maison1,
    "maison2": img_maison2,
    "maison3": img_maison3,
    "ceuilleur": img_ceuilleur
    }
tile_info = {
    "herbe": "{'type': 'herbe'}",
    "arbre": "{'type': 'arbre'}",
    "baies": "{'type': 'baies'}",
    "pierre": "{'type': 'pierre'}",
    "fer": "{'type': 'fer'}",
    "chemin0": "{'type': 'chemin0'}",
    "chemin1": "{'type': 'chemin1'}",
    "chemin2": "{'type': 'chemin2'}",
    "chemin3": "{'type': 'chemin3'}",
    "maison1": "{'type': 'maison1', 'villager1': 'None', 'villager2': 'None', 'ressource1': {'None': '0'}, 'ressource2': {'None': 0} }",
    "maison2": "{'type': 'maison2', 'villager1': 'None', 'villager2': 'None', 'ressource1': {'None': '0'}, 'ressource2': {'None': 0} }",
    "maison3": "{'type': 'maison3', 'villager1': 'None', 'villager2': 'None', 'ressource1': {'None': '0'}, 'ressource2': {'None': 0} }",
    "ceuilleur": "{'type': 'ceuilleur', 'ressource1': {'None': '0'}, 'villager1': 'None'}"
    }

selected_button_0_1 = [0, 0]

# ===================== Fonctions de rendu =====================

def Render_Text(what, color, where, FONT):
    """Affiche du texte à l'écran."""
    text = FONT.render(what, 1, pygame.Color(color))
    screen.blit(text, where)

def Render_FPS(TIME, temp):
    """Affiche le nombre d'images par seconde."""
    current_time = time.time()
    if current_time - TIME > 1:
        temp = str(int(clock.get_fps()))
        TIME = current_time
    Render_Text(f"FPS: {temp}", (80, 174, 0), (1800, 20), FONT)
    return TIME, temp

def Render_map_fast(PLAYER_POSX, PLAYER_POSY, map_surface):
    """Affiche la carte prérendue."""
    screen.blit(map_surface, (PLAYER_POSX, PLAYER_POSY))

key_type = ['ceuilleur',
            'herbe',
            'arbre', 
            'baies',
            'pierre',
            'fer',
            'chemin0',
            'chemin1',
            'chemin2',
            'chemin3',
            'maison1',
            'maison2',
            'maison3',
            ]


def afficher_valeurs(savefile, key_type, FONT, mouse_x, mouse_y):
    """Affiche les informations de la case cliquée."""
    line_number = get_tile_from_mouse(mouse_x, mouse_y, 'line_number')
    # Ceuilleur
    if extract_data_from_file(savefile, line_number, 'type') == key_type[0]:
        key = ['type', 'ressource1', 'villager1']
        jump = 0
        for e in key:
            Render_Text(f"{e} : {extract_data_from_file(savefile, line_number, e)}", (120, 120, 120), (1440, 180 + jump), FONT)
            jump += 30
    # Herbe, arbre, baies, pierre, fer, chemins
    elif extract_data_from_file(savefile, line_number, 'type') in key_type[1:9]:
        Render_Text(f"type : {extract_data_from_file(savefile, line_number, 'type')}", (120, 120, 120), (1440, 180), FONT)

    # Maisons
    elif extract_data_from_file(savefile, line_number, 'type') in key_type[10:12]:
        key = ['type', 'villager1', 'villager2', 'ressource1', 'ressource2']
        jump = 0
        for e in key:
            Render_Text(f"{e} : {extract_data_from_file(savefile, line_number, e)}", (120, 120, 120), (1440, 180 + jump), FONT)
            jump += 30

def update(keys, PLAYER_POSX, PLAYER_POSY, PLAYER_SPEED):
    """Met à jour la position du joueur sur la carte avec limites de déplacement et calcule la vitesse."""
    movement_x = keys[pygame.K_q] - keys[pygame.K_d]
    movement_y = keys[pygame.K_z] - keys[pygame.K_s]
    initial_posx, initial_posy = PLAYER_POSX, PLAYER_POSY
    k = PLAYER_SPEED
    if keys[pygame.K_LSHIFT]:
        PLAYER_SPEED *= 2

    if movement_x != 0 and movement_y == 0:
        PLAYER_POSX += int(movement_x * PLAYER_SPEED)
    if movement_y != 0 and movement_x == 0:
        PLAYER_POSY += int(movement_y * PLAYER_SPEED)
    if movement_y != 0 and movement_x != 0:
        PLAYER_POSX += movement_x * PLAYER_SPEED * 0.71
        PLAYER_POSY += movement_y * PLAYER_SPEED * 0.71
    
    PLAYER_SPEED = k

    # Limite de déplacement de la caméra
    PLAYER_POSX = min(15, max(PLAYER_POSX, -MAP_SIZE * TILE_SIZE + 1405))
    PLAYER_POSY = min(165, max(PLAYER_POSY, -MAP_SIZE * TILE_SIZE + 1065))

    # Calcul de la vitesse du joueur
    distance_x = PLAYER_POSX - initial_posx
    distance_y = PLAYER_POSY - initial_posy
    player_velocity = (distance_x**2 + distance_y**2)**0.5

    return int(PLAYER_POSX), int(PLAYER_POSY), player_velocity

def get_tile_from_mouse(mouse_x, mouse_y, type):
    """Récupère la tuile en fonction des coordonnées de la souris."""
    world_x = mouse_x + (-int(PLAYER_POSX))
    world_y = mouse_y + (-int(PLAYER_POSY))
    tile_x = world_x // TILE_SIZE
    tile_y = world_y // TILE_SIZE
    if type == 'coordonate':
        return tile_x, tile_y
    elif type == 'line_number':
        return tile_x + (tile_y) * MAP_SIZE + 1

def draw_button_menu(screen):
    global selected_button_0_1, img_menu_logement, img_menu_nourriture, img_menu_production, img_menu_combat, img_menu_commerce, img_menu_maison1, img_menu_maison2, img_menu_maison3, img_menu_ceuilleur, img_menu_rien, img_menu_chemin
    positions_button_base = [(1440, 1005), (1510, 1005), (1580, 1005), (1650, 1005), (1720, 1005)]
    positions_button_menu = [(1440, 940), (1510, 940), (1580, 940), (1650, 940), (1720, 940)]
    img_button_base = (img_menu_logement, img_menu_nourriture, img_menu_production, img_menu_combat, img_menu_commerce)

    for i in range(5):
        screen.blit(img_button_base[i], positions_button_base[i])
    
    if selected_button_0_1[0] == 0 and selected_button_0_1[1] != 0:
        button = (img_menu_maison1, img_menu_maison2, img_menu_maison3, img_menu_rien, img_menu_rien)
        for i in range(5):
            screen.blit(button[i], positions_button_menu[i])
            pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(positions_button_menu[selected_button_0_1[1] - 1][0] - 5, positions_button_menu[selected_button_0_1[1] - 1][1] - 5, 55, 55), 5)
    if selected_button_0_1[0] == 1 and selected_button_0_1[1] != 0:
        button = (img_menu_ceuilleur, img_menu_rien, img_menu_rien, img_menu_rien, img_menu_rien)
        for i in range(5):
            screen.blit(button[i], positions_button_menu[i])
            pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(positions_button_menu[selected_button_0_1[1] - 1][0] - 5, positions_button_menu[selected_button_0_1[1] - 1][1] - 5, 55, 55), 5)
    if selected_button_0_1[0] == 2 and selected_button_0_1[1] != 0:
        button = (img_menu_rien, img_menu_rien, img_menu_rien, img_menu_rien, img_menu_rien)
        for i in range(5):
            screen.blit(button[i], positions_button_menu[i])
            pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(positions_button_menu[selected_button_0_1[1] - 1][0] - 5, positions_button_menu[selected_button_0_1[1] - 1][1] - 5, 55, 55), 5)
    if selected_button_0_1[0] == 3 and selected_button_0_1[1] != 0:
        button = (img_menu_rien, img_menu_rien, img_menu_rien, img_menu_rien, img_menu_rien)
        for i in range(5):
            screen.blit(button[i], positions_button_menu[i])
            pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(positions_button_menu[selected_button_0_1[1] - 1][0] - 5, positions_button_menu[selected_button_0_1[1] - 1][1] - 5, 55, 55), 5)
    if selected_button_0_1[0] == 4 and selected_button_0_1[1] != 0:
        button = (img_menu_rien, img_menu_rien, img_menu_rien, img_menu_rien, img_menu_rien)
        for i in range(5):
            screen.blit(button[i], positions_button_menu[i])
            pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(positions_button_menu[selected_button_0_1[1] - 1][0] - 5, positions_button_menu[selected_button_0_1[1] - 1][1] - 5, 55, 55), 5)
    
    if selected_button_0_1[1] == 0:
        pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(positions_button_base[selected_button_0_1[0]][0] - 5, positions_button_base[selected_button_0_1[0]][1] - 5, 55, 55), 5)

def change_data_from_file(savefile, line, new_data):
    """Extrait une donnée spécifique d'une ligne du fichier et la remplace par new_data."""
    with open(savefile, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    if line < len(lines):
        lines[line] = new_data + '\n'
    
    with open(savefile, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def draw_interface_info_ressources(screen):

    # Dessine les surfaces en marron
    pygame.draw.rect(screen, (82, 58, 42), pygame.Rect(0, 0, 1920, 165))
    pygame.draw.rect(screen, (82, 58, 42), pygame.Rect(1410, 0, 1920, 1080))
    pygame.draw.rect(screen, (82, 58, 42), pygame.Rect(0, 1070, 1920, 1080))
    pygame.draw.rect(screen, (82, 58, 42), pygame.Rect(0, 0, 10, 1080))

    # Dessine les contours des surfaces en marron
    pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(10, 10, 1400, 140), 5)
    pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(1420, 10, 490, 140), 5)
    pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(10, 160, 1400, 910), 5)
    pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(1420, 160, 490, 910), 5)

    # Ecrit les textes d'info tiers en haut à droite
    Render_Text(f"POS {str(int(-PLAYER_POSX + 15))} ; {str(int(-PLAYER_POSY + 165))}", (120, 120, 120), (1600, 50), FONT)
    Render_Text(f"MENU {str(selected_button_0_1)}", (120, 120, 120), (1600, 80), FONT)
    Render_Text(f"FPS {int(clock.get_fps())} ; SPEED {str(math.floor(player_velocity*10)/10)}", (240, 120, 80), (1600, 20), FONT)

    # Ecrit les ressources en haut à gauche
    Render_Text(f"BOIS : {RESSOURCES1['Bois']} ; FER : {RESSOURCES1['Fer']} ; PIERRE : {RESSOURCES1['Pierre']}", (120, 120, 120), (20, 20), FONT)
    Render_Text(f"PLANCHES : {RESSOURCES2['Planches']} ; LINGOTS DE FER : {RESSOURCES2['Lingots De Fer']}", (120, 120, 120), (20, 50), FONT)
    Render_Text(f"VIANDE : {RESSOURCES3['Viande']} ; BOISSONS : {RESSOURCES3['Boissons']}", (120, 120, 120), (20, 80), FONT)
    Render_Text(f"VETEMENTS HIVER : {RESSOURCES4['Vetements Hiver']} ; OUTILS EN CUIVRE : {RESSOURCES4['Outils En Cuivre']}", (120, 120, 120), (20, 110), FONT)

    # Ecrit des info de touches en bas a gauche
    Render_Text(f"Recharger la map ( 5s ) : Ctrl + R", (0, 0, 0), (20, 1040), FONT2)
# ===================== Boucle de jeu =====================

running = True
variable_info_tuile = 0
affiche_presset = False
cequejaffiche = None
cequejepose = None
player_velocity = 0
rotate, rotation = False, 1
pygame.event.set_grab(True)  # Bloque la souris dans la fenêtre
map_surface = None
updated = []
map_surface = pre_render_map(savefile)
NotEngoutRessources, PeuxPasPlacerIci = False, False
while running:
    
    # ===================== Gestion graphique =====================
    
    screen.fill((0, 0, 0))
    Render_map_fast(PLAYER_POSX, PLAYER_POSY, map_surface)
    delta_time = clock.tick(FPS) / 50
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    


    # Deplacements camera
    if keys[pygame.K_z] or keys[pygame.K_s] or keys[pygame.K_q] or keys[pygame.K_d]:
        variable_info_tuile = 0
        PLAYER_POSX, PLAYER_POSY, player_velocity = update(keys, PLAYER_POSX, PLAYER_POSY, PLAYER_SPEED)
    if affiche_presset:
        tile_coords = get_tile_from_mouse(mouse_x, mouse_y, 'coordonate')
        tile_x, tile_y = tile_coords[0] * TILE_SIZE, tile_coords[1] * TILE_SIZE
        screen.blit(cequejaffiche, (max(0, min(tile_x, MAP_SIZE * TILE_SIZE + 1405)) + int(PLAYER_POSX), max(0, int(PLAYER_POSY) + min(tile_y, MAP_SIZE * TILE_SIZE + 1060))))
        if keys[pygame.K_e]:
            if 15 < mouse_x < 1405 and 165 < mouse_y < 1065:
                OLDMOUSE_X, OLDMOUSE_Y = mouse_x, mouse_y
                if key_type == 1:
                    if ressource_construire:
                        for e in range(len(ressource_construire)):
                            RESSOURCE_TOT[ressource_construire[e][0]] -= ressource_construire[e][1]
                        RESSOURCES1, RESSOURCES2, RESSOURCES3, RESSOURCES4 = update_ressources(RESSOURCE_TOT)
                    line_number = tile_coords[1] * MAP_SIZE + tile_coords[0]
                    change_data_from_file(savefile, line_number, f"{cequejepose}")
                    new_position = (max(0, min(tile_x, MAP_SIZE * TILE_SIZE + 1405)) + int(PLAYER_POSX), max(0, int(PLAYER_POSY) + min(tile_y, MAP_SIZE * TILE_SIZE + 1060)))
                    if (cequejaffiche, new_position) not in updated:
                        updated.append((cequejaffiche, (new_position, PLAYER_POSX, PLAYER_POSY)))
            
    for e in updated:
        image, position = e
        screen_x, screen_y, playerx, playery = position[0][0], position[0][1], position[1], position[2]
        screen.blit(image, (screen_x -(playerx - int(PLAYER_POSX)), screen_y -(playery - int(PLAYER_POSY))))
    
    draw_interface_info_ressources(screen)
    
    # Quitter le jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (keys[pygame.K_LALT] and keys[pygame.K_a]):
            savegametoplayerpos((int(PLAYER_POSX), int(PLAYER_POSY)))
            savegametoressources([str(RESSOURCES1), str(RESSOURCES2), str(RESSOURCES3), str(RESSOURCES4)])
            running = False
        if (keys[pygame.K_LCTRL] and keys[pygame.K_r]):
            map_surface = pre_render_map(savefile)
            updated = []
        elif event.type == pygame.KEYDOWN:
            NotEngoutRessources, PeuxPasPlacerIci = False, False
            current_time = time.time()
            if current_time - TIME1 > 0.05:
                if event.key == pygame.K_LEFT:
                    rotate = False
                    if selected_button_0_1[0] > 0 and selected_button_0_1[1] == 0:
                        selected_button_0_1[0] -= 1
                    elif selected_button_0_1[1] > 0 and selected_button_0_1[1] != 0:
                        selected_button_0_1[1] -= 1
                elif event.key == pygame.K_RIGHT:
                    rotate = False
                    if selected_button_0_1[0] < 4 and selected_button_0_1[1] == 0:
                        selected_button_0_1[0] += 1
                    elif selected_button_0_1[1] < 5 and selected_button_0_1[1] != 0:
                        selected_button_0_1[1] += 1
                elif event.key == pygame.K_SPACE:
                    if selected_button_0_1[1] != 0:
                        if selected_button_0_1 == [0, 1]:
                            if RESSOURCES1['Bois'] > 20 and RESSOURCES2['Planches'] > 50 and RESSOURCES1['Pierre'] > 10:
                                ressource_construire = [("Bois", 20), ("Planches", 50), ("Pierre", 10)]
                                affiche_presset = True
                                cequejaffiche = tile_images['maison1']
                                cequejepose = tile_info['maison1']
                            else:
                                NotEngoutRessources = True
                        elif selected_button_0_1 == [0, 2]:
                            if RESSOURCES1['Bois'] > 80 and RESSOURCES2['Planches'] > 50 and RESSOURCES1['Pierre'] > 100:
                                ressource_construire = [("Bois", 80), ("Planches", 50), ("Pierre", 100)]
                                affiche_presset = True
                                cequejaffiche = tile_images['maison2']
                                cequejepose = tile_info['maison2']
                            else:
                                NotEngoutRessources = True
                        elif selected_button_0_1 == [0, 3]:
                            if RESSOURCES1['Bois'] > 120 and RESSOURCES2['Planches'] > 200 and RESSOURCES1['Pierre'] > 150:
                                ressource_construire = [("Bois", 120), ("Planches", 200), ("Pierre", 150)]
                                affiche_presset = True
                                cequejaffiche = tile_images['maison3']
                                cequejepose = tile_info['maison3']
                            else:
                                NotEngoutRessources = True
                        elif selected_button_0_1 == [1, 1]:
                            if RESSOURCES1['Bois'] > 10 and RESSOURCES1['Pierre'] > 5:
                                ressource_construire = [("Bois", 10), ("Pierre", 5)]
                                affiche_presset = True
                                cequejaffiche = tile_images['ceuilleur']
                                cequejepose = tile_info['ceuilleur']
                            else:
                                NotEngoutRessources = True
                        elif selected_button_0_1 == [2, 1]:
                            affiche_presset = True
                            cequejaffiche = tile_images['herbe']
                            cequejepose = tile_info['herbe']
                        elif selected_button_0_1 == [2, 2]:
                            affiche_presset = True
                            cequejaffiche = tile_images['arbre']
                            cequejepose = tile_info['arbre']
                        elif selected_button_0_1 == [2, 3]:
                            affiche_presset = True
                            cequejaffiche = tile_images['baies']
                            cequejepose = tile_info['baies']
                        elif selected_button_0_1 == [2, 4]:
                            affiche_presset = True
                            cequejaffiche = tile_images['pierre']
                            cequejepose = tile_info['pierre']
                        elif selected_button_0_1 == [2, 5]:
                            affiche_presset = True
                            cequejaffiche = tile_images['fer']
                            cequejepose = tile_info['fer']
                    else:
                        selected_button_0_1[1] = 1
                elif event.key == pygame.K_r and rotate == True:
# PLUS DE ROTATION
                    pass 
                    if rotation == 4: rotation = 0
                    img_chemin = ('chemin0', 'chemin1', 'chemin2', 'chemin3')
                    cequejaffiche =  tile_images[img_chemin[rotation]]
                    cequejepose = tile_info[img_chemin[rotation]]
                    rotation += 1
                elif event.key == pygame.K_ESCAPE:
                    ressource_construire = []
                    rotate = False
                    selected_button_0_1[1] = 0
                    affiche_presset = False
                    cequejaffiche = None
            TIME1 = current_time

    # ===================== Actions possibles du joueur dans le jeu =====================
    if variable_info_tuile == 1:
        afficher_valeurs(savefile, key_type, FONT, OLDMOUSE_X, OLDMOUSE_Y)
    
    # Gerer le menu
    draw_button_menu(screen)
    if NotEngoutRessources:
        Render_Text("Pas assez de ressources", (255, 0, 0), (1440, 200), FONT)
    
    # Affichage info d'une tuile
    if mouse[0]:  # Clic gauche
        if 15 < mouse_x < 1405 and 165 < mouse_y < 1065:
            OLDMOUSE_X, OLDMOUSE_Y = mouse_x, mouse_y
            variable_info_tuile = 0
            afficher_valeurs(savefile, key_type, FONT, OLDMOUSE_X, OLDMOUSE_Y)
            variable_info_tuile = 1
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()