from snake import Snake
import gui


def play_via_console():
    '''an early version of the game that is playable entirely through the console'''
    height, width = 12, 10
    snake = Snake(height, width)
    snake.print_board()

    # main action loop, choosing to do nothing repeats the action
    action = 0
    while True:
        # console input
        choice = input(': ')

        if 'l' in choice:
            action = 0
        elif 'd' in choice:
            action = 1
        elif 'r' in choice:
            action = 2
        elif 'u' in choice:
            action = 3

        # take an action and print the new board state to the console
        _, _, complete = snake.take_action(action)
        snake.print_board()

        if complete:
            return


def play_via_gui():
    height, width, seed = 12, 10, 73
    snake = Snake(height, width, seed)
    gui.run(snake)


if __name__ == '__main__':
    # play_via_console()
    play_via_gui()