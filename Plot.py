from __future__ import annotations

import matplotlib.pyplot as plt

class Plot:
    @staticmethod
    def heatmap(input_two_dim: list[list[float]], plt_path: str) -> None:
        plt.imshow(input_two_dim, cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.savefig(fname=plt_path)
        plt.show()
    #
    # @staticmethod
    # def heatmap(input_two_dim: list[list[str]], labels: dict[str, int], plt_path: str):
    #     input_two_dim_int: list[list[int]] = []
    #
    #     for x in range(len(input_two_dim)):
    #         row: list[int] = []
    #
    #         for y in range(len(input_two_dim)):
    #             row.append(labels[input_two_dim[x, y]])
