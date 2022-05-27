import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from generate_canopy import generate_canopy
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable

sns.set_theme(style="darkgrid")


def plot_heatmap(data, x, y, title, **kwargs):
    fig: plt.Figure = plt.figure()
    ax = fig.gca()
    left = x.min()
    right = x.max()
    bottom = y.min()
    top = y.max()
    extent = [left, right, bottom, top]
    im = ax.imshow(
        data,
        cmap=cm.viridis,
        #   interpolation="bicubic",
        #   interpolation="gaussian",
        extent=extent,
        **kwargs
    )

    # create an axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes("right", size="5%", pad=0.05)

    plt.colorbar(
        im,
    )  # cax=cax)

    plt.title(title)
    # ax.matshow(data, cmap=cm.viridis, interpolation='bicubic', **kwargs)


def plot_surface(x, y, z, title, **kwargs):
    X, Y = np.meshgrid(x, y)
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    ax.plot_surface(X, Y, z, cmap=cm.viridis, linewidth=0, antialiased=False, **kwargs)
    plt.title(title)


def plot_generated_canopy(domain: np.ndarray):
    ds = generate_canopy(domain)

    plot_heatmap(ds.lai, x=ds.x, y=ds.y, title="Total Lai")
    plot_heatmap(ds.height, x=ds.x, y=ds.y, title="Height")
    plot_surface(x=ds.x, y=ds.y, z=ds.height, title="Height")
    plot_heatmap(ds.patch, x=ds.x, y=ds.y, title="Patch Type")
    plot_heatmap(ds.DBHc, x=ds.x, y=ds.y, title="Diameter at Breast Height")
    plt.show()
