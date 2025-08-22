#################################################################
# FILE : main.py
# WRITER1 : Yonatan Green , yonatan.green1 , 323865386
# WRITER2 : Guy Fussfeld , guyfussfeld , 207766973
# EXERCISE : intro2cs ex10 2022-2023
# DESCRIPTION: snake
#################################################################

import argparse
from game import SnakeGame
from display import GameDisplay
from snake import Snake


def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:
    round_counter = 0
    #init board
    snake = Snake(args.width, args.height)
    game = SnakeGame(snake, args)
    game.add_wall()
    game.add_apple()
    
    # DRAW BOARD AND SHOW SCORE
    game.draw_board(gd)
    gd.show_score(0)
    # END OF ROUND 0  
    gd.end_round()
    
    round_counter += 1
    while not game.is_over(round_counter):
        # CHECK KEY CLICKS
        key_clicked = gd.get_key_clicked()
        game.read_key(key_clicked)
        # Check if snake should be slices, and do so
        game.check_slice_and_slice_snake()
        # UPDATE OBJECTS - 
        #1 Move/Grow Snake (not debug mode)
        #2 Move walls on every second round
        #3 Check collisions
        #4 try add wall and try add apple
        game.update_objects(round_counter)
        # DRAW BOARD
        game.draw_board(gd)
        # End Round
        gd.show_score(game.get_score())
        gd.end_round()
        round_counter += 1


if __name__ == "__main__":
    print("You should run:\n"
          "> python display.py")
