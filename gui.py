import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import QRect, QPoint

class SnakeUI(QWidget):
    # sets the default color scheme for the app
    tile_colors = ['#333333', '#bbbbbb', '#90ee90']

    # configurable parameters for how to render the game
    tile_size = 36                  # width and height of a tile in pixels

    def __init__(self, env):
        # store the environment for playing snake
        self.__env = env

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


    def paintEvent(self, _):
        """Draws each layer of the board one after another every update"""
        # initialize the painter and draw the background
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pix)

        # draw the board to the screen
        self.__draw_board(painter)

    def __draw_board(self, painter):
        """Draw the board using the painter"""
        # get a copy of the board from the environment
        board = self.__env.board
        for r in range(self.__env.height):
            x = self.tile_size * r                         # height offset
            for c in range(self.__env.width):
                y = self.tile_size * c                     # width offset
                # only continue if there is something to draw in this tile
                if board[r, c] == 0:
                    continue

                # create a rectangle for the tile
                rect = QRect(x, y, self.tile_size, self.tile_size)
                # the coloring of the tile can be determined by indexing the color list with the value
                color = QColor(self.tile_colors[board[r, c]])
                # draw the tile
                painter.fillRect(rect.normalized(), color)

def run(env):
    '''driver code for actually running the ui'''
    app = QApplication(sys.argv)
    ui = SnakeUI(env)
    ui.show()
    sys.exit(app.exec_())