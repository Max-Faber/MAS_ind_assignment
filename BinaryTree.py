from __future__ import annotations
import itertools, random, math

class Node:
    def __init__(self, address: list[str], parent: Node | None, depth: int=0) -> None:
        self.parent: Node | None = parent
        self.children: dict[str, Node | None] = {
            'left': None,
            'right': None
        }
        self.address: list[str] = address
        self.depth: int = depth
        self.mcts_info: dict[str, float] = {
            'value': 0,
            'n_visits': 0
        }

    def is_root_node(self) -> bool:
        return self.parent is None

    def is_leaf_node(self) -> bool:
        return self.children['left'] is None and self.children['right'] is None

class BinaryTree:
    def __init__(self, depth: int) -> None:
        assert depth >= 0, "depth must be greater or equal than zero"
        self.depth: int = depth
        self.root_node: Node = Node(address=[], parent=None)
        self.nodes: list[Node] = [self.root_node] # List containing all nodes, which makes it easy to iterate over them for whatever reason
        self.leaf_nodes: dict[Node, dict[str, float | None]] = {} # Node, { edit-distance (d), xi }
        self.highest_xi_node: Node | None = None
        self.A_t: Node | None = None
        self.n_nodes: int = (2 ** (self.depth + 1)) - 1
        self.created_nodes: int = 1
        self.generate()

    def get_node(self, address: list[str], create_node_if_not_exists: bool = False) -> Node | None:
        selected_node: Node = self.root_node
        current_address: list[str] = []

        for direction in address:
            current_address.append(direction)
            if (child := selected_node.children[direction]) is None:
                if not create_node_if_not_exists:
                    break
                child = selected_node.children[direction] = Node(address=current_address, parent=selected_node, depth=selected_node.depth + 1)
                self.nodes.append(child)
                if child.depth == self.depth:
                    self.leaf_nodes[child] = {
                        'd': None,
                        'xi': None
                    }
                self.created_nodes += 1
            selected_node = child
        return selected_node

    def pick_random_leaf_node(self) -> None:
        self.A_t = random.choice(list(self.leaf_nodes.keys()))

    @staticmethod
    def compute_edit_distance(A_i: Node, A_t: Node) -> int:
        n_direction_collisions = 0

        for direction_tuple in zip(A_i.address, A_t.address):
            n_direction_collisions += 1 if direction_tuple[0] != direction_tuple[1] else 0
        return n_direction_collisions

    def compute_xi(self, d: float) -> float:
        B: float = 1
        tau: float = 1
        xi: float = B * math.exp(-d / tau)
        assert xi > 0, "Value for xi should be non-negligible"
        return xi

    def generate(self) -> None:
        for d in range(1, self.depth + 1):
            for address in itertools.product(['left', 'right'], repeat=d):
                self.get_node(address=address, create_node_if_not_exists=True)
        assert self.created_nodes == self.n_nodes # If not something went wrong with generating the Binary Tree
        assert len(self.leaf_nodes) == 2 ** self.depth # We want our Binary Tree to be symmetric
        self.pick_random_leaf_node()
        for leaf_node in self.leaf_nodes:
            if self.highest_xi_node is None:
                self.highest_xi_node = leaf_node
            self.leaf_nodes[leaf_node]['d'] = self.compute_edit_distance(A_i=leaf_node, A_t=self.A_t)
            self.leaf_nodes[leaf_node]['xi'] = self.compute_xi(self.leaf_nodes[leaf_node]['d'])
            self.highest_xi_node = max([self.highest_xi_node, leaf_node], key=lambda x: self.leaf_nodes[x]['xi'])

    def get_visited_node_percentage(self) -> float:
        return (len([node for node in self.nodes if node.mcts_info['n_visits'] > 0]) / len(self.nodes)) * 100
