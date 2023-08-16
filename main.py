import pygame
import sys
from settings import *
from grid import Grid
from menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.restart()
        self.menu = Menu(self)

    def restart(self):
        self.grid = Grid(self.screen)
        
    def draw(self):
        self.screen.fill("gray")
        self.grid.update()
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.restart()
    
    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
        pygame.display.set_caption('Minesweeper')
        
    def run(self):
        while True:
            self.check_events()
            self.draw()
            self.menu.update()   
            self.update()
        
if __name__ == '__main__':
    game = Game()
    game.run()