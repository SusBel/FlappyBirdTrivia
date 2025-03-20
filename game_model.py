import random
from questions import questions_list

# Constants and Colors
WIDTH = 400
HEIGHT = 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)

# Game constants
BIRD_X = WIDTH // 4
BIRD_Y = HEIGHT // 2
BIRD_RADIUS = 20
GRAVITY = 0.5
JUMP_STRENGTH = -8
SQUARE_SIZE = 70
ENCOUNTER_TIME = 150  # 5 seconds at 30 FPS
SQUARE_SPEED = 3
TIME_SCORE_INCREMENT = 1  # Slower score increment
OBSTACLE_BONUS = 10  # Bonus points for passing an obstacle

class GameModel:
    def __init__(self):
        self.face_scanned = False
        
        # Bird properties
        self.bird_y = BIRD_Y
        self.bird_velocity = 0
        
        # Obstacles and text objects (for YES/NO)
        self.squares = []
        self.text_objects = []
        
        # Question attributes
        self.current_question = ""
        self.current_answer = ""
        self.question_checked = False
        
        # Game logic variables
        self.time_since_last_encounter = 0
        self.score = 0
        self.passed_squares = set()
        self.total_frames = 0

    def create_squares(self):
        self.squares.clear()
        # Create top, middle, and bottom squares
        self.squares.append([WIDTH, 50])  # Top square
        self.squares.append([WIDTH, HEIGHT // 2 - SQUARE_SIZE // 2])  # Middle square
        self.squares.append([WIDTH, HEIGHT - 100])  # Bottom square
        
        # Attach YES/NO texts to the first and last squares
        self.text_objects = [
            {"text": "YES", "pos": [WIDTH + 20, 180]},
            {"text": "NO", "pos": [WIDTH + 20, HEIGHT - 200]},
        ]
        
        # Pick a random question from the list
        question = random.choice(questions_list)
        self.current_question = question[0]
        self.current_answer = question[1]
        self.question_checked = False
