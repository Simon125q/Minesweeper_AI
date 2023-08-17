import pygame
from random import randint
from settings import *

class Grid:
    def __init__(self, game):
        self.screen = game.screen
        self.game = game
        self.create_grid()
        self.win = False
        self.lost = False
        
    def __str__(self):
        visual = ''
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col].state != '':
                    visual += self.grid[row][col].state
                else: visual += ' '
            visual += '\n'
            
        return visual
    
    def create_grid(self):
        self.grid = [[0 for row in range(GRID_SIZE)] for col in range(GRID_SIZE)]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.grid[row][col]=Box(row, col, self)
        self.fill_grid()
                
    def fill_grid(self):
        self.locate_bombs()
        self.mark_bombs()
        
    def locate_bombs(self):
        curr_bombs = 0
        while curr_bombs < BOMB_NUM:
            rand_x = randint(0, GRID_SIZE-1)
            rand_y = randint(0, GRID_SIZE-1)
            if self.grid[rand_x][rand_y].value != 'B':
                self.grid[rand_x][rand_y].value = 'B'
                curr_bombs += 1
                
    def mark_bombs(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col].value != 'B':
                    bombs = self.calculate_bombs(self.grid[row][col])
                    self.grid[row][col].value = str(bombs)
                    
    def calculate_bombs(self, curr):
        bombs = 0
        curr_x = curr.x // TILE
        curr_y = curr.y // TILE
        if curr_x - 1 >= 0:
            if self.grid[curr_x - 1][curr_y].value == "B":
                bombs += 1
        if curr_y - 1 >= 0:
            if self.grid[curr_x][curr_y - 1].value == "B":
                bombs += 1
        if curr_x + 1 < GRID_SIZE:
            if self.grid[curr_x + 1][curr_y].value == "B":
                bombs += 1
        if curr_y + 1 < GRID_SIZE:
            if self.grid[curr_x][curr_y + 1].value == "B":
                bombs += 1
        if curr_x - 1 >= 0 and curr_y - 1 >= 0:
            if self.grid[curr_x - 1][curr_y - 1].value == "B":
                bombs += 1
        if curr_y - 1 >= 0 and curr_x + 1 < GRID_SIZE:
            if self.grid[curr_x + 1][curr_y - 1].value == "B":
                bombs += 1
        if curr_y + 1 < GRID_SIZE and curr_x - 1 >= 0:
            if self.grid[curr_x - 1][curr_y + 1].value == "B":
                bombs += 1
        if curr_y + 1 < GRID_SIZE and curr_x + 1 < GRID_SIZE:
            if self.grid[curr_x + 1][curr_y + 1].value == "B":
                bombs += 1           
        return bombs
    
    def unveil_zero(self, curr):
        curr_x = curr.x // TILE
        curr_y = curr.y // TILE
        if curr_x - 1 >= 0:
            self.grid[curr_x - 1][curr_y].state = State.VISITED
        if curr_y - 1 >= 0:
            self.grid[curr_x][curr_y - 1].state = State.VISITED
        if curr_x + 1 < GRID_SIZE:
            self.grid[curr_x + 1][curr_y].state = State.VISITED
        if curr_y + 1 < GRID_SIZE:
            self.grid[curr_x][curr_y + 1].state = State.VISITED
        if curr_x - 1 >= 0 and curr_y - 1 >= 0:
            self.grid[curr_x - 1][curr_y - 1].state = State.VISITED
        if curr_y - 1 >= 0 and curr_x + 1 < GRID_SIZE:
            self.grid[curr_x + 1][curr_y - 1].state = State.VISITED
        if curr_y + 1 < GRID_SIZE and curr_x - 1 >= 0:
            self.grid[curr_x - 1][curr_y + 1].state = State.VISITED
        if curr_y + 1 < GRID_SIZE and curr_x + 1 < GRID_SIZE:
            self.grid[curr_x + 1][curr_y + 1].state = State.VISITED      
    
    def check_if_lost(self):
        for row in self.grid:
            for box in row:
                if box.value == "B" and box.state == State.VISITED:
                    self.show_bombs()
                    self.game.pause = True
        
    def show_bombs(self):
        for row in self.grid:
            for box in row:
                if box.value == "B":
                    box.state = State.VISITED
                
    def update(self):
        self.check_if_lost()
        for row in self.grid:
            for box in row:
                if box.state == State.VISITED and box.value == '0':
                    self.unveil_zero(box)
                
                box.draw(self.screen)
                box.cooldown()
            

class Box:
    def __init__(self, x, y, grid):
        self.x = x * TILE
        self.y = y * TILE
        self.grid = grid
        self.state = State.UNVISITED
        self.value = ''
        self.hovered = False
        self.click_time = None
        self.can_click = True
        self.click_cooldown = 300
        
        self.rect = pygame.Rect((self.x + 1, self.y + 1), (TILE - 2, TILE - 2))
        
    def __str__(self):
        return f"{self.value} box at {self.x} {self.y}"
        
    def draw(self, screen):
        self.check_click()
        if self.hovered:
            pygame.draw.rect(screen, '#888888', self.rect, border_radius = 2)
        else:
            pygame.draw.rect(screen, self.state.value, self.rect, border_radius = 2)
        
        if self.state == State.VISITED and self.value != '0':
            color = 'black'
            if self.value == '1':
                color = 'green'
            elif self.value == '2':
                color = 'yellow'
            else:
                color = 'red'    
            self.text_surf = FONT.render(self.value, True, color)
            self.text_rect = self.text_surf.get_rect(center = self.rect.center)
            screen.blit(self.text_surf, self.text_rect)
        
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_click and current_time - self.click_time > self.click_cooldown:
            self.can_click = True
        
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
            if pygame.mouse.get_pressed()[0]:
                if self.state == State.UNVISITED:
                    self.state = State.VISITED
                    if self.value == '0':
                        self.grid.unveil_zero(self)
                    elif self.value == 'B':
                        self.grid.lost = True
            if self.can_click and pygame.mouse.get_pressed()[2]:
                self.click_time = pygame.time.get_ticks()
                self.can_click = False
                if self.state == State.UNVISITED:
                    self.state = State.FLAG
                elif self.state == State.FLAG:
                    
                    self.state = State.UNVISITED
        else:
            self.hovered = False
            
    
        
        

