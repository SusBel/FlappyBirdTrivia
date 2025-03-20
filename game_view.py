# view.py
import pygame
from game_model import WIDTH, HEIGHT, BIRD_X, BIRD_RADIUS, BLUE, GREEN, BLACK, BUTTON_COLOR, BUTTON_HOVER_COLOR, SQUARE_SIZE

def init_display():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    return screen, clock, font

def draw_main_menu(screen, model, font, button_rect):
    screen.fill((255, 255, 255))  # White background
    
    # Choose button text based on whether the face has been scanned
    button_text = "Scan Face" if not model.face_scanned else "Play"
    
    # Change button color on hover
    mouse_pos = pygame.mouse.get_pos()
    current_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, current_color, button_rect)
    
    text_surface = font.render(button_text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    
    pygame.display.update()

def draw_game(screen, model, font):
    screen.fill((255, 255, 255))  # White background
    
    # Draw the bird
    bird_rect = pygame.Rect(BIRD_X - BIRD_RADIUS, int(model.bird_y) - BIRD_RADIUS, BIRD_RADIUS * 2, BIRD_RADIUS * 2)
    pygame.draw.circle(screen, BLUE, (BIRD_X, int(model.bird_y)), BIRD_RADIUS)
    
    # Draw the obstacle squares
    for square in model.squares:
        pygame.draw.rect(screen, GREEN, (square[0], square[1], SQUARE_SIZE, SQUARE_SIZE))
    
    # Draw YES/NO text objects
    for text_obj in model.text_objects:
        text_surface = font.render(text_obj["text"], True, BLACK)
        screen.blit(text_surface, text_obj["pos"])
    
    # Display the score
    score_text = font.render(f"Score: {model.score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Display the current question (if obstacles are active)
    if model.squares:
        question_surface = font.render(model.current_question, True, BLACK)
        qx = (WIDTH - question_surface.get_width()) // 2
        screen.blit(question_surface, (qx, 50))
    
    pygame.display.update()
