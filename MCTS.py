from __future__ import annotations
from BinaryTree import BinaryTree, Node
import math, random, os, statistics, matplotlib.pyplot as plt, numpy as np

class MCTS:
    def __init__(self, n_iterations: int, n_roll_outs: int, c_hyper_param: float, binary_tree: BinaryTree) -> None:
        self.n_iterations: int = n_iterations
        self.n_roll_outs: int = n_roll_outs
        self.c_hyper_param: float = c_hyper_param
        self.binary_tree: BinaryTree = binary_tree
        self.selected_node: Node = self.binary_tree.root_node
        self.visited_nodes: list[Node] = []

    def find_optimal_node(self) -> Node:
        root_node = self.selected_node

        for _ in range(self.n_iterations):
            # Select and expand
            while self.selected_node.mcts_info['n_visits'] > 0 and not self.selected_node.is_leaf_node():
                self.selected_node = self.get_max_UCB_child()
            for _ in range(self.n_roll_outs):
                # Rollout
                leaf_node = self.rollout()
                # Back-propagate
                self.back_propagate(starting_node=leaf_node)
            # Reset to root node
            self.selected_node = root_node
        while not self.selected_node.is_leaf_node():
            self.selected_node = max(list(self.selected_node.children.values()), key=lambda x: x.mcts_info['value'])
        # print(f'Selected path:\t{self.selected_node.address}\t(xi: {self.binary_tree.leaf_nodes[self.selected_node]["xi"]})')
        # print(f'Best path:\t{self.binary_tree.A_t.address}\t(xi: {self.binary_tree.leaf_nodes[self.binary_tree.A_t]["xi"]})')
        # print(f'Edit distance: {BinaryTree.compute_edit_distance(self.selected_node, self.binary_tree.A_t)}')
        return self.selected_node

    def calc_UCB_value(self, node: Node) -> float:
        parent_node = self.selected_node

        if node.mcts_info['n_visits'] == 0:
            return float('inf') # Un-explored nodes are prioritized
        return node.mcts_info['value'] + (self.c_hyper_param * math.sqrt(math.log(parent_node.mcts_info['n_visits'] / node.mcts_info['n_visits'])))

    def get_max_UCB_child(self) -> Node:
        children: list[Node] = list(self.selected_node.children.values())

        return max(children, key=self.calc_UCB_value)

    def rollout(self) -> Node:
        """Randomly walk the search tree until we reach a leaf node"""
        node: Node = self.selected_node

        while not node.is_leaf_node():
            node = random.choice(list(node.children.values()))
        return node

    def back_propagate(self, starting_node: Node) -> None:
        node: Node = starting_node
        value: float = self.binary_tree.leaf_nodes[node]['xi']

        while True:
            node.mcts_info['value'] += value
            node.mcts_info['n_visits'] += 1
            if node.is_root_node():
                break
            node = node.parent

def plot_results(data_group1: dict[str, list[float] | str], data_group2: dict[str, list[float]], labels: list[float], x_label: str) -> None:
    x: np.core.multiarray = np.arange(len(data_group1['means']))
    width: float = 0.35
    fig, ax = plt.subplots()
    ax.set_ylabel(data_group1['legend_label'], color=data_group1['color'])
    ax.set_xticks(x, labels)
    ax.set_xlabel(x_label)
    ax.yaxis.grid(True)
    ax.set_ylim([0, (max(data_group1['means']) + max(data_group1['st_devs'])) * 1.1])
    rects1 = ax.bar(x - width / 2, data_group1['means'], width, yerr=data_group1['st_devs'], label=data_group1['legend_label'], color=data_group1['color'], capsize=10)
    ax2 = ax.twinx()
    ax2.set_ylabel(data_group2['legend_label'], color=data_group2['color'])
    ax2.set_ylim([0, (max(data_group2['means']) + max(data_group2['st_devs'])) * 1.1])
    rects2 = ax2.bar(x + width / 2, data_group2['means'], width, yerr=data_group2['st_devs'], label=data_group2['legend_label'], color=data_group2['color'], capsize=10)
    plt.show()

if __name__ == '__main__':
    depth: int = 12
    n_iterations: int = 50
    n_roll_outs: int = 5
    n_rounds: int = 100
    c_hyper_params: list[float] = [0, 0.5, 1, 1.5, 2]
    plot_data_edit_distance: dict[str, list[float] | str] = {
        'means': [],
        'st_devs': [],
        'legend_label': 'Edit-distance',
        'color': 'blue'
    }
    plot_data_visited_node_percentage: dict[str, list[float] | str] = {
        'means': [],
        'st_devs': [],
        'legend_label': 'Mean visited nodes %',
        'color': 'orange'
    }

    if not os.path.exists('plots'):
        os.mkdir('plots')
    for c_hyper_param in c_hyper_params:
        edit_distances: list[float] = []
        visited_node_percentages: list[float] = []

        for _ in range(n_rounds):
            bt: BinaryTree = BinaryTree(depth=depth)
            mcts: MCTS = MCTS(n_iterations=n_iterations, n_roll_outs=n_roll_outs, c_hyper_param=c_hyper_param, binary_tree=bt)
            opt_node: Node = mcts.find_optimal_node()
            edit_distances.append(BinaryTree.compute_edit_distance(opt_node, bt.A_t))
            visited_node_percentages.append(bt.get_visited_node_percentage())
        plot_data_edit_distance['means'].append(sum(edit_distances) / len(edit_distances))
        plot_data_edit_distance['st_devs'].append(statistics.stdev(edit_distances))
        plot_data_visited_node_percentage['means'].append(sum(visited_node_percentages) / len(visited_node_percentages))
        plot_data_visited_node_percentage['st_devs'].append(statistics.stdev(visited_node_percentages))
    plot_results(data_group1=plot_data_edit_distance, data_group2=plot_data_visited_node_percentage, labels=c_hyper_params, x_label='c (Exploration-rate)')
