from window import Window
from nodes import (
    Maze
)

if __name__ == "__main__":
    # cell_1 = Cell(win)
    # cell_2 = Cell(win)
    # cell_1.draw(100, 100, 200, 200)
    # cell_2.draw(300, 300, 400, 400)
    # cell_1.draw_move(cell_2)
    num_rows = 12
    num_cols = 15
    win = Window(800, 600)
    m1 = Maze(2, 2, num_rows, num_cols, 50, 50, win)
    m1._break_entrance_and_exit()
    m1._break_walls_r(0, 0)
    m1._reset_cells_visited()
    m1.solve()
    win.wait_for_close()
