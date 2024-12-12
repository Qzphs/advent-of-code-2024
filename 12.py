from sys import stdin


def neighbours(i: int, j: int):
    """Return the four neighbours of (`i`, `j`)."""
    return [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]


class Region:

    def __init__(self, plant: str, height: int, width: int):
        self.plant = plant
        self.height = height
        self.width = width
        self.plots: set[tuple[int, int]] = set()
        self.frontier: set[tuple[int, int]] = set()

    def add(self, i: int, j: int):
        """
        Add (`i`, `j`) as a plot to this region.

        Also update the frontier with any new neighbouring plots.
        """
        self.frontier.discard((i, j))
        self.plots.add((i, j))
        for ni, nj in neighbours(i, j):
            if not 0 <= ni < self.height:
                continue
            if not 0 <= nj < self.width:
                continue
            if (ni, nj) in self.plots:
                continue
            self.frontier.add((ni, nj))

    def price(self):
        """Return the price of this region."""
        return self.area() * self.perimeter()

    def area(self):
        """Return the area of this region."""
        return len(self.plots)

    def perimeter(self):
        """Return the perimeter of this region."""
        return sum(
            sum(neighbour not in self.plots for neighbour in neighbours(i, j))
            for i, j in self.plots
        )


class Garden:

    def __init__(self, plots: list[str]):
        self.plots = plots
        self.height = len(plots)
        self.width = len(plots[0])

    @classmethod
    def from_input(cls, data: str):
        return Garden(data.splitlines())

    def plant(self, i: int, j: int):
        """
        Return the plant at (`i`, `j`).

        If (`i`, `j`) are invalid coordinates, return the empty string
        ('') instead.
        """
        if not 0 <= i < self.height:
            return ""
        if not 0 <= j < self.width:
            return ""
        return self.plots[i][j]

    def regions(self):
        """Find and return a list of all regions in the garden."""
        regions: list[Region] = []
        missing = {
            (i, j) for i in range(self.height) for j in range(self.width)
        }
        while missing:
            # Find another region ###############
            si, sj = missing.pop()
            region = Region(self.plant(si, sj), self.height, self.width)
            region.add(si, sj)
            while region.frontier:
                i, j = region.frontier.pop()
                if self.plant(i, j) != region.plant:
                    continue
                missing.remove((i, j))
                region.add(i, j)
            #####################################
            regions.append(region)
        return regions


garden = Garden.from_input(stdin.read())
print(sum(region.price() for region in garden.regions()))
