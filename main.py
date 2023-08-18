import pygame
import sys
from settings import *
from grid import Grid
from menu import Menu
from ai import AI


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.restart()
        self.menu = Menu(self)

    def restart(self):
        self.grid = Grid(self)
        self.pause = False
        self.ai = AI(self.grid)
        
    def draw(self):
        self.screen.fill("gray")
        if self.grid.check_if_lost() or self.grid.check_if_won():
                self.pause = True
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
            if not self.pause:
                self.draw()
            self.menu.update()   
            self.update()
        
if __name__ == '__main__':
    game = Game()
    game.run()