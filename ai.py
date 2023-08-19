import pygame
from random import randint
from settings import *

class AI:
    def __init__(self, grid):
        self.grid = grid
        
    def calculate_flags(self, curr):
        flags = 0
        neighbours = self.grid.get_neighbours(curr)
        for neighbour in neighbours:
            if neighbour.state == State.FLAG:
                flags += 1
        return flags
    
    def count_neighbours(self, curr):
        count = 0
        neighbours = self.grid.get_neighbours(curr)
        for neighbour in neighbours:
            if neighbour.state == State.UNVISITED or neighbour.state == State.FLAG:
                count += 1
        return count
    
    def flag_neighbours(self, curr):
        neighbours = self.grid.get_neighbours(curr)
        for neighbour in neighbours:
            if neighbour.state == State.UNVISITED:
                neighbour.state = State.FLAG
            
    def unveil_field(self, curr):
        neighbours = self.grid.get_neighbours(curr)
        for neighbour in neighbours:
            if neighbour.state != State.FLAG:
                neighbour.state = State.VISITED
        
    def check_if_move_possible(self, curr):
        neighbours = self.grid.get_neighbours(curr)
        for neighbour in neighbours:
            if neighbour.state == State.UNVISITED:
                return True
        return False
        
    def make_move(self):
        rand = True
        for row in self.grid.grid:
            for box in row:
                if self.check_if_move_possible(box) and box.value != "B" and box.state == State.VISITED:
                    flags = self.calculate_flags(box)
                    neighbour_count = self.count_neighbours(box)
                    if flags == int(box.value):
                        self.unveil_field(box)
                        rand = False
                        break
                    elif neighbour_count == int(box.value):
                        self.flag_neighbours(box)
                        rand = False
                        break
        while rand and not self.grid.check_if_won() and not self.grid.check_if_lost():
            rand_x = randint(0, GRID_SIZE-1)
            rand_y = randint(0, GRID_SIZE-1)
            if self.grid.grid[rand_x][rand_y].state == State.UNVISITED:
                self.grid.grid[rand_x][rand_y].state = State.VISITED
                rand = False
                
    def solve(self):
        if not self.grid.check_if_won() and not self.grid.check_if_lost():
            self.make_move()