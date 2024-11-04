"""import des modules"""
import sys
import random
import pygame
#from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Constantes
WHITE = (200, 200, 200)
RED = (200, 50, 50)
NB_STARS = 50
MAX_ASTEROID = 5


class Ship():
    """Ship Class to symbolize player"""
    velocity_y = 0
    score = 0
    speed = 0.3
    health_points = 3

    def set_hitbox(self, image):
        """Set the hitbox of the ship"""
        self.width = image.get_width()
        self.height = image.get_height()
        self.bounding_box = Rect(self.pos_x, self.pos_y/2, self.width, self.height)

    def __init__(self, x_pos, y_pos, ship_image):
        """Ship Constructor"""
        self.pos_x = x_pos
        self.pos_y = y_pos
        self.image = ship_image
        self.set_hitbox(self.image)

    def move(self, direction):
        """To move the ship"""
        if direction == "Down":
            self.velocity_y = self.speed
        elif direction == "Up":
            self.velocity_y = -self.speed
        elif direction == "None":
            self.velocity_y = 0

    def update(self):
        """update function called every frame"""
        if self.pos_y <= 0:
            self.pos_y = 1
        elif self.pos_y >= 580:
            self.pos_y = 579
        else:
            self.pos_y = self.pos_y + self.velocity_y
        self.bounding_box.centery = self.pos_y+self.height/2


class Star():
    """Star Class to populate a space background"""

    def change_size(self):
        """To allow stars to shine by sizing up and down (Feature to be implemented)"""
        pass

    def __init__(self, x_pos, y_pos, size):
        """Star Constructor"""
        self.pos_x = x_pos
        self.pos_y = y_pos
        self.s_size = size

    def update(self):
        """update function called every frame"""
        self.pos_x -= 0.1


class Asteroid():
    """Asteroid Class to act as ennemy of this game. Don't be hit by them!"""

    def set_hitbox(self, image):
        """Set the hitbox of the asteroid"""
        self.width = image.get_width()
        self.height = image.get_height()
        self.bounding_box = Rect(self.pos_x, self.pos_y, self.width, self.height)

    def __init__(self, x_pos, y_pos, ast_image):
        """Asteroid Constructor"""
        self.pos_x = x_pos
        self.pos_y = y_pos
        self.image = ast_image
        self.set_hitbox(self.image)

    def update(self):
        """update function called every frame"""
        self.pos_x -= 0.5
        self.bounding_box.centerx = self.pos_x+self.width/2

def screen_config():
    """Screen Config"""
    window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("No Man's Sky 2D")
    return window_surface

def init_timer():
    """initialize timer at the start"""
    return pygame.time.get_ticks()

def timer(timer_start):
    """return timer in seconds"""
    return (pygame.time.get_ticks() - timer_start)/1000

def spawn_asteroid(ast_timer, list_asteroids, asteroid_image):
    """Spawn asteroid every 3 seconds"""
    if ast_timer % 3 == 0:
        list_asteroids.append(Asteroid(805, random.randint(0, 550), asteroid_image))


def user_interface(player_ship, timer_start, window):
    """Function to display user interface"""
    # font pour l'affichage du texte
    font = pygame.font.Font('freesansbold.ttf', 16)

    # On crée le texte pour le score
    score_text = font.render('Score : '+ str(player_ship.score), True, WHITE)
    # On crée un objet rectangulaire pour la surface du texte
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (SCREEN_WIDTH/2, 10)

    # On crée le texte pour les HP
    hp_text = font.render('HP : '+ str(player_ship.health_points), True, RED)
    hp_text_rect = hp_text.get_rect()
    hp_text_rect.center = (0+hp_text_rect.width/2, 10)


    # On crée le texte pour le timer
    timer_text = font.render(str(timer(timer_start)), True, WHITE)
    timer_text_rect = score_text.get_rect()
    timer_text_rect.center = (SCREEN_WIDTH/2, 30)

    # On dessine le texte du score
    window.blit(score_text, score_text_rect)
    # On dessine le texte du timer
    window.blit(timer_text, timer_text_rect)
    # On dessine le texte des hp
    window.blit(hp_text, hp_text_rect)

def game_over_display():
    """To display sad words"""
    font = pygame.font.Font('freesansbold.ttf', 16)
    # On crée le texte pour le game over
    game_over_text = font.render('GAME OVER', True, RED)
    # On crée un objet rectangulaire pour la surface du texte
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.center = (SCREEN_WIDTH/2-game_over_text_rect.width/2, SCREEN_HEIGHT/2)

def main():
    """Entry point"""
    pygame.init()

    # Chargement des images
    ship_image = pygame.image.load("ship.png")
    asteroid_image_load = pygame.image.load("ast.png")
    asteroid_image = pygame.transform.scale(asteroid_image_load, (48, 40))

    window = screen_config()

    # Création du joueur
    player_ship = Ship(SCREEN_WIDTH/10, SCREEN_HEIGHT/2, ship_image)

    stars = []
    asteroids = []

    # Génération des étoiles
    for _ in range(NB_STARS):
        stars.append(Star(random.randint(0, SCREEN_WIDTH),
                          random.randint(0, SCREEN_HEIGHT),
                          random.randint(1, 5)))
    timer_start = init_timer()

    game_over = False
    # boucle de jeu
    while not game_over:
        if player_ship.health_points <= 0:
            game_over = True

        spawn_asteroid(timer(timer_start),
                       asteroids,
                       asteroid_image)

        # ------------------- Draw block -------------------
        # font pour l'affichage du texte
        font = pygame.font.Font('freesansbold.ttf', 16)

        # On crée le texte pour le score
        score_text = font.render('Score : '+ str(player_ship.score), True, WHITE)

        # On crée un objet rectangulaire pour la surface du texte
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (SCREEN_WIDTH/2, 10)

        # On crée le texte pour le timer
        timer_text = font.render(str(timer(timer_start)), True, WHITE)
        timer_text_rect = score_text.get_rect()
        timer_text_rect.center = (SCREEN_WIDTH/2, 30)

        # On dessine le texte du score
        window.blit(score_text, score_text_rect)
        # On dessine le texte du timer
        window.blit(timer_text, timer_text_rect)
        # Les étoiles sont dessinées avant pour éviter que le ship passe "en dessous" d'une étoile
        # Drawing of stars in the background
        window.fill(0)

        user_interface(player_ship, timer_start, window)

        for star in stars:
            pygame.draw.rect(window, WHITE, (star.pos_x, star.pos_y, star.s_size, star.s_size))
        # On dessine le vaisseau
        window.blit(player_ship.image, (player_ship.pos_x, player_ship.pos_y))
        # dessin des asteroides.
        # Les lignes commentées sont les hitbox des items, décommenter pour voir le resultat
        # GREEN = (0, 255, 0)
        # RED = (255, 0, 0)
        for ast in asteroids:
            window.blit(ast.image, (ast.pos_x, ast.pos_y))
            # pygame.draw.rect(window, GREEN, ast.bounding_box)
        # pygame.draw.rect(window, RED, player_ship.bounding_box)


        # ------------------- Event block -------------------
        #boucle sur les events
        for event in pygame.event.get():
            #check si on ferme la fenêtre avec la croix
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if game_over:
                game_over_display()
                pygame.time.wait(5000)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if player_ship.pos_y < SCREEN_HEIGHT:
                        player_ship.move("Down")
                    else:
                        player_ship.move("None")
                elif event.key == pygame.K_UP:
                    if player_ship.pos_y > 0:
                        player_ship.move("Up")
                    else:
                        player_ship.move("None")
                        player_ship.pos_y = 0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_ship.move("None")
                elif event.key == pygame.K_UP:
                    player_ship.move("None")

        # ------------------- Update block -------------------
        # on update tous les objets ici.
        # Les étoiles
        for star in stars:
            star.update()
            if star.pos_x < 0:
                stars.remove(star)
                stars.append(Star(SCREEN_WIDTH,
                                  random.randint(0, SCREEN_HEIGHT),
                                  random.randint(1, 3)))
        player_ship.update()
        # Les astéroides
        for ast in asteroids:
            ast.update()
            if ast.pos_x < 0:
                asteroids.remove(ast)
                player_ship.score += 1
            if ast.bounding_box.colliderect(player_ship.bounding_box):
                asteroids.remove(ast)
                player_ship.health_points -= 1
        pygame.display.update()


if __name__ == "__main__":
    main()
