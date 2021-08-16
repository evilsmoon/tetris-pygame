import pygame, sys, os, random 
from time import sleep
import Figure

from pygame.locals import *
colors = [
    (37, 235, 11),
    (160, 154, 143),
    (139, 176, 186),
    (57, 217, 227),
    (82, 30, 24),
    (13, 216, 46),
    (198, 39, 57)
]
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

level = 1
lines_to_clear = 1
volume = 1.0
mousePosition = None

class Game:
    # level = 1
    lines_cleared = 0
    score = 0
    state = "start"
    field = []  # used to tell which tiles are empty vs ones that contain figures, does not include figure currently falling down
    HEIGHT = 0
    WIDTH = 0
    startX = 100
    startY = 50
    zoom = 20
    figure = None
    

    def __init__(self, height, width):
        self.field = []  # to reset field if needed
        self.figure = None
        self.height = height
        self.width = width
        # for creating a empty field[]
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def create_figure(self):
        self.figure = Figure.Figure(3, 0)

    # checking each cell in the 4x4 matrix that contains the current figure
    # to see whether current figure is out of bounds of game screen
    # or colliding with a fixed figure, returns False for no collisions and no out of bounds instances
    def intersects(self):
        intersects = False
        for i in range(4):
            for j in range(4):
                # making sure tiles containing figure are not 0
                if (i * 4) + j in self.figure.get_image():
                    if (i + self.figure.y) > (self.height - 1) or \
                        (j + self.figure.x) > (self.width - 1) or \
                        (j + self.figure.x) < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersects = True
        return intersects

    def freeze_figure(self):
        for i in range(4):
            for j in range(4):
                # identifies tiles containing figure vs empty tiles in the 4x4 matrix
                if i * 4 + j in self.figure.get_image():
                    # give non zero values to all tiles containing the figure
                    self.field[i + self.figure.y][j +
                                                  self.figure.x] = self.figure.color
        # after freezing, check if any rows are full so that we can remove that row
        self.break_lines()
        # then create new figure
        self.create_figure()
        if self.intersects():
            # if right after creating new figure, it intersects with something
            # then there is a column of fixed figures reaching the top of the screen thereby ending the game
            self.state = "gameover"

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(0, self.width):
                if self.field[i][j] == 0:
                    zeros += 1

            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        # since height index in self.field is in descending order this code assigns the higher row to the lower row
                        self.field[i1][j] = self.field[i1 - 1][j]

        # add to score, if multiple lines are cleared at the same time exponentialize the score
        self.score += lines ** 2
        self.lines_cleared += lines
        self.check_level_up()

    def check_level_up(self):
        global level
        global lines_to_clear
        if self.lines_cleared >= level:  # if number of lines cleared >= game level then level up
            level += 1
            lines_to_clear = level
            self.lines_cleared = 0
            return True
        else:
            # if not ready to level up yet
            # then calculate remaining number of
            # lines to clear in order to level up
            lines_to_clear = level - self.lines_cleared
            return False
    # makes the figure fall down indefinitely until it gets into a collision

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        # take back 1 tile to prevent current figure from touching fixed figures/screen bounds
        self.figure.y -= 1
        self.freeze_figure()

    # similar to go_space() but only goes down 1 tile when executed
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze_figure()

    def go_sideways(self, dx):
        # dx is the direction to go sideways, 1 for right, -1 for left
        previous_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            # if the new figure position intersects with something else
            # then revert back to the previously saved position
            self.figure.x = previous_x

    def rotate(self):
        previous_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            # if there is a collision during new rotation
            # then revert to previous rotation
            self.figure.rotation = previous_rotation
    def _pause(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    print("in")
                    paused = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("on")
                    paused = False
                    break
    def main(self):
        global level
        global lines_to_clear
        global mousePosition, volume
        screen_height = 500
        screen_width = 600
        game_height = 20
        game_width = 10
        pressing_down = False
        gameover = False
        counter = 0
        fps = 30
    
        pygame.init()
        pygame.display.set_caption('tetris')
    
        window = pygame.display.set_mode((screen_height, screen_width))
        clock = pygame.time.Clock()
        game = Game(game_height, game_width)
        pygame.mixer.init()
        pygame.mixer.music.load('music/tetris.ogg')
        pygame.mixer.music.play(-1)
    
        btn_play = pygame.image.load('img/audio-tool-in-silence.png').get_rect().size
    
    
        while not gameover:
            if game.figure is None:
                game.create_figure()
            counter += 1
            if counter > 100000:
                counter = 0
            if counter % (fps // level // 2) == 0 or pressing_down:
                if game.state == "start":
                    game.go_down()
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        game.go_sideways(1)
                    if event.key == pygame.K_LEFT:
                        game.go_sideways(-1)
                    if event.key == pygame.K_UP:
                        game.rotate()
                    if event.key == pygame.K_DOWN:
                        pressing_down = True
                    if event.key == pygame.K_SPACE:
                        game.go_space()
                    if event.key == pygame.K_p:
                        main()
                        
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)
            if event.type == pygame.MOUSEBUTTONUP:
                if mousePosition[0] > 415 and mousePosition[0] < 415 + \
                    btn_play[0]:
                    if mousePosition[1] > 170 and mousePosition[1] < 170 + \
                        btn_play[1]:
                        pygame.mixer.music.pause()
            if event.type == pygame.MOUSEBUTTONUP:
                if mousePosition[0] > 445 and mousePosition[0] < 445 + \
                    btn_play[0]:
                    if mousePosition[1] > 170 and mousePosition[1] < 170 + \
                        btn_play[1]:
                        pygame.mixer.music.unpause()
            if event.type == pygame.MOUSEBUTTONUP:
                if mousePosition[0] > 350 and mousePosition[0] < 350 + \
                    btn_play[0]:
                    if mousePosition[1] > 150 and mousePosition[1] < 150 + \
                        btn_play[1]:
                        game._pause()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mousePosition[0] > 325 and mousePosition[0] < 325 + \
                    btn_play[0]:
                    if mousePosition[1] > 150 and mousePosition[1] < 150 + \
                        btn_play[1]:
                        game._pause()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mousePosition[0] > 375 and mousePosition[0] < 375 + \
                    btn_play[0]:
                    if mousePosition[1] > 150 and mousePosition[1] < 150 + \
                        btn_play[1]:
                        gameover = True
                        main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mousePosition[0] > 400 and mousePosition[0] < 400 + \
                    btn_play[0]:
                    if mousePosition[1] > 150 and mousePosition[1] < 150 + \
                        btn_play[1]:
                        gameover = True
                        pygame.quit()
    
    
            if event.type == pygame.KEYUP:  # event is saved in memory so we can access event outside the for loop
                if event.key == pygame.K_DOWN:
                    pressing_down = False
    
            window.fill(WHITE)
    
            # this is used to draw grey grid on window
            for i in range(game.height):
                for j in range(game.width):
                    # last arg is for line thickness
                    pygame.draw.rect(window, GREY, [
                                     game.startX + game.zoom * j, game.startY + game.zoom * i, game.zoom, game.zoom], 1)
                    if game.field[i][j] > 0:
                        pygame.draw.rect(window, colors[game.field[i][j]],
                                         [game.startX + game.zoom * j, game.startY + game.zoom * i, game.zoom - 2, game.zoom - 1])
    
            # this is used to draw current figure on a 4x4 matrix in game grid
            if game.figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                  
                        if p in game.figure.get_image():
                            pygame.draw.rect(window, colors[game.figure.color],
                                             [
                                game.startX + game.zoom *
                                (j + game.figure.x) + 1,
                                game.startY + game.zoom *
                                (i + game.figure.y) + 1,
                                game.zoom - 2,
                                game.zoom - 2
                            ])
                
            if (game.score ==3):
                pygame.quit()
                
            font2 = pygame.font.SysFont('Consolas', 11, bold=True)
            font1 = pygame.font.SysFont('Comic Sans MS', 11, bold=True)
            text_score = font1.render("Score: " + str(game.score), True, BLACK)
            text_level = font1.render("Level: " + str(level), True, BLACK)
            text_menu = font1.render("Menu: ", True, BLACK)
            text_lines_to_clear = font1.render(
                "Lines to clear: " + str(lines_to_clear), True, BLACK)
            text_game_over1 = font1.render("Game Over", True, BLACK)
            text_game_over2 = font1.render("Press ESC", True, BLACK)
            # text_time_game = font1.render("Time: "+str(clock.get_rawtime()), True,BLACK)
           
            mousePosition = pygame.mouse.get_pos()
            window.blit(pygame.font.SysFont('Consolas',11,bold=True).render("Volumen: "+str(volume*100),True,BLACK),[325,175])
            pygame.draw.rect(window, (229, 229, 229), (325, 200, 100, 5))
            volumePosition = (100 / 100) * (volume * 100)
            pygame.draw.rect(window, (204, 204, 204), (325+volumePosition, 190, 10, 25))
            pygame.mixer.music.set_volume(volume)
            window.blit(pygame.image.load('img/audio-tool-in-silence.png'), (415,170))
            window.blit(pygame.image.load('img/herramienta-de-audio-con-altavoz.png'), (445,170))
            window.blit(pygame.image.load('img/play.png'), (325,150))
            window.blit(pygame.image.load('img/pausa.png'), (350,150))
            window.blit(pygame.image.load('img/repetir.png'), (375,150))
            window.blit(pygame.image.load('img/logout.png'), (400,150))
    
    
            if pygame.mouse.get_pressed()[0] ==True:
                if mousePosition[1] > 200 and mousePosition[1] < 225:
                    if mousePosition[0] > 350 and mousePosition[0] < 450:
                        volume = float((mousePosition[0] - 350)) / 100
    
            # second arg is represents dest where [top, left]
            window.blit(text_score, [100, 20])
            # window.blit(text_time_game, [150, 20])
            window.blit(text_lines_to_clear, [250, 20])
            window.blit(text_level, [250, 5])
            window.blit(text_menu, [325, 125])
            # window.blit()
    
    
    
            if game.check_level_up():
                main()
            if game.state == "gameover":
                window.blit(text_game_over1, [20, 220])
                window.blit(text_game_over2, [20, 275])
    
            pygame.display.flip()
            pygame.display.update()
            clock.tick(fps)  # paces the game to a slower fall speed
    
    
    
    
def main():
    juego = Game(20,10)
    juego.main()
if __name__ == "__main__":
    # call the main function
    main()