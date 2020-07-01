import numpy as np
import matplotlib.pyplot as plt
from plot import plot_4, plot_1

def read_tag_data_from_file(tag):

    file = "D:/Descargas/Universidad/TFG/analisis/sensores/" + tag + ".txt"

    return np.fromregex(file, r"POS,(.+),(.+),(.+),(.+)", [('x', np.float64), ('y', np.float64), ('z', np.float64), ('qf', np.int32)])[1:]

def get_tag_data(tag):
    data = read_tag_data_from_file(tag)

    x_data = np.average(data['x'])
    y_data = np.average(data['y'])
    x_data_var = np.var(data['x'])
    y_data_var = np.var(data['y'])
    qf = np.average(data['qf'])
    qf_var = np.var(data['qf'])

    return np.array([x_data, x_data_var, y_data, y_data_var, qf, qf_var])


def get_tray(tag, title):

    for i in range(3,4):
        file = tag + "-" + str(i) + ".txt"


        puntos = np.loadtxt(file, delimiter='\t', dtype={'names': ('x_teo', 'y_teo', 'tag', 'x_real', 'x_real_var', 'y_real', 'y_real_var', 'yaw', 'trash'),
                                                        'formats': ('f4', 'f4', 'S35', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4')})

        matriz = np.empty((len(puntos), 3))
        print(len(puntos))        
        matriz_var = np.empty((len(puntos), 3))

        matriz[0][0] = puntos[0]['yaw']
        matriz[0][1] = get_tag_data(puntos[i]['tag'].decode('UTF-8'))[0]
        matriz[0][2] = get_tag_data(puntos[i]['tag'].decode('UTF-8'))[2]

        for i in range(1, len(puntos)):
            data = get_tag_data(puntos[i]['tag'].decode('UTF-8'))

            matriz[i][0] = puntos[i]['yaw']
            matriz[i][1] = 100* (get_tag_data(puntos[i]['tag'].decode('UTF-8'))[0]- puntos[i]['x_real'])
            matriz[i][2] = 100* (get_tag_data(puntos[i]['tag'].decode('UTF-8'))[2]- puntos[i]['y_real'])

            matriz_var[i][1] = 100 * get_tag_data(puntos[i]['tag'].decode('UTF-8'))[1]
            matriz_var[i][2] = 100 * get_tag_data(puntos[i]['tag'].decode('UTF-8'))[3]

            # print(data)
            print(f"{100*data[0]} - {100*data[2]}")

            # print(f"{puntos[i]['x_real']:.4f} \t {puntos[i]['y_real']:.4f} \t {puntos[i]['yaw']:.4f}")

        plt.polar(matriz[:,0], matriz[:,1] - matriz[0,1], 'ko')
        plt.polar(matriz[:,0], (matriz[:,1] - matriz[0,1]) + matriz_var[:,1], 'bo')
        plt.polar(matriz[:,0], (matriz[:,1] - matriz[0,1]) - matriz_var[:,1], 'bo')
        plt.show()

        plt.polar(matriz[:,0], matriz[:,2] - matriz[0,2], 'ko')
        plt.polar(matriz[:,0], (matriz[:,2] - matriz[0,2]) + matriz_var[:,2], 'bo')
        plt.polar(matriz[:,0], (matriz[:,2] - matriz[0,2]) - matriz_var[:,2], 'bo')
        plt.show()

    # plot_4(matriz, matriz_var, ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title + f" - Trayectoria {i+1}")
    # plot_1(matriz[0], 'Diferencia X')


def main():

    tag = "D:/Descargas/Universidad/TFG/analisis/datos/ROT2020-06-29--15h34m"
    get_tray(tag, 'hola')

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/ROT2020-06-29--15h26m"
    # get_tray(tag, 'hola')

main()