#################################################################
# FILE : snake_game.py
# WRITER1 : Yonatan Green , yonatan.green1 , 323865386
# WRITER2 : Guy Fussfeld , guyfussfeld , 207766973
# EXERCISE : intro2cs ex10 2022-2023
# DESCRIPTION: snake
#################################################################

from typing import Optional
from game_display import GameDisplay
from game_utils import *
from apple import Apple
from wall import Wall
import math


class SnakeGame:

    def __init__(self, snake, args) -> None:
        self.__args = args

        self.__snake = snake

        self.__apples = [] #list of apples on board
        self.__walls = [] #list of wall on board

        self.__score = 0

        self.__slice_index = -1 #flag the indicates if should slice snake, and where
        self.__growth_counter = 0 #counts the num of rounds that snake should grow 

        self.__is_game_over = False

#################################################################
                    #START FUNCTIONS
#################################################################
    def update_objects(self, round_number) -> None:
        """this function updates objects on the board 
            according to gameplay
        """
        if not self.__args.debug: #if not in debug mode
            beggining_length = self.__snake.get_length()

            # growth
            did_grow = self.snake_growth_handle()

            # regular movement - only if did not grow
            if (not did_grow) and (not self.__is_game_over):
                self.move_the_snake()
            
            #apple consuming handle
            if self.check_eat_and_eat_apple():
                self.__score += math.floor(math.sqrt(beggining_length))

        # every even round
        if (round_number % 2 == 0 and round_number != 0) and not self.check_snake_wall_collision():  
            self.move_walls()
            self.remove_walls()  # remove walls that left the borders

        self.add_wall()
        self.add_apple()

    def read_key(self, key_clicked: Optional[str]) -> None:
        if key_clicked != None:
            snake_dir = self.__snake.get_dir()
            # make sure not turning 180 
            if snake_dir in ["Up", "Down"] and key_clicked in ["Right", "Left"]:
                self.__snake.set_dir(key_clicked)
            if snake_dir in ["Right", "Left"] and key_clicked in ["Up", "Down"]:
                self.__snake.set_dir(key_clicked)

    def draw_board(self, gd: GameDisplay) -> None:
        """this function draws all board objects"""
        # draw snake
        if not self.__args.debug:
            for cell in self.__snake.get_body():
                gd.draw_cell(cell[0], cell[1], self.__snake.get_color())
        # draw apples
        for apple in self.__apples:
            pos = apple.get_pos()
            gd.draw_cell(pos[0], pos[1], apple.get_color())
        # draw walls
        for wall in self.__walls:
            for cell in wall.get_cells():
                if self.check_bounds([cell]):
                    gd.draw_cell(cell[0], cell[1], wall.get_color())
    
    def is_over(self, round) -> bool:
        """checks if game over flag was lifted or rounds number exceeded"""
        return self.__is_game_over or (self.__args.rounds >= 0 and self.__args.rounds < round)
    
    def get_score(self):
        return self.__score 
#################################################################
                     #CHECKS
#################################################################
    def check_cell_empty(self, cell):
        """this function checks if a given cell is empty"""

        snake_occupied_cells = self.__snake.get_body()
        apples_occupied_cells = [apple.get_pos() for apple in self.__apples]
        walls_occupied_cells = []
        for wall in self.__walls:
            for pos in wall.get_cells():
                walls_occupied_cells.append(pos)

        occupied_cells = snake_occupied_cells + apples_occupied_cells + walls_occupied_cells

        return not (cell in occupied_cells)
    
    def check_bounds(self, cell_lst):
        """this function check if all given cells in a list 
            are inside bounds of the board
        """
        is_in_bounds = True
        for cell in cell_lst:
            horizontal_check = 0 <= cell[0] and cell[0] < self.__args.width
            vertical_check = 0 <= cell[1] and cell[1] < self.__args.height
            if not (horizontal_check and vertical_check):
                is_in_bounds = False #cell not in bounds
        return is_in_bounds



#################################################################
                     #Snake Related
#################################################################
    def snake_growth_handle(self):
        """this function handles snake growth
            returns true if growth happened, else false
        """
        did_grow = False
        if self.__growth_counter > 0: #if should grow this round
            did_grow = True
            self.__snake.grow_snake()
            self.__growth_counter -= 1 

        #every time snake grows, checks if game is over
        self.__is_game_over = (self.__snake.is_self_collapsed()) or \
            (not self.check_bounds([self.__snake.get_head()])) or \
            self.check_snake_wall_collision()

        return did_grow

    def check_snake_wall_collision(self):
        """returns True if snake collides with a wall
            else returns False
        """
        head = self.__snake.get_head()
        #check if snake head is in one of the walls body
        for wall in self.__walls:
            if head in wall.get_cells():
                return True
        return False
    
    def check_slice_and_slice_snake(self):
        # if need to slice the snake
        if self.__slice_index != -1:
            # slice
            self.__snake.slice_snake(self.__slice_index)
            self.__slice_index = -1
    
    def move_the_snake(self):
        self.__snake.move_snake()

        self.__is_game_over = (self.__snake.is_self_collapsed()) or \
            (not self.check_bounds([self.__snake.get_head()])) or \
            self.check_snake_wall_collision()
        if self.__is_game_over: #for drawing snake headless
            self.__snake.remove_head()

#################################################################
                     #Wall Related
#################################################################
    def add_wall(self):
        if len(self.__walls) < self.__args.walls:  # can add
            x, y, dir = get_random_wall_data()
            wall = Wall((x, y), dir)

            #check that all cells are empty
            is_empty = True
            for cell in wall.get_cells():
                if not self.check_cell_empty(cell):
                    is_empty = False
                    break

            if is_empty:
                self.__walls.append(wall)

    def move_walls(self):
        """move all walls on board and alert snake slicing"""
        min_hit_index = self.__snake.get_length()

        for wall in self.__walls:
            wall.move_wall()
            # check if hit apple
            for i, apple in enumerate(self.__apples):
                if apple.get_pos() == wall.get_cells()[0]:
                    del self.__apples[i]
                    break
            # check if hit snake
            wall_head = wall.get_cells()[0]
            for index, snake_cell in enumerate(self.__snake.get_body()):
                if wall_head == snake_cell:
                    if index < min_hit_index:
                        min_hit_index = index # remember closest to head hit index

        if min_hit_index != self.__snake.get_length():  # wall hit snake
            self.__slice_index = min_hit_index
            if min_hit_index == 1 or min_hit_index == 0:  # if new snake length is 0 or 1
                self.__is_game_over = True

    def remove_walls(self):
        """this function removes all out of bounds walls"""
        indexs_to_remove = []
        for index, wall in enumerate(self.__walls):
            # check wall tail in bounds
            if not self.check_bounds([wall.get_cells()[2]]):
                indexs_to_remove.append(index)

        # remove from last index to first, to prevent index issues
        for i in indexs_to_remove[::-1]: 
            del self.__walls[i]

#################################################################
                     #Apple Related
#################################################################

    def add_apple(self):
        if len(self.__apples) < self.__args.apples:  # can add
            pos = get_random_apple_data()
            if self.check_cell_empty(pos):
                apple = Apple(pos)
                self.__apples.append(apple)

    def check_eat_and_eat_apple(self) -> bool:
        """this function checks if snake hit apple
            return True if did else False
        """
        index = -1
        snake_head = self.__snake.get_head()
        #locate apple index to be eaten
        for i in range(len(self.__apples)):
            if snake_head == self.__apples[i].get_pos(): 
                index = i
                break
        #eat the apple
        if index != -1:
            del self.__apples[index]
            self.__growth_counter += 3
            return True
        return False
    
        
