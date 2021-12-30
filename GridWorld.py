import random, numpy as np

class GridCell:
    def __init__(self, reward: int, terminal: bool, accessible: bool, color: str) -> None:
        self.reward: int = reward
        self.terminal: bool = terminal
        self.accessible: bool = accessible
        self.color: str = color

class GridWorld:
    def __init__(self) -> None:
        self.dimension = 9
        self.possible_positions_axes = list(np.arange(1, self.dimension + 1, 1))
        self.possible_actions: dict[str, dict[str, int]] = {
            'north': {
                'x_change': 0,
                'y_change': -1
            },
            'east': {
                'x_change': 1,
                'y_change': 0
            },
            'south': {
                'x_change': 0,
                'y_change': 1
            },
            'west': {
                'x_change': -1,
                'y_change': 0
            }
        }
        # Dict key: tuple containing the grid coordinates (x, y), dict value: grid cell information (GridCell class)
        self.grid: dict[tuple[int, int], GridCell] = {
            # Column 1
            (1, 1): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (1, 2): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (1, 3): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (1, 4): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (1, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (1, 6): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (1, 7): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (1, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (1, 9): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            # Column 2
            (2, 1): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (2, 2): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (2, 3): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (2, 4): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (2, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (2, 6): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (2, 7): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (2, 8): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (2, 9): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            # Column 3
            (3, 1): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (3, 2): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (3, 3): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (3, 4): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (3, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (3, 6): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (3, 7): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (3, 8): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (3, 9): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            # Column 4
            (4, 1): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (4, 2): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (4, 3): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (4, 4): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (4, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (4, 6): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (4, 7): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (4, 8): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (4, 9): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            # Column 5
            (5, 1): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (5, 2): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (5, 3): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (5, 4): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (5, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (5, 6): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (5, 7): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (5, 8): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (5, 9): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            # Column 6
            (6, 1): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (6, 2): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (6, 3): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (6, 4): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (6, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (6, 6): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (6, 7): GridCell(reward=-50,    terminal=True,  accessible=True,    color='red'),   (6, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (6, 9): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            # Column 7
            (7, 1): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (7, 2): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (7, 3): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),
            (7, 4): GridCell(reward=-1,     terminal=False, accessible=False,   color='blue'),  (7, 5): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),  (7, 6): GridCell(reward=-1, terminal=False, accessible=False,   color='blue'),
            (7, 7): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (7, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (7, 9): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            # Column 8
            (8, 1): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (8, 2): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (8, 3): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (8, 4): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (8, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (8, 6): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (8, 7): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (8, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (8, 9): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            # Column 9
            (9, 1): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (9, 2): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (9, 3): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (9, 4): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (9, 5): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (9, 6): GridCell(reward=-1, terminal=False, accessible=True,    color='white'),
            (9, 7): GridCell(reward=-1,     terminal=False, accessible=True,    color='white'), (9, 8): GridCell(reward=-1, terminal=False, accessible=True,    color='white'), (9, 9): GridCell(reward=50, terminal=True,  accessible=True,    color='green')
        }

    def is_valid_action(self, coordinates: tuple[int, int], action: str) -> bool:
        x: int = coordinates[0]
        y: int = coordinates[1]
        new_x: int = x + self.possible_actions[action]['x_change']
        new_y: int = y + self.possible_actions[action]['y_change']

        return 1 <= new_x <= self.dimension and 1 <= new_y <= self.dimension and (new_x in self.possible_positions_axes or new_y in self.possible_positions_axes) and \
               self.grid[(new_x, new_y)].accessible

    def get_possible_actions(self, coordinates: tuple[int, int]) -> list[tuple[str, float]]:
        possible_rewards: list[tuple[str, float]] = []
        x: int = coordinates[0]
        y: int = coordinates[1]

        for action in self.possible_actions:
            coordinate = (x + self.possible_actions[action]['x_change'], y + self.possible_actions[action]['y_change'])
            if not self.is_valid_action(coordinates=coordinate, action=action):
                coordinate = coordinates
            possible_rewards.append((action, self.grid[coordinate].reward))
        return possible_rewards

    # def get_best_action(self, coordinates: tuple[int, int]) -> tuple[str, float]:
    #     possible_rewards: list[tuple[str, float]] = self.get_possible_actions(coordinates=coordinates)
    #
    #     random.shuffle(possible_rewards) # We shuffle in order to prevent that the same is always selected when
    #     return max(possible_rewards, key=lambda x: x[1])
