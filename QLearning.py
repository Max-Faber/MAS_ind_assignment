from GridWorld import GridWorld
import operator, numpy as np

class SARSA:
    def __init__(self, gw: GridWorld, alpha: float, gamma: float, epsilon: float) -> None:
        self.gw: GridWorld = gw
        self.action_probability: float = 1.0 / len(self.gw.possible_actions)
        self.alpha: float = alpha
        self.gamma: float = gamma
        self.epsilon: float = epsilon
        self.Q_values: dict[tuple[int, int], dict[str, float]] = {}
        for c in self.gw.grid.keys():
            self.Q_values[c] = {
                a: 0.0 for a in list(self.gw.possible_actions.keys())
            }

    def get_epsilon_greedy_policy(self, s: tuple[int, int]) -> list[float]:
        n_actions: int = len(self.gw.possible_actions)
        # best_action: tuple[str, float] = self.gw.get_best_action(coordinates=s)
        best_action: str = max(self.Q_values[s].items(), key=operator.itemgetter(1))
        probabilities: list[float] = [1.0 * self.epsilon / n_actions for _ in range(n_actions)]

        probabilities[list(self.gw.possible_actions.keys()).index(best_action[0])] += (1.0 - self.epsilon)
        return probabilities

    def get_next_action(self, s: tuple[int, int]) -> str:
        greedy_policy: list[float] = self.get_epsilon_greedy_policy(s=s)
        return np.random.choice(list(self.gw.possible_actions.keys()), p=greedy_policy)

    def update_Q(self, s: tuple[int, int], a: str) -> tuple[tuple[int, int], int, bool, str]:
        step: tuple[tuple[int, int], int, bool] = self.gw.step(coordinates=s, action=a)
        new_s: tuple[int, int] = step[0]
        reward: int = step[1]
        terminate: bool = step[2]
        new_a: str = self.get_next_action(s=new_s)

        target = reward + self.gamma * self.Q_values[new_s][new_a]
        delta = target - self.Q_values[s][a]

        self.Q_values[s][a] = self.Q_values[s][a] + self.alpha * delta
        return new_s, reward, terminate, new_a
