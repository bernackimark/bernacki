class Tile:
    def __init__(self):
        self.is_checked: bool = False

    def click_tile(self):
        print('I was clicked')
        self.is_checked = not self.is_checked

    @property
    def img(self):
        return '_/theme/maroon_tile.png' if self.is_checked else '_/theme/gold_tile.png'


class TileMatrix:
    rows = ['A', 'B', 'C', 'D', 'E']
    cols = [1, 2, 3, 4, 5]

    def __init__(self, row_cnt: int, col_cnt: int):
        self.row_cnt = row_cnt
        self.col_cnt = col_cnt
        self.tiles: list[list[Tile]] = [[Tile() for idx, c in enumerate(TileMatrix.cols) if idx <= self.col_cnt-1]
                                        for idx, r in enumerate(TileMatrix.rows) if idx <= self.row_cnt-1]

    def __iter__(self):
        return iter(self.tiles)