import matplotlib.pyplot as plt
import numpy as np

def plot_4(matrix, matrix_var, titles, sup_title):

    fig, axs = plt.subplots(2,2)
    
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
            im = ax.imshow(ma[row])

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

            ax.set_xticklabels(np.arange(-(shape[1]//2) +1, shape[1]//2 +1, 1))
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
    im = ax.imshow(matrix)

    shape = matrix.shape

    # Loop over data dimensions and create text annotations.
    for i in range(shape[0]):
        for j in range(shape[1]):
            text = ax.text(j, i, np.round(matrix[i, j],2),
                        ha="center", va="center", color="w")

    ax.set_xticklabels(np.arange(-shape[0]//2, shape[0]//2 +1,1))
    ax.set_yticklabels(np.arange(shape[0]//2 +1,-shape[0]//2 -1,-1))

    ax.set_title(title)
    fig.tight_layout()
    plt.show()