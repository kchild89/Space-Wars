import pygame
import time
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1600, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Name of the game
pygame.display.set_caption("Space Wars")

# Load Background Image
background = pygame.transform.scale(pygame.image.load("Images/background.jpeg"), (WIDTH, HEIGHT))

# Load audio
pygame.mixer.music.load("Audio/main-audio.mp3")
start_sound = pygame.mixer.Sound("Audio/start-audio.mp3")


# Ship Size and Velocity
ship_width = 100
ship_heigth = 100
ship_velocity = 18

# Star Size and Velocity
star_width = 35
star_height = 160
star_velocity = 14

# Explosion Size
explosion_width = 400
explosion_height = 200

# Time Style and Size
font = pygame.font.SysFont("comicsans", 40)

# Load Ship Image
ship_image = pygame.image.load("Images/space44.png").convert_alpha()
ship_image = pygame.transform.scale(ship_image, (ship_width, ship_heigth))

# Load Explosion Image 
explosion_image = pygame.image.load("Images/explosion.png").convert_alpha()
explosion_image = pygame.transform.scale(explosion_image, (explosion_width, explosion_height))

# Load Star Image 
star_image = pygame.image.load("Images/star.png").convert_alpha()
star_image = pygame.transform.scale(star_image, (star_width, star_height))

def draw(player, elapsed_time, stars, explosion):
    WIN.blit(background, (0, 0))

    time_text = font.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Draw Ship Image
    WIN.blit(ship_image, (player.x, player.y))
    
    # Draw Star Image
    for star in stars:
        WIN.blit(star_image, (star.x, star.y))

     # Draw explosion if it exists
    if explosion:
        WIN.blit(explosion_image, (explosion[0], explosion[1]))    
    

    pygame.display.update()

def main():
    run = True

    start_sound.play()
    pygame.mixer.music.play(-1)

    player = pygame.Rect(200, HEIGHT - ship_heigth,
                         ship_width, ship_heigth)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    explosion = None
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - star_width)
                star = pygame.Rect(star_x, -star_height,
                                   star_width, star_height)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        
        # Player Movement
        keys = pygame.key.get_pressed()
        
        # Left
        if keys[pygame.K_LEFT] and player.x - ship_velocity >= 0:
            player.x -= ship_velocity
            
        # Right
        if keys[pygame.K_RIGHT] and player.x + ship_velocity + player.width <= WIDTH:
            player.x += ship_velocity

        for star in stars[:]:
            star.y += star_velocity
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                explosion = (player.x + player.width / 2 - explosion_width / 2, player.y + player.height / 2 - explosion_height / 2)
                pygame.time.delay(500)
                hit = True
                
        if explosion:
            WIN.blit(explosion_image, (explosion[0], explosion[1]))
                
            
        # Lost Text        
        if hit:
            lost_text = font.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            
            pygame.display.update()
            pygame.time.delay(2000)
            break
            

        draw(player, elapsed_time, stars, explosion)

    pygame.quit()

if __name__ == "__main__":
    main()
