from GridWorld import GridWorld, GridCell
import operator, numpy as np

class SARSA:
    def __init__(self, gw: GridWorld, learning_rate: float, discount_factor: float, epsilon: float) -> None:
        self.gw: GridWorld = gw
        self.action_probability: float = 1.0 / len(self.gw.possible_actions)
        self.learning_rate: float = learning_rate
        self.discount_factor: float = discount_factor
        self.epsilon: float = epsilon
        self.Q_values: dict[tuple[int, int], dict[str, float]] = {}
        for c in self.gw.grid.keys():
            self.Q_values[c] = {
                a: 0.0 for a in list(self.gw.possible_actions.keys())
            }

    def get_weighted_mean(self, s: tuple[int, int], greedy_policy: list[float]) -> float:
        weighted_mean: float = 0.0

        actions: list[tuple[str, float]] = self.gw.get_possible_actions(coordinates=s)
        for action, probability in zip(actions, greedy_policy):
            weighted_mean += action[1] * probability

        return weighted_mean

    def get_epsilon_greedy_policy(self, s: tuple[int, int]) -> list[float]:
        n_actions: int = len(self.gw.possible_actions)
        # best_action: tuple[str, float] = self.gw.get_best_action(coordinates=s)
        best_action: str = max(self.Q_values[s].items(), key=operator.itemgetter(1))
        probabilities: list[float] = [1.0 * self.epsilon / n_actions for _ in range(n_actions)]

        probabilities[list(self.gw.possible_actions.keys()).index(best_action[0])] += (1.0 - self.epsilon)
        return probabilities


    def get_next_action(self, greedy_policy: list[float]) -> str:
        return np.random.choice(list(self.gw.possible_actions.keys()), p=greedy_policy)

    def update_Q(self, s: tuple[int, int]) -> str:
        greedy_policy: list[float] = self.get_epsilon_greedy_policy(s=s)
        next_action: str = self.get_next_action(greedy_policy=greedy_policy)

        self.Q_values[s][next_action] += self.learning_rate * (self.gw.grid[s].reward + self.discount_factor * self.get_weighted_mean(s=s, greedy_policy=greedy_policy) - self.Q_values[s][next_action])
        return next_action
