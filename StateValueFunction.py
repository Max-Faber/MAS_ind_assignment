from GridWorld import GridWorld
from Plot import Plot
import random, os

class StateValueFunction:
    def __init__(self, gw: GridWorld, n_episodes: int) -> None:
        self.gw: GridWorld = gw
        self.n_episodes = n_episodes
        self.total_rewards: dict[tuple[int, int], list[int]] = {r: [] for r in self.gw.grid.keys()}

    def get_two_dim_mean_reward_list(self) -> list[list[float]]:
        two_dim_mean_reward_list: list[list[float]] = []

        for y in self.gw.possible_positions_axes:
            row: list[float] = []
            for x in self.gw.possible_positions_axes:
                coordinate = (x, y)

                row.append(sum(self.total_rewards[coordinate]) / len(self.total_rewards[coordinate]))
            two_dim_mean_reward_list.append(row)
        return two_dim_mean_reward_list

    def compute_state_value_function(self) -> None:
        for _ in range(self.n_episodes):
            if _ % 10 == 0:
                print(f'{_}/{self.n_episodes}')
            for start_position in self.gw.grid.keys():
                self.random_walk(coordinates=start_position)
        Plot.heatmap(input_two_dim=self.get_two_dim_mean_reward_list(), plt_path='plots/state_value_function_heatmap_MC.png')

    def random_walk(self, coordinates: tuple[int, int]) -> None:
        total_reward: int = 0
        actions: list[str] = list(self.gw.possible_actions.keys()) # Do this conversion once for efficiency
        starting_position: tuple[int, int] = coordinates

        while True:
            x: int = coordinates[0]
            y: int = coordinates[1]

            if self.gw.grid[coordinates].terminal:
                break
            action: str = random.choice(actions)
            if not x + self.gw.possible_actions[action]['x_change'] in self.gw.possible_positions_axes or not y + self.gw.possible_actions[action]['y_change'] in self.gw.possible_positions_axes or\
                not self.gw.grid[(x + self.gw.possible_actions[action]['x_change'], y + self.gw.possible_actions[action]['y_change'])].accessible:
                # We ran into a wall or grid-border
                total_reward -= 1
                continue
            # Make transition to next state (or location in the grid)
            coordinates = (x + self.gw.possible_actions[action]['x_change'], y + self.gw.possible_actions[action]['y_change'])
            # Add reward of the latest transition
            total_reward += self.gw.grid[coordinates].reward
        self.total_rewards[starting_position].append(total_reward)

if __name__ == '__main__':
    n_episodes: int = 5000
    gw: GridWorld = GridWorld()
    svf: StateValueFunction = StateValueFunction(gw=gw, n_episodes=n_episodes)

    if not os.path.exists('plots'):
        os.mkdir('plots')
    svf.compute_state_value_function()
