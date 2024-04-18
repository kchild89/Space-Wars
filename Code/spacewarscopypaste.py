import pygame
import time
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1400, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Wars")

pygame.mixer.music.load("Audio/main-audio.mp3")
start_sound = pygame.mixer.Sound("Audio/start-audio.mp3")

BG = pygame.transform.scale(pygame.image.load("Images/background.jpeg"), (WIDTH, HEIGHT))

SHIP_WIDTH = 80
SHIP_HEIGHT = 80
SHIP_VEL = 14

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 12

EXPLOSION_WIDTH = 200
EXPLOSION_HEIGHT = 200

FONT = pygame.font.SysFont("comicsans", 40)

# Load ship image
SHIP_IMAGE = pygame.image.load("Images/space44.png").convert_alpha()
SHIP_IMAGE = pygame.transform.scale(SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))

EXPLOSION_IMAGE = pygame.image.load("Images/explosion.png").convert_alpha()
EXPLOSION_IMAGE = pygame.transform.scale(EXPLOSION_IMAGE, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))

def draw(player, elapsed_time, stars, explosion):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Draw ship image
    WIN.blit(SHIP_IMAGE, (player.x, player.y))

    for star in stars:
        pygame.draw.rect(WIN, "red", star)

    if explosion:
        WIN.blit(EXPLOSION_IMAGE, (explosion[0], explosion[1]))

    pygame.display.update()


def main():
    run = True

    start_sound.play()
    pygame.mixer.music.play(-1)

    player = pygame.Rect(200, HEIGHT - SHIP_HEIGHT,
                         SHIP_WIDTH, SHIP_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False
    explosion = None

    while run:
        star_count += clock.tick(60) #Fps
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(5):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT,
                                   STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - SHIP_VEL >= 0:
            player.x -= SHIP_VEL

        if keys[pygame.K_RIGHT] and player.x + SHIP_VEL + player.width <= WIDTH:
            player.x += SHIP_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                explosion = (player.x + player.width / 2 - EXPLOSION_WIDTH / 2, player.y + player.height / 2 - EXPLOSION_HEIGHT / 2)
                hit = True
                pygame.time.delay(500) # Delay to show explosion effect
                break

        draw(player, elapsed_time, stars, explosion)

    # Show "You Lost!" message after explosion
    lost_text = FONT.render("You Lost!", 1, "white")
    WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)
    pygame.quit()

if __name__ == "__main__":
    main()
