from __future__ import annotations

import random, operator, os, numpy as np
from SARSA import SARSA
from GridWorld import GridWorld
from Plot import Plot

def collect_two_dim_action_list(gw: GridWorld, sarsa: SARSA, action_lookup: dict[str, int], floor_coordinates: list[tuple[int, int]]) -> tuple[list[list[int]], list[list[float | np.nan]]]:
    two_dim_action_list: list[list[int]] = []
    two_dim_Q_list: list[list[float | np.nan]] = []

    for y in gw.possible_positions_axes:
        best_actions_row: list[int] = []
        best_Q_row: list[float | np.nan] = []

        for x in gw.possible_positions_axes:
            if not (x, y) in floor_coordinates:
                best_actions_row.append(-1)
                best_Q_row.append(np.nan)
                continue
            best_actions_row.append(action_lookup[max(sarsa.Q_values[(x, y)].items(), key=operator.itemgetter(1))[0]])
            best_Q_row.append(max(sarsa.Q_values[(x, y)].values()))
        two_dim_action_list.append(best_actions_row)
        two_dim_Q_list.append(best_Q_row)
    return two_dim_action_list, two_dim_Q_list

if __name__ == '__main__':
    n_episodes: int = 1000
    alpha: float = 0.1 # Learning rate
    gamma: float = 1
    epsilon: float = 0.1
    strategy: str = 'SARSA'
    # strategy: str = 'Q-Learning'
    gw: GridWorld = GridWorld()
    sarsa: SARSA = SARSA(gw=gw, alpha=alpha, gamma=gamma, epsilon=epsilon)
    floor_coordinates: list[tuple[int, int]] = [c for c in gw.grid.keys() if gw.grid[c].color == 'white']  # We can only start from the floor coordinates
    action_lookup: dict[str, int] = {
        'north': 0,
        'east': 1,
        'south': 2,
        'west': 3
    }

    if not os.path.exists('plots'):
        os.mkdir('plots')
    for episode in range(n_episodes):
        coordinates: tuple[int, int] = random.choice(floor_coordinates)
        action: str = sarsa.get_next_action(s=coordinates)

        print(f'Episode: {episode + 1}/{n_episodes}')
        while True:
            step: tuple[tuple[int, int], int, bool, str] = sarsa.update_Q(s=coordinates, a=action, strategy=strategy)
            coordinates: tuple[int, int] = step[0]
            reward: int = step[1]
            terminate: bool = step[2]
            action: str = step[3]

            if terminate:
                break

    grids: tuple[list[list[int]], list[list[float | np.nan]]] = collect_two_dim_action_list(gw=gw, sarsa=sarsa, action_lookup=action_lookup, floor_coordinates=floor_coordinates)
    two_dim_action_list: list[list[int]] = grids[0]
    two_dim_Q_list: list[list[float | np.nan]] = grids[1]
    Plot.heatmap_q_values(directions=two_dim_action_list, q_values=two_dim_Q_list, plt_path=f'plots/heatmap_{strategy}.png', ticks=gw.possible_positions_axes)
