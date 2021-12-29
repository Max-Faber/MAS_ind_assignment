class GridCell:
    def __init__(self, reward: int, terminal: bool, accessible: bool, color: str) -> None:
        self.reward: int = reward
        self.terminal: bool = terminal
        self.accessible: bool = accessible
        self.color: str = color

class GridWorld:
    def __init__(self) -> None:
        # Dict key: tuple containing the grid coordinates (x, y), dict value: grid cell information (GridCell class)
        self.grid: dict[tuple[int, int], GridCell] = {
            # Row 1
            (1, 1): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (1, 2): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (1, 3): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (1, 4): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (1, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (1, 6): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (1, 7): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (1, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (1, 9): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            # Row 2
            (2, 1): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (2, 2): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (2, 3): GridCell(reward=-1,     terminal=False, accessible=False,   color='blue'),
            (2, 4): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (2, 5): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (2, 6): GridCell(reward=-1,     terminal=False, accessible=False,   color='blue'),
            (2, 7): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (2, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (2, 9): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            # Row 3
            (3, 1): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (3, 2): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (3, 3): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (3, 4): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (3, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (3, 6): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (3, 7): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (3, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (3, 9): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            # Row 4
            (4, 1): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (4, 2): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (4, 3): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (4, 4): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (4, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (4, 6): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (4, 7): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (4, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (4, 9): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            # Row 5
            (5, 1): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (5, 2): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (5, 3): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (5, 4): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (5, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (5, 6): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (5, 7): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (5, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (5, 9): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            # Row 6
            (6, 1): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (6, 2): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (6, 3): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (6, 4): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (6, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (6, 6): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (6, 7): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (6, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (6, 9): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            # Row 7
            (7, 1): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (7, 2): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (7, 3): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (7, 4): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (7, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (7, 6): GridCell(reward=-50,    terminal=True,  accessible=True,    color='red'),
            (7, 7): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (7, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (7, 9): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            # Row 8
            (8, 1): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (8, 2): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (8, 3): GridCell(reward=-1,     terminal=False, accessible=False,   color='blue'),
            (8, 4): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (8, 5): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (8, 6): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (8, 7): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (8, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (8, 9): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            # Row 9
            (9, 1): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (9, 2): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (9, 3): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (9, 4): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (9, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (9, 6): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'),
            (9, 7): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (9, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (9, 9): GridCell(reward=50,     terminal=True,  accessible=True,    color='green')
        }

if __name__ == '__main__':
    pass