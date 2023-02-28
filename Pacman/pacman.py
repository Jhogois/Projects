import pygame
from abc import ABCMeta, abstractmethod
import random

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)
font = pygame.font.SysFont("arial", 24, True, False)

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
PINK = (255, 15, 192)
CYAN = (0, 255, 255)
SPEED = 1
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4


class ElementGame(metaclass=ABCMeta):
    @abstractmethod
    def paint(self, screen):
        pass

    @abstractmethod
    def calculate_rules(self):
        pass

    @abstractmethod
    def process_events(self, events):
        pass


class Movable(metaclass=ABCMeta):
    @abstractmethod
    def accept_movement(self):
        pass

    @abstractmethod
    def refuse_movement(self, directions):
        pass

    @abstractmethod
    def corner(self, directions):
        pass


class Scenario(ElementGame):
    def __init__(self, size, pac) -> None:
        self.pacman = pac
        self.movables = []
        self.score = 0
        # Possible states 0-Playing 1-Paused 2-GameOver 3-Win
        self.state = "PLAYING"
        self.size = size
        self.lifes = 5
        self.matrix = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def add_movable(self, obj):
        self.movables.append(obj)

    def paint_score(self, screen):
        dot_x = 30 * self.size
        img_score = font.render(f'Score: {self.score}', True, YELLOW)
        img_lifes = font.render(f"Lifes: {self.lifes}", True, YELLOW)
        screen.blit(img_score, (dot_x, 50))
        screen.blit(img_lifes, (dot_x, 100))

    def paint_line(self, screen, number_line, line):
        for number_column, column in enumerate(line):
            x = number_column * self.size
            y = number_line * self.size
            half = self.size // 2
            color = BLACK
            if column == 2:
                color = BLUE
            pygame.draw.rect(screen, color, (x, y, self.size, self.size), 0)
            if column == 1:
                pygame.draw.circle(screen, YELLOW, (x + half, y + half), self.size // 10, 0)

    def paint(self, screen):
        if self.state == "PLAYING":
            self.paint_playing(screen)
        elif self.state == "PAUSED":
            self.paint_playing(screen)
            self.paint_paused(screen)
        elif self.state == "GAME-OVER":
            self.paint_playing(screen)
            self.paint_gameover(screen)
        elif self.state == "VICTORY":
            self.paint_playing(screen)
            self.paint_victory(screen)

    def paint_victory(self, screen):
        self.paint_center_text(screen, "C O N G R A T U L A T I O N S  Y O U  W I N ! ! !")

    def paint_center_text(self, screen, text):
        img_text = font.render(text, True, YELLOW)
        text_x = (screen.get_width() - img_text.get_width()) // 2
        text_y = (screen.get_height() - img_text.get_height()) // 2
        screen.blit(img_text, (text_x, text_y))

    def paint_gameover(self, screen):
        self.paint_center_text(screen, "G A M E  O V E R")

    def paint_paused(self, screen):
        self.paint_center_text(screen, "P A U S E D")

    def paint_playing(self, screen):
        for number_line, line in enumerate(self.matrix):
            self.paint_line(screen, number_line, line)
        self.paint_score(screen)

    def get_directions(self, line, column):
        directions = []
        if self.matrix[int(line - 1)][int(column)] != 2:
            directions.append(UP)
        if self.matrix[int(line + 1)][int(column)] != 2:
            directions.append(DOWN)
        if self.matrix[int(line)][int(column - 1)] != 2:
            directions.append(LEFT)
        if self.matrix[int(line)][int(column + 1)] != 2:
            directions.append(RIGHT)
        return directions

    def calculate_rules(self):
        if self.state == "PLAYING":
            self.calculate_rules_playing()
        elif self.state == "PAUSED":
            self.calculate_rules_paused()
        elif self.state == "GAME-OVER":
            self.calculate_rules_gameover()

    def calculate_rules_gameover(self):
        pass

    def calculate_rules_paused(self):
        pass

    def calculate_rules_playing(self):
        for movable in self.movables:
            lin = int(movable.line)
            col = int(movable.column)
            lin_intention = int(movable.line_intention)
            col_intention = int(movable.column_intention)
            directions = self.get_directions(lin, col)
            if len(directions) >= 3:
                movable.corner(directions)
            if isinstance(movable, Ghost) and movable.line == self.pacman.line \
                    and movable.column == self.pacman.column:
                self.lifes -= 1
                if self.lifes <= 0:
                    self.state = "GAME-OVER"
                else:
                    self.pacman.line = 1
                    self.pacman.column = 1
            else:
                if 0 <= col_intention < 28 and 0 <= lin_intention < 29 and \
                        self.matrix[lin_intention][col_intention] != 2:
                    movable.accept_movement()
                    if isinstance(movable, Pacman) and self.matrix[lin][col] == 1:
                        self.score += 1
                        self.matrix[lin][col] = 0
                        if self.score >= 306:
                            self.state = "VICTORY"
                else:
                    movable.refuse_movement(directions)

    def process_events(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.state == "PLAYING":
                        self.state = "PAUSED"
                    else:
                        self.state = "PLAYING"


class Pacman(ElementGame, Movable):

    def __init__(self, size) -> None:
        self.column = 1
        self.line = 1
        self.x_center = 400
        self.y_center = 300
        self.size = size
        self.x_speed = 0
        self.y_speed = 0
        self.ray = self.size // 2
        self.column_intention = self.column
        self.line_intention = self.line
        self.opening = 0
        self.opening_speed = 2

    def calculate_rules(self):
        self.column_intention = self.column + self.x_speed
        self.line_intention = self.line + self.y_speed
        self.x_center = int(self.column * self.size + self.ray)
        self.y_center = int(self.line * self.size + self.ray)

    def paint(self, screen):
        # Draw the Pacman body
        pygame.draw.circle(
            screen, YELLOW, (self.x_center, self.y_center), self.ray
            )
        self.opening += self.opening_speed
        if self.opening > self.ray:
            self.opening_speed = -2
        if self.opening <= 0:
            self.opening_speed = 2
        # Mouth drawing
        mouth_corner = (self.x_center, self.y_center)
        upper_lip = (self.x_center + self.ray, self.y_center - self.opening)
        lower_lip = (self.x_center + self.ray, self.y_center + self.opening)
        dots = [mouth_corner, upper_lip, lower_lip]
        pygame.draw.polygon(screen, BLACK, dots, 0)

        # Pacman's eye
        eye_x = int(self.x_center + self.ray / 3)
        eye_y = int(self.y_center - self.ray * 0.70)
        eye_ray = int(self.ray / 10)
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), eye_ray, 0)

    def process_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.x_speed = SPEED
                elif e.key == pygame.K_LEFT:
                    self.x_speed = -SPEED
                elif e.key == pygame.K_UP:
                    self.y_speed = -SPEED
                elif e.key == pygame.K_DOWN:
                    self.y_speed = SPEED
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.x_speed = 0
                elif e.key == pygame.K_LEFT:
                    self.x_speed = 0
                elif e.key == pygame.K_UP:
                    self.y_speed = 0
                elif e.key == pygame.K_DOWN:
                    self.y_speed = 0

    def accept_movement(self):
        self.line = self.line_intention
        self.column = self.column_intention

    def refuse_movement(self, directions):
        self.line_intention = self.line
        self.column_intention = self.column

    def corner(self, directions):
        pass


class Ghost(ElementGame):
    def __init__(self, color, size) -> None:
        self.column = 13.0
        self.line = 15.0
        self.line_intention = self.line
        self.column_intention = self.column
        self.speed = 1
        self.direction = DOWN
        self.size = size
        self.color = color

    def paint(self, screen):
        cut = self.size // 8
        px = int(self.column * self.size)
        py = int(self.line * self.size)
        contour = [(px, py + self.size),
                   (px + cut, py + cut * 2),
                   (px + cut * 2, py + cut // 2),
                   (px + cut * 3, py),
                   (px + cut * 5, py),
                   (px + cut * 6, py + cut // 2),
                   (px + cut * 7, py + cut * 2),
                   (px + self.size, py + self.size)]
        pygame.draw.polygon(screen, self.color, contour, 0)

        eye_ext_ray = cut
        eye_int_ray = cut // 2

        eye_l_x = int(px + cut * 2.5)
        eye_l_y = int(py + cut * 2.5)

        eye_r_x = int(px + cut * 5.5)
        eye_r_y = int(py + cut * 2.5)

        pygame.draw.circle(screen, WHITE, (eye_l_x, eye_l_y), eye_ext_ray, 0)
        pygame.draw.circle(screen, BLACK, (eye_l_x, eye_l_y), eye_int_ray, 0)
        pygame.draw.circle(screen, WHITE, (eye_r_x, eye_r_y), eye_ext_ray, 0)
        pygame.draw.circle(screen, BLACK, (eye_r_x, eye_r_y), eye_int_ray, 0)

    def calculate_rules(self):
        if self.direction == UP:
            self.line_intention -= self.speed
        elif self.direction == DOWN:
            self.line_intention += self.speed
        elif self.direction == LEFT:
            self.column_intention -= self.speed
        elif self.direction == RIGHT:
            self.column_intention += self.speed

    def change_direction(self, directions):
        self.direction = random.choice(directions)

    def corner(self, directions):
        self.change_direction(directions)

    def accept_movement(self):
        self.line = self.line_intention
        self.column = self.column_intention

    def refuse_movement(self, directions):
        self.line_intention = self.line
        self.column_intention = self.column
        self.change_direction(directions)

    def process_events(self, evts):
        pass


if __name__ == "__main__":
    size = 600 // 30
    pacman = Pacman(size)
    blinky = Ghost(RED, size)
    inky = Ghost(CYAN, size)
    clyde = Ghost(ORANGE, size)
    pinky = Ghost(PINK, size)
    scenario = Scenario(size, pacman)
    scenario.add_movable(pacman)
    scenario.add_movable(blinky)
    scenario.add_movable(inky)
    scenario.add_movable(clyde)
    scenario.add_movable(pinky)

    while True:
        # Calculate the rules
        pacman.calculate_rules()
        blinky.calculate_rules()
        inky.calculate_rules()
        clyde.calculate_rules()
        pinky.calculate_rules()
        scenario.calculate_rules()

        # Paint the screen
        screen.fill(BLACK)
        scenario.paint(screen)
        pacman.paint(screen)
        blinky.paint(screen)
        inky.paint(screen)
        clyde.paint(screen)
        pinky.paint(screen)
        pygame.display.update()
        pygame.time.delay(100)

        # Capture the events
        events = pygame.event.get()
        pacman.process_events(events)
        scenario.process_events(events)
