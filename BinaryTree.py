from __future__ import annotations
import itertools, random
import math


class Node:
    def __init__(self, address: list[str], depth: int=0) -> None:
        self.children: dict[str, Node | None] = {
            'left': None,
            'right': None
        }
        self.address: list[str] = address
        self.depth: int = depth

class BinaryTree:
    def __init__(self, depth: int) -> None:
        assert depth >= 0, "depth must be greater or equal than zero"
        self.depth: int = depth
        self.root_node: Node = Node(address=[])
        self.leaf_nodes: dict[Node, dict[str, float | None]] = {} # Node, { edit-distance (d), xi }
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
                child = selected_node.children[direction] = Node(address=current_address, depth=selected_node.depth + 1)
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
        B: float = 2
        t: float = 1
        xi: float = B * math.exp(-d / t)
        return xi

    def generate(self) -> None:
        for d in range(1, self.depth + 1):
            for address in itertools.product(['left', 'right'], repeat=d):
                self.get_node(address=address, create_node_if_not_exists=True)
        assert self.created_nodes == self.n_nodes # If not something went wrong with generating the Binary Tree
        assert len(self.leaf_nodes) == 2 ** self.depth # We want our Binary Tree to be symmetric
        self.pick_random_leaf_node()
        for leaf_node in self.leaf_nodes:
            self.leaf_nodes[leaf_node]['d'] = self.compute_edit_distance(A_i=leaf_node, A_t=self.A_t)
            self.leaf_nodes[leaf_node]['xi'] = self.compute_xi(self.leaf_nodes[leaf_node]['d'])
