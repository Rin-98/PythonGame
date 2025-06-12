import pygame
import random

# initialize Pygame
pygame.init()

# Screen Setting 
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Screen Size
pygame.display.set_caption("Catch The Falling Object") # Game Title
clock = pygame.time.Clock()

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SKY = (135, 206, 235)
GRASS = (34, 139, 34)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (34, 139, 34)

# Font
font = pygame.font.SysFont("Arial", 30)

# Player setting
player_width = 60
player_height = 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 60
player_speed = 8

# Objects types
object_types = ['red', 'blue', 'bomb']

# Draw Tree Fuction
def draw_tree(x, y):
    pygame.draw.rect(screen, BROWN, (x + 15, y + 40, 20, 60)) # Trunk
    pygame.draw.polygon(screen, GREEN, [(x + 25, y), (x, y + 40), (x + 50, y + 40)])
    
# Mountain Position
mountain_x = 0

# Reset game Function 
def reset_game():
    global score, lives, level, speed, objects, birds, player_x, cloud_x, game_over, show_entry
    player_x =  WIDTH // 2 - player_width // 2
    objects = [{
        'x': random.randint(0, WIDTH - 30),
        'y': random.randint(-300, -50),
        'type': random.choice(object_types)
    } for _ in range(5)]
    birds = [{"x": i * 150, "y": random.randint(50, 150), "bomb_y": -100} for i in range(5)] 
    cloud_x = -200
    score = 0 
    lives = 3
    level = 1
    speed = 5
    game_over = False
    show_entry = False
    
reset_game()
running = True
    
# Game Loop
while running:
    screen.fill(SKY) # Sky Blue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif show_entry and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if WIDTH//2 - 75 < mx < WIDTH//2 + 75 and HEIGHT//2 + 40 < my < HEIGHT//2 + 90:
                reset_game()
                
    if not game_over:
        # Keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 8
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += 8
        
        # Draw Sun
        pygame.draw.circle(screen, YELLOW, (80, 80), 40)  # Yellow sun   
        
        # Moving Mountain
        mountain_x -= 1
        if mountain_x <= -WIDTH:
            mountain_x = 0
        
        # Draw Mountain as Polygons
        mountain_color =  (100, 100, 100) # Grey
        pygame.draw.polygon(screen, mountain_color, [(mountain_x + 100, HEIGHT - 100), (mountain_x + 300, 250), (mountain_x + 500, HEIGHT - 100)])
        pygame.draw.polygon(screen, mountain_color, [(mountain_x + 400, HEIGHT - 100), (mountain_x + 600, 200), (mountain_x + 800, HEIGHT - 100)])
    
    
        # Draw Trees and Ground
        for x in [100, 250, 400, 520]:
            draw_tree(x, HEIGHT - 160)
        pygame.draw.rect(screen, GREEN, (0, HEIGHT - 100, WIDTH, 100))
    
        # Draw Moving Cloud
        cloud_x += 1
        if cloud_x > WIDTH:
            cloud_x = -200
        pygame.draw.ellipse(screen, WHITE, (cloud_x, 80, 100, 50))
        pygame.draw.ellipse(screen, WHITE, (cloud_x + 30, 70, 100, 50))
        pygame.draw.ellipse(screen, WHITE, (cloud_x + 60, 80, 100, 50))
        
        # Draw player
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        pygame.draw.rect(screen, BLACK, player_rect)
        
        # Move and Draw Object
        for obj in objects:
            obj["y"] += speed
            color = RED if obj["type"] == "red" else BLUE if obj["type"] == "blue" else BLACK
            obj_rect = pygame.Rect(obj["x"], obj["y"], 30, 30)
            pygame.draw.rect(screen, color, obj_rect)
        
            # Collosion dection
            if player_rect.colliderect(obj_rect):
                if obj["type"] == "red": score += 1
                elif obj["type"] == "blue": score -= 1
                elif obj["type"] == "bomb": lives = 0
                obj.update({"y": random.randint(-300, -50), "x": random.randint(0, WIDTH - 30), "type": random.choice(object_types)})
        
            # Missed Objects
            if obj["y"] > HEIGHT:
                if obj["type"] != "bomb": lives -= 1
                obj.update({"y": random.randint(-300, -50), "x": random.randint(0, WIDTH - 30), "type": random.choice(object_types)})
            
        # Birds Flying
        for bird in birds:
            bird["x"] += 2
            if bird["x"] > WIDTH:
                bird["x"] = -20
                bird["y"] = random.randint(50, 150)
            pygame.draw.line(screen, BLACK, (bird["x"], bird["y"]), (bird["x"] + 5, bird["y"] - 5), 2)
            pygame.draw.line(screen, BLACK, (bird["x"] + 5, bird["y"] - 5), (bird["x"] + 10, bird["y"]), 2)
        
            # Drop Bomb From bird
            if random.randint(0, 300) < 2:
                bird["bomb_y"] = bird["y"]
            
            if bird["bomb_y"] < HEIGHT:
                bird["bomb_y"] += speed
                pygame.draw.circle(screen, BLACK, (bird["x"] + 5, int(bird["bomb_y"])), 7)
                if player_rect.colliderect(pygame.Rect(bird["x"] + 5, int(bird["bomb_y"]), 10, 10)):
                    lives = 0
                
        # Update Speed Level
        speed = 5 + score // 5 
        level = score // 10 + 1
    
        # Display info
        score_text = font.render(f"Score: {score}", True, BLACK)
        lives_text = font.render(f"Lives: {'❤️' * lives}", True, RED)
        level_text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 150, 10))
        screen.blit(level_text, (250, 10))
    
        # Game Over Screen with Retry
        if lives <= 0:
            game_over = True
            show_entry = True
        
    else:
        screen.blit(font.render("Game Over!", True, BLACK), (WIDTH // 2 - 80, HEIGHT // 2 - 30))
        pygame.draw.rect(screen, (200, 200, 200), (WIDTH // 2 - 75, HEIGHT // 2 + 40, 150, 50))
        pygame.draw.rect(screen, BLACK, (WIDTH // 2 - 75, HEIGHT // 2 + 40, 150, 50), 2)
        screen.blit(font.render("Retry", True, BLACK), (WIDTH // 2 -  30, HEIGHT // 2 + 50))
    
    pygame.display.flip()
    clock.tick(60)
        
pygame.quit()    
