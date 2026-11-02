"""
Maze module
"""


class Cell:
    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """Initializes the cell at (x,y), surrounded by walls.

        Args:
            x (int): horizontal coordinate
            y (int): vertical coordinate

        """
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def has_all_walls(self):
        """Checks if cell have all the walls.

        Returns:
            bool: True if cell have all the walls, False otherwise.

        """
        return all(self.walls.values())

    def break_wall(self, other, direction):
        """Breaks down the wall between cells (self and other).

        Args:
            other (str): cell object
            direction (str): navigation direction (N,S,E,W)

        """
        self.walls[direction] = False
        other.walls[Cell.wall_pairs[direction]] = False


class Maze:
    # A maze compass used for navigation between cells
    compass = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}

    def __init__(self, nx, ny):
        """Initializes the maze grid, consists of (nx,ny) cells.

        Args:
            nx (int): number of lines
            ny (int): number of columns

        """
        self.nx, self.ny = nx, ny
        self.maze_cells = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    def cell_at(self, x, y):
        """Gets the cell object at (x,y) coordinates.

        Args:
            x (int): horizontal coordinate
            y (int): vertical coordinate

        Returns:
            Cell: cell object at (x,y) coordinates.

        """
        return self.maze_cells[x][y]

    def find_valid_neighbours(self, cell):
        """Gets a list of unvisited neighbors to the cell.

        Args:
            cell (Cell): cell object

        Returns:
            list: a list of unvisited neighbours

        """
        neighbours = []

        for direction, (dx, dy) in Maze.compass.items():
            x2, y2 = cell.x + dx, cell.y + dy
            if 0 <= x2 < self.nx and 0 <= y2 < self.ny:
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours
