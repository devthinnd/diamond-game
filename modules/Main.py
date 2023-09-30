import pygame
from pygame.locals import *
import time
from constants.constants import SIZE, SRC_BG, SRC_BG_MUSIC, SRC_CRASH, SRC_DING
from modules.Diamond import Diamond
from modules.Snake import Snake

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Diamond Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.diamond = Diamond(self.surface)
        self.diamond.draw()

    def play_background_music(self):
        pygame.mixer.music.load(SRC_BG_MUSIC)
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound(SRC_CRASH)
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound(SRC_DING)

        pygame.mixer.Sound.play(sound)
        # pygame.mixer.music.stop()


    def reset(self):
        self.snake = Snake(self.surface)
        self.diamond = Diamond(self.surface)


    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load(SRC_BG)
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.diamond.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating diamond scenario
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.diamond.x, self.diamond.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.diamond.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Amount diamond: {self.snake.length}", True, (255, 97, 0))
        self.surface.blit(score, (10,10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Hahahahaha... You lose! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter.\nTo exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.1)