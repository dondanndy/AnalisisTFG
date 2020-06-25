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

    for i in range(3):
        file = tag + "-" + str(i) + ".txt"

        puntos = np.loadtxt(file, delimiter='\t', dtype={'names': ('x_teo', 'y_teo', 'tag', 'x_real', 'y_real', 'trash'),
                                                        'formats': ('f4', 'f4', 'S35', 'f4', 'f4', 'f4')})

        matriz = np.empty((4,5,5))         
        matriz_var = np.empty((4,5,5))       

        for punto in puntos:
            data = get_tag_data(punto['tag'].decode('UTF-8'))
            
            diff_x = np.abs(punto['x_real'] - data[0])
            diff_y = np.abs(punto['y_real'] - data[2])
            ratio_diff = diff_x/diff_y

            matriz[0][int(punto['y_teo'])+2][int(punto['x_teo'])+2] = 100 * diff_x
            matriz[1][int(punto['y_teo'])+2][int(punto['x_teo'])+2] = 100 * diff_y
            # matriz[2][int(punto['y_teo'])+2][int(punto['x_teo'])+2] = np.abs(np.round(np.sqrt(np.power(punto['x_real'], 2) + np.power(punto['y_real'], 2)) - np.sqrt(np.power(data[0], 2) + np.power(data[2], 2)), 4)) #Probablemente no sirva
            matriz[2][int(punto['y_teo'])+2][int(punto['x_teo'])+2] = 100 * np.abs(np.round(np.sqrt(np.power(diff_x, 2) + np.power(diff_y, 2)), 4)) #Quiza es la buena
            
            # matriz[2][int(punto['y_teo'])+2][int(punto['x_teo'])+2] = np.round(np.abs(diff_x *punto['x_real'] + diff_y*punto['y_real']) / np.sqrt(np.power(punto['x_real'], 2) + np.power(punto['y_real'], 2)), 4)
            
            matriz[3][int(punto['y_teo'])+2][int(punto['x_teo'])+2] = data[4]

            # Matriz varianzas
            matriz_var[0][int(punto['y_teo'])+2][int(punto['x_teo'])+2] = 100 * np.round(data[1],3)
            matriz_var[1][int(punto['y_teo'])+2][int(punto['x_teo'])+2] = 100 * np.round(data[3],3)
            matriz_var[2][int(punto['y_teo'])+2][int(punto['x_teo'])+2] = 9999.0
            matriz_var[3][int(punto['y_teo'])+2][int(punto['x_teo'])+2] = data[5]

            # print(data)

            # print(f"{punto['x_real']:.4f} \t {punto['y_real']:.4f} \t {data[0]} +- {data[1]} \t {data[2]} +- {data[3]} \t " +
            #       f"{diff_x} - {diff_y} - {ratio_diff}")

        for k in range(len(matriz)):
            matriz[k] = np.flip(matriz[k],0)
            matriz_var[k] = np.flip(matriz_var[k],0)

        plot_4(matriz, matriz_var, ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title + f" - Trayectoria {i+1}")
        # plot_1(matriz[0], 'Diferencia X')


def main():

    tag = "D:/Descargas/Universidad/TFG/analisis/datos/2020-06-22--18h23m"
    get_tray(tag, "Espiral (Sensor en kinect)")

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/2020-06-22--19h14m"
    # get_tray(tag, "Espiral (Sensor en medio)")
    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/2020-06-22--18h48m"


main()

        
