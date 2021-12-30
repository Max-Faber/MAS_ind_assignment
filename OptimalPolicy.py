import random, operator, os
from SARSA import SARSA
from GridWorld import GridWorld
from Plot import Plot

def collect_two_dim_action_list(gw: GridWorld, sarsa: SARSA, action_lookup: dict[str, int]) -> list[list[int]]:
    two_dim_action_list: list[list[int]] = []

    for y in gw.possible_positions_axes:
        best_actions_row: list[int] = []

        for x in gw.possible_positions_axes:
            best_actions_row.append(action_lookup[max(sarsa.Q_values[(x, y)].items(), key=operator.itemgetter(1))[0]])
        two_dim_action_list.append(best_actions_row)
    return two_dim_action_list

if __name__ == '__main__':
    n_episodes: int = 100
    learning_rate: float = 0.6
    discount_factor: float = 1.0
    epsilon: float = 0.2
    gw: GridWorld = GridWorld()
    sarsa: SARSA = SARSA(gw=gw, learning_rate=learning_rate, discount_factor=discount_factor, epsilon=epsilon)
    floor_coordinates: list[tuple[int, int]] = [c for c in gw.grid.keys() if gw.grid[c].color == 'white']  # We can only start from the floor coordinates
    action_lookup: dict[str, int] = {
        'north': 0,
        'east': 1,
        'south': 2,
        'west': 3
    }

    if not os.path.exists('plots'):
        os.mkdir('plots')
    for _ in range(n_episodes):
        initial_coordinates: tuple[int, int] = random.choice(floor_coordinates)
        coordinates: tuple[int, int] = initial_coordinates

        print(f'Episode: {_ + 1}/{n_episodes}')
        while True:
            if gw.grid[coordinates].terminal:
                break
            action: str = sarsa.update_Q(s=coordinates)

            if not gw.is_valid_action(coordinates=coordinates, action=action):
                continue
            # Make transition to next state (or location in the grid)
            coordinates = (coordinates[0] + gw.possible_actions[action]['x_change'], coordinates[1] + gw.possible_actions[action]['y_change'])
            continue
    two_dim_action_list: list[list[int]] = collect_two_dim_action_list(gw=gw, sarsa=sarsa, action_lookup=action_lookup)
    Plot.heatmap(input_two_dim=two_dim_action_list, plt_path='plots/heatmap_sarsa.png')
