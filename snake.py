import copy
import curses
import random
import os
import time
from typing import List, Tuple


# Defining objects for type hints
Apple = List[int]  # size 2
Snake = List[List[int]]  # size Nx2, with N being Snake's length
Window = curses.window

# Globals
DIRECTIONS = {
    curses.KEY_LEFT: 'left',
    curses.KEY_RIGHT: 'right',
    curses.KEY_UP: 'up',
    curses.KEY_DOWN: 'down'
}

OPPOSITE_DIRECTIONS = {
    curses.KEY_LEFT: 'right',
    curses.KEY_RIGHT: 'left',
    curses.KEY_UP: 'down',
    curses.KEY_DOWN: 'up'
}

DIFFICULTIES = {
    '1': 500,
    '2': 200,
    '3': 40
}


def main() -> None:
    """Main function of this script."""
    difficulty = select_difficulty()
    score = curses.wrapper(game_loop, difficulty)
    print_score(score=score)


def select_difficulty() -> int:
    """Selects the game difficulty by asking for user input."""
    while True:
        answer = input('Select game difficulty:\n(1): Easy\n(2): Normal\n(3): Hard\nYour choice: ')
        if answer in DIFFICULTIES.keys():
            return DIFFICULTIES[answer]
        print('Invalid option, please type 1, 2 or 3.\n')


def game_loop(window: Window, difficulty: int) -> int:
    """Main game loop. Returns the score obtained by the player."""
    curses.curs_set(0)
    window_size = window.getmaxyx()
    score = 0
    snake = init_snake()  # starting snake
    draw_snake(window, snake)
    apple = get_new_apple(window_size)  # starting apple
    draw_apple(window, apple)
    key = curses.KEY_DOWN  # starting key
    direction = 'down'  # starting direction
    while True:  # main gameplay loop
        window.border(0)
        window.timeout(difficulty)
        next_key = window.getch()
        key = next_key if next_key != -1 else key
        direction = DIRECTIONS[key] if snake_changed_direction(direction, key) else direction
        extend_snake_head(snake, direction)
        if snake_ate_apple(snake, apple):
            apple = get_new_apple(window_size)
            draw_apple(window, apple)
            score += 1
        else:
            tail = shorten_snake(window, snake)
        if game_is_over(snake, window_size):
            return score
        draw_snake(window, snake)


def init_snake() -> Snake:
    """Initializes and returns the Snake at a fixed position."""
    snake = [
        [15, 10],
        [14, 10],
        [13, 10],
    ]
    return snake


def draw_snake(window: Window, snake: Snake) -> None:
    """Draws the Snake on the screen."""
    snake_head, *snake_body = snake
    window.addch(*snake_head, '@')
    for snake_body_part in snake_body:
        window.addch(*snake_body_part, '#')


def get_new_apple(window_size: Tuple[int, int]) -> Apple:
    """Returns a new Apple in a random position on the screen."""
    h, w = window_size
    return [random.randint(1, h-2), random.randint(1, w-2)]


def draw_apple(window: Window, apple: Apple) -> None:
    """Draws the apple on the screen."""
    window.addch(*apple, curses.ACS_DIAMOND)


def snake_changed_direction(direction: str, key: int) -> bool:
    """Checks whether the user pressed a key that's in a different direction
    compared to the direction of the snake's movement."""
    for k, d in OPPOSITE_DIRECTIONS.items():
        if key == k and direction == d:
            return False
    return True


def extend_snake_head(snake: Snake, direction: str) -> None:
    """Extends the snake head one space in the given direction. 
    The body remains in the same position."""
    head = copy.copy(snake[0])
    if direction == 'left':  # increase X coord by 1
        head[1] -= 1
    elif direction == 'right':  # decrease X coord by 1
        head[1] += 1
    elif direction == 'up':  # decrease Y coord by 1
        head[0] -= 1
    elif direction == 'down':  # increase Y coord by 1
        head [0] += 1
    snake.insert(0, head)


def snake_ate_apple(snake: Snake, apple: Apple) -> bool:
    """Checks whether the Snake has eaten the Apple."""
    return snake[0] == apple


def shorten_snake(window: Window, snake: Snake) -> None:
    """Removes the last part of the Snake. This happens when the Snake doesn't eat the Apple. 
    The part is then erased from the screen."""
    tail = snake.pop()
    window.addch(*tail, ' ')


def game_is_over(snake: Snake, window_size: Tuple[int, int]) -> bool:
    """Returns whether the game is over or not."""
    return snake_hit_wall(snake, window_size) or snake_hit_self(snake)


def snake_hit_wall(snake: Snake, window_size: Tuple[int]) -> bool:
    """Returns True if the snake has collided with a wall, False otherwise."""
    head = snake[0]
    for dim, h in zip(window_size, head):
        if not 0 < h < (dim-1):
            return True
    return False


def snake_hit_self(snake: Snake) -> bool:
    """Returns True if the snake has collided with itself, False otherwise."""    
    return snake[0] in snake[1:]


def print_score(score: int) -> None:
    """Prints the score onto the screen."""
    print('Game Over!')
    print(f'Your Score: {score}')


if __name__ == '__main__':
    main()
