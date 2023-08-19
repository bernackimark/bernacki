class Tile:
    def __init__(self):
        self.is_checked: bool = False

    def switch_checked(self):
        self.is_checked = not self.is_checked

    @property
    def img(self):
        return '_/theme/maroon_tile.png' if self.is_checked else '_/theme/gold_tile.png'


class TileMatrix:
    rows = ['A', 'B', 'C', 'D', 'E']
    cols = [1, 2, 3, 4, 5]

    def __init__(self, row_cnt: int, col_cnt: int):
        self.name = ''
        self.row_cnt = row_cnt
        self.col_cnt = col_cnt
        self.tiles: list[list[Tile]] = [[Tile() for c in TileMatrix.cols if c-1 <= self.col_cnt]
                                        for r_idx, _ in enumerate(TileMatrix.rows) if r_idx <= self.row_cnt-1]

    def __iter__(self):
        return iter(self.tiles)

    def click_tile(self, row, col):
        # this can probably be simplified using the checked_matrix property
        current_col: list[bool] = [t.is_checked for r_idx, tiles in enumerate(self)
                                   if r_idx != row
                                   for c_idx, t in enumerate(tiles) if c_idx == col]
        if any(current_col):
            return
        self.tiles[row][col].switch_checked()

    @property
    def checked_matrix(self) -> [list[list[bool]]]:
        return [[t.is_checked for c_idx, t in enumerate(tiles)] for r_idx, tiles in enumerate(self)]

    @property
    def is_legitimate_shape(self) -> bool:
        # first two columns must have a tile
        # all checked columns must be consecutive
        
        return NotImplementedError
    
        # CODE THESE RULES NEXT



tile_matrix: TileMatrix