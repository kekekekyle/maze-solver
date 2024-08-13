import random
import time
from shapes import (
    Line,
    Point,
)

class Cell():
    def __init__(
        self,
        window=None,
        visited=False,
    ):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._window = window
        self.visited = visited

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            if self._window is not None:
                self._window.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            if self._window is not None:
                self._window.draw_line(line, fill_color="white")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            if self._window is not None:
                self._window.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            if self._window is not None:
                self._window.draw_line(line, fill_color="white")
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            if self._window is not None:
                self._window.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            if self._window is not None:
                self._window.draw_line(line, fill_color="white")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            if self._window is not None:
                self._window.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            if self._window is not None:
                self._window.draw_line(line, fill_color="white")

    def draw_move(self, to_cell, undo=False):
        from_point = Point(self._x1 + (self._x2 - self._x1) / 2, self._y1 + (self._y2 - self._y1) / 2)
        to_point = Point(to_cell._x1 + (to_cell._x2 - to_cell._x1) / 2, to_cell._y1 + (to_cell._y2 - to_cell._y1) / 2)
        line = Line(from_point, to_point)
        self._window.draw_line(line, "red" if undo is False else "gray")


class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        window=None,
        seed=None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self._create_cells()
        if seed is not None:
            random.seed(seed)

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_rows):
            self._cells.append([])
            for j in range(self.num_cols):
                cell = Cell(self.window)
                self._cells[i].append(cell)
                self._draw_cells(i, j)


    def _draw_cells(self, i, j):
        cell_x1 = self.x1 + (j * self.cell_size_x)
        cell_y1 = self.y1 + (i * self.cell_size_y)
        cell_x2 = self.x1 + ((j + 1) * self.cell_size_x)
        cell_y2 = self.y1 + ((i + 1) * self.cell_size_y)
        self._cells[i][j].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        if self.window is not None:
            self._animate()

    def _animate(self):
        if self.window is not None:
            self.window.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False
        self._draw_cells(0, 0)
        exit_cell = self._cells[self.num_rows - 1][self.num_cols - 1]
        exit_cell.has_bottom_wall = False
        self._draw_cells(self.num_rows - 1, self.num_cols - 1)

    def _break_walls_r(self, i, j):
        cell = self._cells[i][j]
        cell.visited = True
        while True:
            to_visit = []
            if i + 1 < self.num_rows and self._cells[i + 1][j].visited == False:
                to_visit.append("down") 
            if j + 1 < self.num_cols and self._cells[i][j + 1].visited == False:
                to_visit.append("right")
            if j - 1 >= 0 and self._cells[i][j - 1].visited == False:
                to_visit.append("left")
            if i - 1 >= 0 and self._cells[i - 1][j].visited == False:
                to_visit.append("up")
            if len(to_visit) == 0:
                self._cells[i][j].draw(
                    self.x1 + (j * self.cell_size_x),
                    self.y1 + (i * self.cell_size_y),
                    self.x1 + ((j + 1) * self.cell_size_x),
                    self.y1 + ((i + 1) * self.cell_size_y),
                )
                return
            else:
                next_cell = random.sample(to_visit, 1)[0]
                if next_cell == "down":
                    cell.has_bottom_wall = False
                    self._draw_cells(i, j)
                    self._cells[i + 1][j].has_top_wall = False
                    self._draw_cells(i + 1, j)
                    self._break_walls_r(i + 1, j)
                if next_cell == "right":
                    cell.has_right_wall = False
                    self._draw_cells(i, j)
                    self._cells[i][j + 1].has_left_wall = False
                    self._draw_cells(i, j + 1)
                    self._break_walls_r(i, j + 1)
                if next_cell == "left":
                    cell.has_left_wall = False
                    self._draw_cells(i, j)
                    self._cells[i][j - 1].has_right_wall = False
                    self._draw_cells(i, j - 1)
                    self._break_walls_r(i, j - 1)
                if next_cell == "up":
                    cell.has_top_wall = False
                    self._draw_cells(i, j)
                    self._cells[i - 1][j].has_bottom_wall = False
                    self._draw_cells(i - 1, j)
                    self._break_walls_r(i - 1, j)

    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        cell = self._cells[i][j]

        self._animate()
        cell.visited = True
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        for direction in [("down", i + 1, j), ("right", i, j + 1), ("left", i, j - 1), ("up", i - 1, j)]:
            if direction[1] >= 0 and direction[1] < self.num_rows and direction[2] >= 0 and direction[2] < self.num_cols:
                next_cell = self._cells[direction[1]][direction[2]]
                if next_cell.visited == False:
                    if (direction[0] == "down" and cell.has_bottom_wall == False and next_cell.has_top_wall == False) \
                    or (direction[0] == "right" and cell.has_right_wall == False and next_cell.has_left_wall == False) \
                    or (direction[0] == "left" and cell.has_left_wall == False and next_cell.has_right_wall == False) \
                    or (direction[0] == "up" and cell.has_top_wall == False and next_cell.has_bottom_wall == False): 
                        cell.draw_move(next_cell)
                        if self._solve_r(direction[1], direction[2]) == True:
                            return True
                        else:
                            cell.draw_move(next_cell, undo=True)

        return False
