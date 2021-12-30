import random, operator, os
from SARSA import SARSA
from GridWorld import GridWorld
from Plot import Plot

def collect_two_dim_action_list(gw: GridWorld, sarsa: SARSA, action_lookup: dict[str, int], floor_coordinates: list[tuple[int, int]]) -> list[list[int]]:
    two_dim_action_list: list[list[int]] = []

    for y in gw.possible_positions_axes:
        best_actions_row: list[int] = []

        for x in gw.possible_positions_axes:
            if not (x, y) in floor_coordinates:
                best_actions_row.append(-1)
                continue
            best_actions_row.append(action_lookup[max(sarsa.Q_values[(x, y)].items(), key=operator.itemgetter(1))[0]])
        two_dim_action_list.append(best_actions_row)
    return two_dim_action_list

if __name__ == '__main__':
    n_episodes: int = 10000
    alpha: float = 0.2
    gamma: float = 0.9
    epsilon: float = 0.4
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
            step: tuple[tuple[int, int], int, bool, str] = sarsa.update_Q(s=coordinates, a=action)
            coordinates: tuple[int, int] = step[0]
            reward: int = step[1]
            terminate: bool = step[2]
            action: str = step[3]

            if terminate:
                break

    two_dim_action_list: list[list[int]] = collect_two_dim_action_list(gw=gw, sarsa=sarsa, action_lookup=action_lookup, floor_coordinates=floor_coordinates)
    Plot.heatmap_q_values(q_values=two_dim_action_list, plt_path='plots/heatmap_sarsa.png', ticks=gw.possible_positions_axes)
