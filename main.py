from snake import Snake


def play_game():
    height, width, seed = 12, 10, 73
    snake = Snake(height, width, seed)
    snake.print_board()

    action = 0
    while True:
        choice = input(': ')

        if 'l' in choice:
            action = 0
        elif 'd' in choice:
            action = 1
        elif 'r' in choice:
            action = 2
        elif 'u' in choice:
            action = 3

        s, r, complete = snake.take_action(action)
        snake.print_board()

        if complete:
            return


def main():
    play_game()


if __name__ == '__main__':
    main()