import anvil.facebook.auth
import anvil.server
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
        self.status = ''
        self.multiplier = 3

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
    def column_trues(self) -> list[bool]:
        trues = [False for _ in range(self.col_cnt)]
        for r in self.checked_matrix:
            for idx, c in enumerate(r):
                if c:
                    trues[idx] = True
        return trues

    @property
    def is_valid(self) -> bool:
        if not self.name:
            self.status = 'Please name your pay line.'
            return False
        # first two columns must have a tile
        if not (self.column_trues[0] and self.column_trues[1]):
            self.status = 'Your first two columns must have a title.'
            return False
        # all checked columns must be consecutive, therefore a False-True pair isn't valid
        pairs = [(c, self.column_trues[idx+1]) for idx, c in enumerate(self.column_trues) if idx < self.col_cnt-1]
        if (False, True) in pairs:
            self.status = "Don't leave any gaps between columns."
            return False
        self.status = 'submitted'
        return True

    @property
    def line_length(self) -> int:
        return max(idx for idx, value in enumerate(self.column_trues) if value) + 1

    @property
    def transposed_checked_matrix(self) -> list[list[bool]]:
        return [[row[i] for row in self.checked_matrix] for i in range(len(self.checked_matrix[0]))]

    @property
    def y_offsets(self) -> list[int]:
        return [r_idx for c_idx, col in enumerate(self.transposed_checked_matrix) if c_idx <= self.line_length - 1
                for r_idx, value in enumerate(col) if value]


tile_matrix: TileMatrix