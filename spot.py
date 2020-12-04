import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
  def __init__(self, row, col, width, total_rows):
    self.row = row
    self.col = col
    self.x = row * width
    self.y = col * width
    self.color = WHITE
    self.neighbors = []
    self.width = width
    self.total_rows = total_rows
    self.front = None
    self.front_pos = None

  def get_pos(self):
    return self.row, self.col

  def is_pit(self):
    return self.color == RED

  def is_gold(self):
    return self.color == GREEN

  def is_miner(self):
    return self.color == ORANGE

  def is_beacon(self):
    return self.color == TURQUOISE

  def is_neighbor(self):
    return self.color == BLACK

  def reset(self):
    self.color = WHITE

  def miner(self):
    self.color = ORANGE

  def pit(self):
    self.color = RED

  def gold(self):
    self.color = GREEN

  def beacon(self):
    self.color = TURQUOISE

  def neighbor(self):
    self.color = BLACK

  def get_front(self):
    return self.front
  
  def get_front_pos(self):
    return self.front_pos 

  def draw(self, win):
    pygame.draw.rect(win, self.color,(self.x, self.y, self.width, self.width))

  def update_neighbors(self, grid):
    self.neighbors = []
    if (self.row < self.total_rows - 1
        and not grid[self.row + 1][self.col].is_miner()):  # DOWN

      self.neighbors.append(grid[self.row + 1][self.col])
      grid[self.row + 1][self.col].neighbor()

    if self.row > 0 and not grid[self.row - 1][self.col].is_miner():  # UP

      self.neighbors.append(grid[self.row - 1][self.col])
      grid[self.row - 1][self.col].neighbor()

    if (self.col < self.total_rows - 1
            and not grid[self.row][self.col + 1].is_miner()):  # RIGHT

      self.neighbors.append(grid[self.row][self.col + 1])
      grid[self.row][self.col + 1].neighbor()

    if self.col > 0 and not grid[self.row][self.col -1].is_miner():  # LEFT

      self.neighbors.append(grid[self.row][self.col - 1])
      grid[self.row][self.col - 1].neighbor()

  def reset_neighbors(self):
    for neighbor in self.neighbors:
        neighbor.reset()

  def init_front(self, grid):
    self.front = grid[self.row + 1][self.col]
    self.front_pos = 'right'
    print(self.front_pos)
    self.front.neighbor()

  def rotate_front(self, grid):
    front_row, front_col = self.front.get_pos()
    try:
      if (self.col < self.total_rows - 1
          and self.row < self.total_rows - 1
          and self.right_front(grid).is_neighbor()):

        self.front.reset()
        self.front = self.bottom_front(grid)
        self.front_pos = 'bottom'
        self.front.neighbor()

      elif self.col > 0 and self.left_front(grid).is_neighbor():

        self.front.reset()
        self.front = self.top_front(grid)
        self.front_pos = 'top'
        self.front.neighbor()

      elif self.row > 0 and self.bottom_front(grid).is_neighbor():

        self.front.reset()
        self.front = self.left_front(grid)
        self.front_pos = 'left'
        self.front.neighbor()

      elif (self.row < self.total_rows - 1
            and self.top_front(grid).is_neighbor()):
        self.front.reset()
        self.front = self.right_front(grid)
        self.front_pos = 'right'
        self.front.neighbor()

    except IndexError:
        print("index error bitch")

  def update_front(self, grid):
    self.front.reset()
    if (self.row >= self.total_rows - 1 and 
          not (self.top_front(grid).is_neighbor() 
          or self.left_front(grid).is_neighbor())):

      self.front = self.bottom_front(grid)
    elif (self.col >= 0 and not(self.top_front(grid).is_neighbor())):
      self.front= self.right_front(grid)

    else:
      x, y = self.front.get_pos()
      if self.front_pos == 'right':
        self.front = self.right_front(grid)

      elif self.front_pos == 'left':
        self.front = self.left_front(grid)

      elif self.front_pos == 'bottom' :
        self.front = self.bottom_front(grid)

      elif self.front_pos == 'top' :
        self.front = self.top_front(grid)      

    self.front.neighbor()
  
  def top_front(self,grid):
    return grid[self.row][self.col - 1]

  def bottom_front(self,grid):
    return grid[self.row][self.col + 1]

  def right_front(self, grid):
    return grid[self.row + 1][self.col]

  def left_front(self, grid):
    return grid[self.row - 1][self.col]

