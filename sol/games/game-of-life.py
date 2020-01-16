import time
from os import system


class GameOfLife(object):
    char_alive = '█'
    char_dead = '░'
    char_horiz = '─'
    char_vert = '│'
    char_top_l = '┌'
    char_top_r = '┐'
    char_bot_l = '└'
    char_bot_r = '┘'

    def __init__(self, matrix_size, overflow=True):
        super().__init__()
        self._overflow = overflow
        self._matrix_size = matrix_size
        self._matrix = [x[:] for x in [[False] * matrix_size] * matrix_size]

    def __str__(self):
        lines = [self._str_line(i) for i in range(self._matrix_size)]
        return '\n'.join(self._box(lines))

    def _str_line(self, line_no):
        line_arr = [
            self.char_alive if x else self.char_dead for x in self._matrix[line_no]]
        return ''.join(line_arr)

    def _box(self, str_lines):
        top_bar = ''.join([self.char_top_l, self.char_horiz *
                           (self._matrix_size), self.char_top_r])
        bot_bar = ''.join([self.char_bot_l, self.char_horiz *
                           (self._matrix_size), self.char_bot_r])

        ret = []
        ret.append(top_bar)
        for line in str_lines:
            ret.append(''.join([self.char_vert, line, self.char_vert]))
        ret.append(bot_bar)

        return ret

    def _calc_cell(self, x, y):
        living_neighbors = sum([self.get_cell(i, j)
                                for i in range(x-1, x+2) for j in range(y-1, y+2)])
        if self.get_cell(x, y):
            # Alive
            living_neighbors -= 1
            if 2 <= living_neighbors <= 3:
                return True

            return False
        else:
            # Dead
            if living_neighbors == 3:
                return True

            return False

    def get_cell(self, x, y):
        if self._overflow:
            real_x = x % self._matrix_size
            real_y = y % self._matrix_size
            return self._matrix[real_y][real_x]

        if 0 <= x < self._matrix_size and 0 <= y < self._matrix_size:
            return self._matrix[y][x]

        return False

    def set_cell(self, x, y, is_alive):
        self._matrix[y][x] = is_alive

    def step(self, n=1):
        for i in range(n):
            new_matrix = [[self._calc_cell(x, y) for x in range(
                self._matrix_size)] for y in range(self._matrix_size)]
            self._matrix = new_matrix


ass = GameOfLife(40, overflow=True)

ass.set_cell(0, 5+1, True)
ass.set_cell(0, 5+2, True)
ass.set_cell(0, 5+3, True)
ass.set_cell(1, 5+0, True)
ass.set_cell(1, 5+3, True)
ass.set_cell(2, 5+3, True)
ass.set_cell(3, 5+3, True)
ass.set_cell(4, 5+0, True)
ass.set_cell(4, 5+2, True)

ass.set_cell(10+0, 10+1, True)
ass.set_cell(10+1, 10+1, True)
ass.set_cell(10+2, 10+0, True)
ass.set_cell(10+2, 10+2, True)
ass.set_cell(10+3, 10+1, True)
ass.set_cell(10+4, 10+1, True)
ass.set_cell(10+5, 10+1, True)
ass.set_cell(10+6, 10+1, True)
ass.set_cell(10+7, 10+0, True)
ass.set_cell(10+7, 10+2, True)
ass.set_cell(10+8, 10+1, True)
ass.set_cell(10+9, 10+1, True)

while True:
    ass.step()
    system('cls')
    print(ass)
