import numpy as np
import hashlib

class Snake:
    '''a class for providing an environment to play the game snake.
    It stresses a performant and scalable implementation that provides methods for an agent to play.
    An optional seed parameter allows particular random conditions to be repeated if desired'''
    # configurable parameters defining the behavior of the game
    __MIN_SIZE = 10             # the minimum dimensions of the board
    __MIN_EDGE = 2              # the minimum distance from the edge to spawn food
    __JITTER = 2                # max distance from the center to start
    __START_LEN = 1             # the starting length of the snake

    # magic constants for encoding what occupies a given tile as an integer
    __SNAKE = 1
    __FOOD = 2

    # magic constants for encoding the mapping from action to integer
    __LEFT = 0
    __DOWN = 1
    __RIGHT = 2
    __UP = 3

    def __init__(self, height: int, width: int, seed: int = 0) -> None:
        # assert the minimum size requirement
        assert(height >= self.__MIN_SIZE and width >= self.__MIN_SIZE)
        # if an rng seed was provided, use it
        if seed:
            np.random.seed(seed)
        # initialize the board as a 2d numpy array
        self.__board = np.zeros((height, width), dtype=np.uint8)
        self.__height, self.__width = height, width
        # calculate the starting position for the snake as a random point near the middle of the board
        start_r = height // 2 + np.random.randint(-self.__JITTER, self.__JITTER + 1)
        start_c = width // 2 + np.random.randint(-self.__JITTER, self.__JITTER + 1)
        # store the snake itself as a list of coordinate pairs, starting from the tail
        self.__snake = [(start_r, start_c)] * self.__START_LEN

        # mark the starting point as occupied on the board by a snake
        self.__board[start_r, start_c] = self.__SNAKE
        # spawn the first piece of food
        self.__spawn_food()

        # the entire state of the game needs to be uniquely mapped into an integer from 0 to the number of states
        # this is a surprisingly hard problem, here it's done by considering two things:
        #   - board state, there are 3*r*c possible values since there are three possible values at each tile
        #   - snake head position, there are r*c unique indices to choose from
        # concluding, the state space should have 3*r^2*c^2 possible values
        self.n_states = 3 * height ** 2 * width ** 2
        self.n_actions = 4

    def print_board(self) -> None:
        '''a simple helper function to provide a debugging output for the board'''
        for r in range(self.__height):
            for c in range(self.__width):
                print(f'{self.__board[r, c]}', end=' ')
            print(end='\n')

    def __spawn_food(self) -> None:
        '''a helper function to find an unoccupied space on the board and mark it as having food'''
        # repeatedly sample points from the board until one is unoccupied and spawn food there
        while True:
            # do not spawn food too close to an edge
            r = np.random.randint(self.__MIN_EDGE, self.__height - self.__MIN_EDGE)
            c = np.random.randint(self.__MIN_EDGE, self.__width - self.__MIN_EDGE)
            # check that the randomly selected tile is empty
            if not self.__board[r, c]:
                # mark the tile as containing food
                self.__board[r, c] = self.__FOOD
                return

    def take_action(self, action) -> int and int and bool:
        '''a public method for taking an action. 
        Modelled after the openai gym, it takes one parameter:
            - an integer encoding an action to take during the time step    (0 to 3)
        It returns three values:
            - an integer uniquely encoding the state of the game            (-1)
            - an integer encoding the reward that was earned for an action  (0 to 1)
            - a bool encoding whether or not the game concluded'''
        # calculate the new position of the head of the snake based on the action
        head_r, head_c = self.__snake[-1]
        if action == self.__LEFT: 
            r, c = head_r, head_c - 1
        elif action == self.__DOWN:
            r, c = head_r + 1, head_c
        elif action == self.__RIGHT:
            r, c = head_r, head_c + 1
        elif action == self.__UP:
            r, c = head_r - 1, head_c
        
        # check to see if the snake hit a wall and stop the game
        if r >= self.__height or r < 0 or c >= self.__height or c < 0:
            return -1, 0, True
        # check to see if the snake hit itself and stop the game
        if self.__board[r, c] == self.__SNAKE:
            return -1, 0, True
        # calculate reward using a check that the snake hit food
        if self.__board[r, c] == self.__FOOD:
            reward = 1
        else:
            reward = 0

        # move the head of the snake to the new position
        self.__snake.append((r, c))
        self.__board[r, c] = self.__SNAKE
        # if the snake did not find food, move the tail
        if not reward:
            tail_r, tail_c = self.__snake.pop(0)
            self.__board[tail_r, tail_c] = 0
        # if it did, spawn a new piece elsewhere
        else:
            self.__spawn_food()

        # use a hash and the linear index of the head along with a modulus to create the state mapping
        state_map = int.from_bytes(hashlib.md5(self.__board.tostring()).digest(), 'little')
        state = ((r * self.__width + c) * state_map) % self.n_states
        
        return state, r, False
        

        