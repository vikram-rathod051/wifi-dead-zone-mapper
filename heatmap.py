import matplotlib.pyplot as plt
import numpy as np


def create_heatmap(data):
    if data.empty:
        return None

    # Convert recorded locations into a 2D grid.
    grid = data.pivot_table(
        index="Y",
        columns="X",
        values="Signal (dBm)",
        aggfunc="mean"
    )

    if grid.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 5))

    image = ax.imshow(
        grid.values,
        origin="lower",
        cmap="RdYlGn",
        aspect="auto",
        vmin=-90,
        vmax=-30
    )

    ax.set_title("Wi-Fi Signal Strength Heatmap")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")

    ax.set_xticks(np.arange(len(grid.columns)))
    ax.set_xticklabels(grid.columns)

    ax.set_yticks(np.arange(len(grid.index)))
    ax.set_yticklabels(grid.index)

    colorbar = fig.colorbar(image, ax=ax)
    colorbar.set_label("Signal Strength (dBm)")

    fig.tight_layout()

    return fig