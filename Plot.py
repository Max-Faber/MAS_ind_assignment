from __future__ import annotations
from matplotlib.lines import Line2D
from matplotlib import colors

import matplotlib.pyplot as plt, numpy as np

class Plot:
    @staticmethod
    def heatmap(input_two_dim: list[list[float]], plt_path: str, custom_labels: dict[str, str] = dict[str, str]) -> None:
        if len(custom_labels):
            legend_elements = []

            for label, color in custom_labels.items():
                legend_elements.append(Line2D([0], [0], color=color, lw=4, label=label))
            plt.legend(bbox_to_anchor=(1.3, 1.0), handles=legend_elements)
            cmap = colors.ListedColormap(['black', 'red', 'orange', 'white'])
            norm = colors.BoundaryNorm([0, 1, 2, 3], cmap.N)
            heatmap = plt.pcolor(input_two_dim, cmap=cmap, norm=norm)
            # plt.imshow(input_two_dim, cmap=cmap, norm=norm)
        else:
            plt.imshow(input_two_dim, cmap='hot', interpolation='nearest')
            plt.colorbar()
        plt.savefig(fname=plt_path)
        plt.show()

    @staticmethod
    def heatmap_q_values(q_values: list[list[int]], plt_path: str, ticks: list[int]):
        plt.xticks(ticks=np.arange(len(ticks)), labels=[str(t) for t in ticks])
        plt.yticks(ticks=np.arange(len(ticks)), labels=[str(t) for t in ticks])
        plt.imshow(q_values, cmap='coolwarm')
        for x in reversed(range(len(q_values))):
            for y in reversed(range(len(q_values))):
                if q_values[x][y] == 0: # north
                    plt.arrow(y, x, 0, -0.4, fill=False, head_width=0.1, length_includes_head=True)
                elif q_values[x][y] == 3: # east
                    plt.arrow(y, x, -0.4, 0, fill=False, head_width=0.1, length_includes_head=True)
                elif q_values[x][y] == 2: # south
                    plt.arrow(y, x, 0, 0.4, fill=False, head_width=0.1, length_includes_head=True)
                elif q_values[x][y] == 1: # west
                    plt.arrow(y, x, 0.4, 0, fill=False, head_width=0.1, length_includes_head=True)
        plt.savefig(fname=plt_path)
        plt.show()
