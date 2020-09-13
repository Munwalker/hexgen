import math
import random
import numpy as np


class Heightmap:
    """
    Generate a heightmap using Diamond-square algorithm.
    :param params: generator parameters (used here : size, sea_percent, height_range, roughness)
    :return: True or False on success
    """

    def __init__(self, params, debug=False):
        self.params = params

        # start making the heightmap
        self.size = self.params.get('size')
        # get the grid (size*size) full of 0
        self.grid = np.zeros((self.size, self.size))

        # initialize corners of the world
        self.grid[0][0] = random.randint(0, 255)
        self.grid[self.size - 1][0] = random.randint(0, 255)
        self.grid[0][self.size - 1] = random.randint(0, 255)
        self.grid[self.size - 1][self.size - 1] = random.randint(0, 255)

        self._subdivide(0, 0, self.size - 1, self.size - 1)

        # compute average and record top height
        avg = []
        m = []
        for g in self.grid:
            m.append(max(g))
            avg.append(sum(g) / float(len(g)))

        self.highest_height = max(m)
        self.lowest_height = min(m)
        self.average_height = sum(avg) / float(len(avg))
        sea_percent = self.params.get('sea_percent')
        self.sealevel = round(self.average_height * (sea_percent * 2 / 100))

        if sea_percent == 100:
            self.sealevel = 255

        if debug:
            print(f"Sea level at {self.sealevel} or {sea_percent}")

    def height_at(self, x, y):
        return self.grid[x][y]

    def _adjust(self, xa, ya, x, y, xb, yb):
        """ fix the middle if the border
        xa;ya   -      ?x;y?      -       xb;yb
        """
        if self.grid[x][y] == 0:
            # d is the distance between the 2 known points.
            # the greater it is the more difference it can have from the height average of the 2 points.
            d = math.fabs(xa - xb) + math.fabs(ya - yb)
            roughness = self.params.get('roughness')
            # height = average of the 2 known points * random negative or positive * d * world roughness
            v = (self.grid[xa][ya] + self.grid[xb][yb]) / 2.0 \
                + (random.random() - 0.5) * d * roughness
            c = int(math.fabs(v) % 257)
            # Acceleration : avoid calculates twice
            if y == 0:
                self.grid[x][self.size - 1] = c
            if x == 0 or x == self.size - 1:
                if y < self.size - 1:
                    self.grid[x][self.size - 1 - y] = c
            range_low, range_high = self.params.get('height_range')
            if c < range_low:
                c = range_low
            elif c > range_high:
                c = range_high
            self.grid[x][y] = c

    def _subdivide(self, x1, y1, x2, y2):
        """ subdivide the heightmap iterate (diamond square algorithm)
        x1;y1   -       -       -       x2;y1
        -       -     ?x;y?     -       -
        x1;y2   -       -       -       x2;y2
        """
        # determinates coordinates of central point (x;y)
        if not ((x2 - x1 < 2.0) and (y2 - y1 < 2.0)):
            x = int((x1 + x2) / 2)
            y = int((y1 + y2) / 2)

            # average height of given points (x1;y1 / x1;y2 / x2;y1 / x2;y2)
            v = int((self.grid[x1][y1] + self.grid[x2][y1] +
                     self.grid[x2][y2] + self.grid[x1][y2]) / 4)
            range_low, range_high = self.params.get('height_range')
            if v < range_low:
                v = range_low
            elif v > range_high:
                v = range_high
            self.grid[x][y] = v

            # calculate height of the side
            # x1;y1   -      ?x;y1     -       x2;y1
            # ?x1;y    -      x;y      -       ?x2;y
            # x1;y2   -      ?x;y2     -       x2;y2
            self._adjust(x1, y1, x, y1, x2, y1)
            self._adjust(x2, y1, x2, y, x2, y2)
            self._adjust(x1, y2, x, y2, x2, y2)
            self._adjust(x1, y1, x1, y, x1, y2)

            # redo for smaller square
            self._subdivide(x1, y1, x, y)
            self._subdivide(x, y1, x2, y)
            self._subdivide(x, y, x2, y2)
            self._subdivide(x1, y, x, y2)
