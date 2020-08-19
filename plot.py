import matplotlib.pyplot as plt
import numpy as np
from tikzplotlib import save

def plot_4(matrix, matrix_var, titles, sup_title):

    fig, axs = plt.subplots(2,2, figsize=(14,9))

    _min = np.min(matrix[0:2])
    _max = np.max(matrix[0:2])
    
    for col in range(2):
        if col == 0:
            ma = matrix[:2]
            ma_var = matrix_var[:2]
            title = titles[:2]
        else:
            ma = matrix[2:]
            ma_var = matrix_var[2:]
            title = titles[2:]
        
        for row in range(2):
            ax = axs[row, col]
            if col == 0:
                im = ax.imshow(ma[row], interpolation='spline36', origin="lower",  vmin = _min, vmax = _max)
            else:
                im = ax.imshow(ma[row], interpolation='spline36', origin="lower")

            shape = ma[row].shape

            for i in range(shape[0]):
                for j in range(shape[1]):
                    if (ma_var[row][i, j] == 9999.0):
                        text = ax.text(j, i, np.round(ma[row][i, j],2),
                                ha="center", va="center", color="w")
                    else:
                        text = ax.text(j, i, str(np.round(ma[row][i, j],2)) + "\n (" + str(np.round(ma_var[row][i, j],2)) + ")",
                                ha="center", va="center", color="w")

            # ax.set_xticklabels(np.arange(-3,3,1))
            # ax.set_yticklabels(np.arange(3,-3,-1))

            # print(shape)
            # print(np.arange(-shape[1]//2 + 1, shape[1]//2 +1, 1))

            ax.set_xticklabels(np.arange(-shape[1]//2 +1, shape[1]//2 +1, 1))
            ax.set_yticklabels(np.arange(shape[0]//2 + 1,-shape[0]//2 -1,-1))

            ax.set_xlabel("x")
            ax.set_ylabel("y")
            
            ax.set_title(title[row])

            fig.colorbar(im, ax=ax) 

    fig.tight_layout()
    fig.suptitle(sup_title)
        
    plt.show()

def plot_1(matrix, title):

    fig, ax = plt.subplots()
    im = ax.imshow(matrix, interpolation='spline36', origin="lower")

    shape = matrix.shape

    # Loop over data dimensions and create text annotations.
    for i in range(shape[0]):
        for j in range(shape[1]):
            text = ax.text(j, i, np.round(matrix[i, j],2),
                        ha="center", va="center", color="w")

    ax.set_xticklabels(np.arange(-shape[0]//2 + 1, shape[0]//2 +1,1))
    ax.set_yticklabels(np.arange(shape[0]//2 +1,-shape[0]//2 -1,-1))

    ax.set_title(title)
    fig.tight_layout()
    fig.colorbar(im, ax=ax)
    # plt.savefig('prueba.pgf')
    plt.show()

def plot_2(matrix, matrix_var, title):

    fig, axs = plt.subplots(1,2)
    # im = ax.imshow(matrix, interpolation='spline36', origin="lower")

    shape = matrix.shape

    im = axs[0].imshow(matrix, interpolation='spline36', origin="lower")
    axs[0].set_title(title)
    fig.colorbar(im, ax=axs[0])
    
    im = axs[1].imshow(matrix_var, interpolation='spline36', origin="lower", cmap='hot')  
    axs[1].set_title("Varianza")
    fig.colorbar(im, ax=axs[1])

    for i in range(2):
        axs[i].set_xticklabels(np.arange(-shape[0]//2 + 1, shape[0]//2 +1,1))
        axs[i].set_yticklabels(np.arange(shape[0]//2 +1,-shape[0]//2 -1,-1))

        axs[i].set_xlabel("x")
        axs[i].set_ylabel("y")

    # fig.suptitle(title)
    fig.tight_layout()
    plt.show()

def plot_3(matrix, matrix_var, title, file_name, save):
    # from mpl_toolkits.axes_grid1 import make_axes_locatable
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes

    _min = np.min(matrix[0:2])
    _max = np.max(matrix[0:2])

    fig = plt.figure(figsize=[7,5], constrained_layout=False)
    widths = [0.3,1]
    heights = [1]
    spec = fig.add_gridspec(ncols=2, nrows=1, width_ratios=widths, height_ratios=heights, hspace=0.01)


    ax_ejes = spec[0].subgridspec(2, 1)
    ax_x = fig.add_subplot(ax_ejes[0])
    ax_y = fig.add_subplot(ax_ejes[1])
    ax_pos = fig.add_subplot(spec[1])
    ax_pos.set_title("Posición")

    ax_x.set_title("Eje x")
    ax_x.set_xticks([])
    ax_x.set_yticks([])
    ax_y.set_title("Eje y")
    ax_y.set_xticks([])
    ax_y.set_yticks([])

    im_pos = ax_pos.imshow(matrix[2], interpolation='spline36', origin="lower")
    cb_pos = fig.colorbar(im_pos, ax = ax_pos, shrink=0.9)

    for i in range(matrix[2].shape[0]):
        for j in range(matrix[2].shape[1]):
            text = ax_pos.text(j, i, str(np.round(matrix[2][i, j],2)) + "\n (" + str(np.round(matrix_var[2][i, j],2)) + ")",
                        ha="center", va="center", color="w")

    cb_pos.ax.get_yaxis().labelpad = 15
    cb_pos.ax.set_ylabel('Diferencia de posición [cm]', rotation=270)

    ax_pos.set_xticklabels(np.arange(-3,3,1))
    ax_pos.set_yticklabels(np.arange(-4,4,1))
    ax_pos.set_xlabel("x [m]")
    ax_pos.set_ylabel("y [m]")


    imx = ax_x.imshow(matrix[0], interpolation='spline36', origin="lower", vmin=_min, vmax=_max, cmap='gnuplot')
    imy = ax_y.imshow(matrix[1], interpolation='spline36', origin="lower", vmin=_min, vmax=_max, cmap='gnuplot')
    axins = inset_axes(ax_x, # here using axis of the lowest plot
               width="10%",  # width = 5% of parent_bbox width
               height="150%",  # height : 340% good for a (4x4) Grid
               loc='lower left',
               bbox_to_anchor=(-0.5, -0.8, 1, 1),
               bbox_transform=ax_x.transAxes,
               borderpad=0,
               )

    # Colorbar
    axins.yaxis.tick_left()

    cb = fig.colorbar(imx, cax=axins)
    cb.ax.get_yaxis().labelpad = -50
    cb.ax.set_ylabel('Diferencia en la medida de cada eje [cm]', rotation=90)
    
    # Save or show the plot
    if save:
        import matplotlib
        matplotlib.use("pgf")
        matplotlib.rcParams.update({
            "pgf.texsystem": "pdflatex",
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
        })
        plt.savefig(f'{file_name}.pgf')
    else:
        plt.show()


def plot_3_bis(matrix, matrix_var, title):
    # DEPRECATED

    # from mpl_toolkits.axes_grid1 import make_axes_locatable
    # import matplotlib
    # matplotlib.use("pgf")
    # matplotlib.rcParams.update({
    #     "pgf.texsystem": "pdflatex",
    #     'font.family': 'serif',
    #     'text.usetex': True,
    #     'pgf.rcfonts': False,
    # })

    fig, axs = plt.subplots(ncols=2, nrows=2, figsize=[7,5])
    gs = axs[0, 1].get_gridspec()
    # remove the underlying axes
    for ax in axs[0:, -1]:
        ax.remove()
    axbig = fig.add_subplot(gs[0:, -1])

    imx = axs[0,0].imshow(matrix[0], interpolation='spline36', origin="lower")
    imy = axs[1,0].imshow(matrix[1], interpolation='spline36', origin="lower")
    impos = axbig.imshow(matrix[2], interpolation='spline36', origin="lower")

    # Titulos
    axs[0,0].set_title("Eje x")
    axs[1,0].set_title("Eje y")
    axbig.set_title("Posición")

    # Leyenda
    axs[0,0].set_xticks([])
    axs[0,0].set_yticks([])
    axs[1,0].set_xticks([])
    axs[1,0].set_yticks([])
    # axs[0,0].set_xticklabels(np.arange(-3,3,1))
    # axs[0,0].set_yticklabels(np.arange(-4,4,1))
    # axs[1,0].set_xticklabels(np.arange(-3,3,1))
    # axs[1,0].set_yticklabels(np.arange(-4,4,1))

    axbig.set_xticklabels(np.arange(-3,3,1))
    axbig.set_yticklabels(np.arange(-4,4,1))
    
    # fig.colorbar(imx, ax=[axs[0, 0]], location='bottom', shrink=0.6)
    fig.colorbar(imx, ax=axs[:, 0],location='left', shrink=0.6)
    fig.colorbar(impos, ax=axbig, shrink=0.8)

    # fig.tight_layout()

    plt.show()
