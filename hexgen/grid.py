import math
import numpy as np
from hexgen.heightmap import Heightmap
from hexgen.hex import Hex


class GridBoundsException(Exception):
    pass


class Grid:
    """
    Generate a Grid.
    :param heightmap: heightmap of the world
    :param params: generator parameters (used here : size)
    :return: True or False on success
    """

    def __init__(self, heightmap: Heightmap, params, debug=False):
        self.params = params
        self.sealevel = heightmap.sealevel
        self.average_height = heightmap.average_height
        self.highest_height = heightmap.highest_height
        self.lowest_height = heightmap.lowest_height

        self.avg_altitude = 0
        self.num_ocean_hexes = 0

        self.hexes = []
        self.coldest_hexes = []

        if debug:
            print("Making grid")

        # creating the empty grid, then create each tile (Hex)
        self.grid = np.ndarray((heightmap.size, heightmap.size), dtype=np.object)
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                self.grid[x][y] = Hex(self, x, y, heightmap.height_at(x, y))
                if self.grid[x][y].is_water:
                    self.num_ocean_hexes += 1

        self.calculate()

    @property
    def size(self):
        return self.params.get('size')

    def find_hex(self, x, y):
        """ Finds a hex and a x and y coordinate """
        try:
            return self.grid[x][y]
        except IndexError:
            raise GridBoundsException("Invalid coordinates {}, {}".format(x, y))

    def calculate(self):
        """ run through the grid, calculate the edges"""
        alt = 0
        hexes = []
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                self.grid[x][y].calculate()
                alt += self.grid[x][y].altitude
                hexes.append(self.grid[x][y])
        self.avg_altitude = round(alt / math.pow(self.size, 2))

        # sort all tiles by temperature, copy 10% coldest to array coldest_hexes
        self.hexes = sorted(hexes, key=lambda x: x.temperature)
        number = round(len(self.hexes) * 0.10)
        self.coldest_hexes = self.hexes[:number]
