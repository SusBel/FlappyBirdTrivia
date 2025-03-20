# controller.py
import pygame
from game_model import GameModel, WIDTH, HEIGHT, BIRD_X, BIRD_RADIUS, GRAVITY, JUMP_STRENGTH, ENCOUNTER_TIME, SQUARE_SPEED, TIME_SCORE_INCREMENT, OBSTACLE_BONUS, SQUARE_SIZE
from game_view import init_display, draw_main_menu, draw_game
from face_recognition import face_id_scan

def main_menu(model, screen, clock, font):
    button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 30, 150, 60)
    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not model.face_scanned and button_rect.collidepoint(event.pos):
                    face_id_scan(model)
                elif model.face_scanned and button_rect.collidepoint(event.pos):
                    menu_running = False
        draw_main_menu(screen, model, font, button_rect)
        clock.tick(30)

def game_loop(model, screen, clock, font):
    running = True
    while running:
        model.time_since_last_encounter += 1
        model.total_frames += 1
        
        # Increment score slowly over time
        if model.total_frames % 10 == 0:
            model.score += TIME_SCORE_INCREMENT
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Make the bird jump when space is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                model.bird_velocity = JUMP_STRENGTH
        
        # Update bird movement
        model.bird_velocity += GRAVITY
        model.bird_y += model.bird_velocity
        
        # Create new squares (and a question) every ENCOUNTER_TIME frames
        if model.time_since_last_encounter >= ENCOUNTER_TIME:
            model.create_squares()
            model.time_since_last_encounter = 0
            model.passed_squares.clear()
        
        # Move squares and text objects leftwards
        for square in model.squares:
            square[0] -= SQUARE_SPEED
        for text_obj in model.text_objects:
            text_obj["pos"][0] -= SQUARE_SPEED
        
        # Remove off-screen squares and text objects
        model.squares = [square for square in model.squares if square[0] + SQUARE_SIZE > 0]
        model.text_objects = [text_obj for text_obj in model.text_objects if text_obj["pos"][0] + SQUARE_SIZE > 0]
        
        # Check for collisions with squares
        bird_rect = pygame.Rect(BIRD_X - BIRD_RADIUS, int(model.bird_y) - BIRD_RADIUS, BIRD_RADIUS * 2, BIRD_RADIUS * 2)
        for square in model.squares:
            square_rect = pygame.Rect(square[0], square[1], SQUARE_SIZE, SQUARE_SIZE)
            if bird_rect.colliderect(square_rect):
                running = False
            square_tuple = tuple(square)
            if square[0] + SQUARE_SIZE < BIRD_X and square_tuple not in model.passed_squares:
                model.score += OBSTACLE_BONUS
                model.passed_squares.add(square_tuple)
        
        # Check the player's answer once obstacles pass behind the bird.
        if model.squares and not model.question_checked:
            if model.squares[0][0] + SQUARE_SIZE < BIRD_X:
                model.question_checked = True
                # Assuming the gap is around y = 300: YES if bird is above 300, NO otherwise.
                if model.current_answer == "YES" and model.bird_y >= 300:
                    running = False  # Wrong answer
                elif model.current_answer == "NO" and model.bird_y < 300:
                    running = False  # Wrong answer
        
        # End game if bird goes off-screen
        if model.bird_y + BIRD_RADIUS > HEIGHT or model.bird_y - BIRD_RADIUS < 0:
            running = False
        
        draw_game(screen, model, font)
        clock.tick(30)
    
    pygame.quit()

def run_game():
    pygame.init()
    screen, clock, font = init_display()
    model = GameModel()
    main_menu(model, screen, clock, font)
    game_loop(model, screen, clock, font)
