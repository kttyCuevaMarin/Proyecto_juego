import pygame
import random
import time
import os

pygame.init()

# ------------------- CONFIGURACION -------------------
WIDTH = 480
HEIGHT = 750
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FRUIT GAME")
FPS = 60
clock = pygame.time.Clock()

# ------------------- COLORES -------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_PINK = (230, 120, 140)
BG_PURPLE = (120, 80, 160)
PURPLE2 = (150, 110, 200)
YELLOW = (255, 255, 100)
GREEN = (100, 255, 100)
RED = (255, 100, 100)

# ------------------- FUENTES -------------------
font_big = pygame.font.Font(None, 60)
font_med = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 28)

# ------------------- RANKING -------------------
RANKING_FILE = "ranking.txt"

def save_score(score):
    scores = []
    if os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, "r") as f:
            scores = [int(line.strip()) for line in f.readlines()]
    scores.append(score)
    scores = sorted(scores, reverse=True)[:5] 
    with open(RANKING_FILE, "w") as f:
        for s in scores:
            f.write(f"{s}\n")
    return scores

# ------------------- ANIMACION DE FRUTAS EN MENU -------------------
fruit_positions = []

def draw_falling_fruits():
    global fruit_positions
    if len(fruit_positions) < 12:
        fruit_positions.append([
            random.randint(0, WIDTH - 40),
            random.randint(-800, -40),
            random.choice([RED, YELLOW, GREEN]),
            random.choice([-1,1])
        ])
    for fruit in fruit_positions:
        x, y, color, dir_x = fruit
        pygame.draw.circle(display, color, (x, y), 18)
        fruit[1] += 2
        fruit[0] += dir_x
        if fruit[0] <= 0 or fruit[0] >= WIDTH:
            fruit[3] *= -1
    fruit_positions[:] = [f for f in fruit_positions if f[1] < HEIGHT]

# ------------------- CONTADOR REGRESIVO -------------------
def countdown_screen():
    for i in range(3, 0, -1):
        display.fill(BG_PURPLE)
        draw_falling_fruits()
        countdown_text = font_big.render(str(i), True, WHITE)
        rect = countdown_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        display.blit(countdown_text, rect)
        pygame.display.update()
        pygame.time.delay(1000)
    display.fill(BG_PURPLE)
    start_text = font_big.render("¡YA!", True, WHITE)
    rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    display.blit(start_text, rect)
    pygame.display.update()
    pygame.time.delay(1000)

# ------------------- PANTALLA DE INICIO -------------------
def start_screen():
    title = font_big.render("FRUIT GAME", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 160))
    subtitle = font_med.render("¡Atrapa las frutas!", True, WHITE)
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 220))
    instructions = [
        "A  y  D  para mover la canasta",
        "Manzana y Plátano = Puntos",
        "Poción = +1 Vida",
        "Si caen frutas pierdes vida"
    ]
    button_rect = pygame.Rect(WIDTH//2 - 110, 480, 220, 70)
    button_text = font_med.render("EMPEZAR", True, WHITE)
    button_flash_timer = 0
    flash_on = True
    waiting = True
    while waiting:

        for i in range(HEIGHT):
            color = (
                int(BG_PURPLE[0] * (i/HEIGHT) + PURPLE2[0]*(1-i/HEIGHT)),
                int(BG_PURPLE[1] * (i/HEIGHT) + PURPLE2[1]*(1-i/HEIGHT)),
                int(BG_PURPLE[2] * (i/HEIGHT) + PURPLE2[2]*(1-i/HEIGHT))
            )
            pygame.draw.line(display, color, (0,i), (WIDTH,i))
        draw_falling_fruits()
        display.blit(title, title_rect)
        display.blit(subtitle, subtitle_rect)
        y = 300
        for line, color in zip(instructions, [RED, YELLOW, GREEN, WHITE]):
            pygame.draw.circle(display, color, (WIDTH//2-120, y+10), 10)
            t = font_small.render(line, True, WHITE)
            rect = t.get_rect(center=(WIDTH//2+30, y+10))
            display.blit(t, rect)
            y += 40
        # Botón parpadeante
        button_flash_timer += 1
        if button_flash_timer % 60 == 0:
            flash_on = not flash_on
        pygame.draw.rect(display, BLACK if flash_on else PURPLE2, button_rect, border_radius=20)
        text_rect = button_text.get_rect(center=button_rect.center)
        display.blit(button_text, text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
    countdown_screen()  

# ------------------- GAME OVER -------------------
def game_over_screen(final_score):
    best_scores = save_score(final_score)
    animation_y = 0
    title = font_big.render("¡PERDISTE!", True, WHITE)
    reason = font_med.render("Se te acabaron las vidas", True, WHITE)
    score_text = font_med.render(f"Puntaje final: {final_score}", True, WHITE)
    button_rect = pygame.Rect(WIDTH//2 - 140, 520, 280, 75)
    button_text = font_med.render("VOLVER A INTENTAR", True, WHITE)
    running = True
    anim_speed = 0.5  # velocidad suave
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False

        animation_y += anim_speed
        if animation_y > HEIGHT:
            animation_y = 0

        display.fill((200, 80, 100))
        pygame.draw.circle(display, (255, 180, 200), (WIDTH//2, int(animation_y)), 250)
        pygame.draw.circle(display, (230, 140, 170), (WIDTH//2, int(animation_y - 200)), 200)

        display.blit(title, title.get_rect(center=(WIDTH//2, 200)))
        display.blit(reason, reason.get_rect(center=(WIDTH//2, 270)))
        display.blit(score_text, score_text.get_rect(center=(WIDTH//2, 320)))

        # Ranking
        y_rank = 380
        rank_title = font_med.render("Mejores Puntajes:", True, WHITE)
        display.blit(rank_title, rank_title.get_rect(center=(WIDTH//2, y_rank)))
        y_rank += 40
        for i, s in enumerate(best_scores):
            text = font_small.render(f"{i+1}. {s}", True, WHITE)
            display.blit(text, text.get_rect(center=(WIDTH//2, y_rank)))
            y_rank += 30

        # Botón
        pygame.draw.rect(display, BLACK, button_rect, border_radius=25)
        display.blit(button_text, button_text.get_rect(center=button_rect.center))

        pygame.display.update()
        clock.tick(FPS)

    countdown_screen()

# ------------------- GAME LOOP -------------------
def game_loop():
    pygame.mixer.music.load("audio/fondo.mp3")
    pygame.mixer.music.play(-1)
    BASKET_VELOCITY = 9
    Score = 0
    player_lives = 5
    apple_speed = 3
    banana_speed = 4
    potion_speed = 2
    basket = pygame.image.load("imagenes/Canasta.png")
    apple = pygame.image.load("imagenes/manzana.png")
    banana = pygame.image.load("imagenes/platano.png")
    potion = pygame.image.load("imagenes/item.png")
    basket_rect = basket.get_rect(center=(WIDTH//2, HEIGHT-50))
    apple_rect = apple.get_rect(x=random.randint(0, WIDTH-64), y=140)
    banana_rect = banana.get_rect(x=random.randint(0, WIDTH-64), y=0)
    potion_rect = potion.get_rect(x=random.randint(0, WIDTH-64), y=-200)
    feedbacks = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and basket_rect.left > 0:
            basket_rect.x -= BASKET_VELOCITY
        if keys[pygame.K_d] and basket_rect.right < WIDTH:
            basket_rect.x += BASKET_VELOCITY
        # Caída frutas
        apple_rect.y += apple_speed
        banana_rect.y += banana_speed
        potion_rect.y += potion_speed
        if apple_rect.y > HEIGHT:
            player_lives -= 1
            apple_rect.y = 140
            apple_rect.x = random.randint(0, WIDTH-64)
            feedbacks.append({'text': '-1 vida', 'pos': (basket_rect.centerx, basket_rect.y-30), 'timer': time.time()})
        if banana_rect.y > HEIGHT:
            player_lives -= 1
            banana_rect.y = 0
            banana_rect.x = random.randint(0, WIDTH-64)
            feedbacks.append({'text': '-1 vida', 'pos': (basket_rect.centerx, basket_rect.y-30), 'timer': time.time()})
        if potion_rect.y > HEIGHT:
            potion_rect.y = -200
            potion_rect.x = random.randint(0, WIDTH-64)
        # Colisiones
        if basket_rect.colliderect(apple_rect):
            Score += 1
            apple_rect.y = 140
            apple_rect.x = random.randint(0, WIDTH-64)
            feedbacks.append({'text': '+1', 'pos': (basket_rect.centerx, basket_rect.y-30), 'timer': time.time()})
        if basket_rect.colliderect(banana_rect):
            Score += 3
            banana_rect.y = 0
            banana_rect.x = random.randint(0, WIDTH-64)
            feedbacks.append({'text': '+3', 'pos': (basket_rect.centerx, basket_rect.y-30), 'timer': time.time()})
        if basket_rect.colliderect(potion_rect):
            player_lives += 1
            potion_rect.y = -200
            potion_rect.x = random.randint(0, WIDTH-64)
            feedbacks.append({'text': '+1 vida', 'pos': (basket_rect.centerx, basket_rect.y-30), 'timer': time.time()})
        if player_lives <= 0:
            pygame.mixer.music.stop()
            game_over_screen(Score)
            return

        display.fill(DARK_PINK)
        display.blit(basket, basket_rect)
        display.blit(apple, apple_rect)
        display.blit(banana, banana_rect)
        display.blit(potion, potion_rect)
        score_txt = font_small.render(f"SCORE: {Score}", True, WHITE)
        lives_txt = font_small.render(f"VIDAS: {player_lives}", True, WHITE)
        display.blit(score_txt, (10, 90))
        display.blit(lives_txt, (WIDTH-120, 90))
        pygame.draw.line(display, WHITE, (0, 140), (WIDTH, 140), 3)

        current_time = time.time()
        for fb in feedbacks[:]:
            if current_time - fb['timer'] < 1.0:
                txt = font_small.render(fb['text'], True, WHITE)
                fb['pos'] = (fb['pos'][0], fb['pos'][1]-1)
                display.blit(txt, txt.get_rect(center=fb['pos']))
            else:
                feedbacks.remove(fb)

        pygame.display.update()
        clock.tick(FPS)

# ------------------- BUCLE PRINCIPAL -------------------
while True:
    start_screen()
    game_loop()

pygame.quit()
