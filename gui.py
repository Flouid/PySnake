import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import QRect, QPoint
from PyQt5.Qt import Qt

class SnakeUI(QWidget):
    # sets the default color scheme for the app
    tile_colors = ['#333333', '#bbbbbb', '#90ee90']

    # magic constants for action mapping
    __LEFT = 0
    __DOWN = 1
    __RIGHT = 2
    __UP = 3

    # configurable parameters for how to render the game
    tile_size = 36                  # width and height of a tile in pixels
    refresh_rate = 1/10             # the number of times the scene updates per second

    def __init__(self, env) -> None:
        # store the environment for playing snake
        self.__env = env
        # initialize the agent as moving left
        self.__action = self.__LEFT

        # use the environment to calculate some details for rendering the board
        self.height = self.tile_size * env.height
        self.width = self.tile_size * env.width

        # call the parent constructor for a qwidget
        super(SnakeUI, self).__init__()
        # lock in a size for the window and give it a nice name
        self.resize(self.height, self.width)
        self.setWindowTitle('PySnake')

        # create an empty layout and set it as the default
        layout = QVBoxLayout()
        self.setLayout(layout)

        # create the background 
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(QColor(self.tile_colors[0]))


    def paintEvent(self, _) -> None:
        '''handle updating the screen'''
        # initialize the painter and draw the background
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pix)

        # draw the board to the screen
        self.__draw_board(painter)

    def __draw_board(self, painter) -> None:
        '''draw the board using the painter'''
        # get a copy of the board from the environment
        board = self.__env.board
        for r in range(self.__env.height):
            y = self.tile_size * r                         # height offset
            for c in range(self.__env.width):
                x = self.tile_size * c                     # width offset
                # only continue if there is something to draw in this tile
                if board[r, c] == 0:
                    continue

                # create a rectangle for the tile
                rect = QRect(x, y, self.tile_size, self.tile_size)
                # the coloring of the tile can be determined by indexing the color list with the value
                color = QColor(self.tile_colors[board[r, c]])
                # draw the tile
                painter.fillRect(rect.normalized(), color)

    def keyPressEvent(self, event) -> None:
        '''handle input from the keyboard'''
        key = event.key()
        # map the keypress to an action
        if key == Qt.Key_A:
            self.__action = self.__LEFT
        elif key == Qt.Key_S:
            self.__action = self.__DOWN
        elif key == Qt.Key_D:
            self.__action = self.__RIGHT
        elif key == Qt.Key_W:
            self.__action = self.__UP
        else:
            # if the user didn't press a valid key then don't refresh
            return

        # take the action
        _, _, complete = self.__env.take_action(self.__action)
        # terminate if the game is complete 
        if complete:
            sys.exit(0)

        # update the frame
        self.update()


def run(env):
    '''driver code for actually running the ui'''
    app = QApplication(sys.argv)
    ui = SnakeUI(env)
    ui.show()
    sys.exit(app.exec_())
