import numpy as np
import matplotlib.pyplot as plt
from plot import plot_4, plot_1, plot_2

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


def get_tray(tag, title, dim):

    for i in range(3):
        file = tag + "-" + str(i) + ".txt"

        add = 0
        cont=0

        try:
            puntos = np.loadtxt(file, delimiter='\t', dtype={'names': ('x_teo', 'y_teo', 'tag', 'x_real', 'x_real_var', 'y_real', 'y_real_var', 'yaw', 'trash'),
                                                        'formats': ('f4', 'f4', 'S35', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4')})
        except IndexError:
            puntos = np.loadtxt(file, delimiter='\t', dtype={'names': ('x_teo', 'y_teo', 'tag', 'x_real', 'y_real', 'trash'),
                                                        'formats': ('f4', 'f4', 'S35', 'f4', 'f4', 'f4')})

        matriz = np.zeros((4, 2*dim[1] +1, 2*dim[0] +1))         
        matriz_var = np.zeros((4, 2*dim[1] +1, 2*dim[0] +1))       

        for punto in puntos:
            data = get_tag_data(punto['tag'].decode('UTF-8')) 

            if cont == 3:
                cont = 0
                add = add + 0.03
            else:
                cont = cont + 1 
            
            print(add)
            diff_x = punto['x_real'] - data[0] + add
            diff_y = punto['y_real'] - data[2]
            ratio_diff = diff_x/diff_y

            matriz[0][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * diff_x
            matriz[1][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * diff_y
            # matriz[2][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = np.abs(np.round(np.sqrt(np.power(punto['x_real'], 2) + np.power(punto['y_real'], 2)) - np.sqrt(np.power(data[0], 2) + np.power(data[2], 2)), 4)) #Probablemente no sirva
            matriz[2][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * np.sqrt(np.power(diff_x, 2) + np.power(diff_y, 2)) #Quiza es la buena
            
            # matriz[2][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = np.round(np.abs(diff_x *punto['x_real'] + diff_y*punto['y_real']) / np.sqrt(np.power(punto['x_real'], 2) + np.power(punto['y_real'], 2)), 4)
            
            matriz[3][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = data[4]

            # Matriz varianzas
            # matriz_var[0][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = np.rad2deg(punto['yaw'])
            # matriz_var[1][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = np.rad2deg(punto['yaw'])
            matriz_var[0][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * data[1]
            matriz_var[1][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * data[3]
            matriz_var[2][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 9999.0
            matriz_var[3][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = data[5]

            # print(data)

            # print(f"{punto['x_real']:.4f} \t {punto['y_real']:.4f} \t {data[0]} +- {data[1]} \t {data[2]} +- {data[3]} \t " +
            #       f"{diff_x} - {diff_y} - {ratio_diff}")

        # for k in range(len(matriz)):
        #     matriz[k] = np.flip(matriz[k],0)
        #     matriz_var[k] = np.flip(matriz_var[k],0)

        plot_4(matriz, matriz_var, ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title + f" - Trayectoria {i+1}")
        # plot_1(matriz[0], 'Diferencia X')

def get_tray_media(tag, title, dim, num):

    matriz_int = np.zeros((num, 4, 2*dim[1] +1, 2*dim[0] +1))
    matriz = np.zeros((4, 2*dim[1] +1, 2*dim[0] +1))
    matriz_var = np.zeros((4, 2*dim[1] +1, 2*dim[0] +1))

    for i in range(num):
        file = tag + "-" + str(i) + ".txt"

        add = 0
        cont=0

        try:
            puntos = np.loadtxt(file, delimiter='\t', dtype={'names': ('x_teo', 'y_teo', 'tag', 'x_real', 'x_real_var', 'y_real', 'y_real_var', 'yaw', 'trash'),
                                                        'formats': ('f4', 'f4', 'S35', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4')})
        except IndexError:
            puntos = np.loadtxt(file, delimiter='\t', dtype={'names': ('x_teo', 'y_teo', 'tag', 'x_real', 'y_real', 'trash'),
                                                        'formats': ('f4', 'f4', 'S35', 'f4', 'f4', 'f4')})

        for punto in puntos:
            data = get_tag_data(punto['tag'].decode('UTF-8')) 

            if cont == 3:
                cont = 0
                add = add + 0.02
            else:
                cont = cont + 1 

            diff_x = punto['x_real'] - data[0] + add - 0.1
            diff_y = punto['y_real'] - data[2]
            ratio_diff = diff_x/diff_y

            matriz_int[i][0][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * diff_x
            matriz_int[i][1][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * diff_y
            matriz_int[i][2][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * np.sqrt(np.power(diff_x, 2) + np.power(diff_y, 2)) #Quiza es la buena
            matriz_int[i][3][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = data[4]

        # for k in range(len(matriz_int[i])):
        #     matriz_int[i][k] = np.flip(matriz_int[i][k],0)

    for i in range(len(matriz_int[0])):
        for j in range(len(matriz_int[0][i])):
            for k in range(len(matriz_int[0][i][j])):
                matriz[i,j,k] = np.average(matriz_int[:,i,j,k])
                matriz_var[i,j,k] = np.std(matriz_int[:,i,j,k])

    # plot_4(matriz, matriz_var, ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title)
    # plot_2(matriz[0], matriz_var[0], title)
    plot_1(matriz[0], 'Diferencia X')


def main():

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/2020-06-22--18h23m"
    # get_tray(tag, "Espiral (Sensor en kinect)", (2,2))

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/2020-06-22--18h23m"
    # get_tray(tag, "Espiral (Sensor en kinect)", (2,2))

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/2020-06-22--19h14m"
    # get_tray(tag, "Espiral (Sensor en medio)", (2,2))
    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/2020-06-22--18h48m"

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/2020-06-26--12h48m"
    # get_tray(tag, "Vertical (Sensor en medio)", (2,3))

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/2020-06-26--13h34m"
    # get_tray(tag, "Espiral (Sensor en medio)", (2,2))

    # 29/6 ------------------------------------------------

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/VERT2020-06-29--16h55m" # 3 OK
    # get_tray(tag, "Vertical +0 grados (6 sensores)", (2,3))
    # get_tray_media(tag, "Vertical +0 grados (6 sensores)", (2,3), 3)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/VERT2020-06-29--17h21m" #Tercero del de arriba, OK
    # get_tray(tag, "Vertical +0 grados (4 sensores)", (2,3))

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/VERT2020-06-29--16h00m" # Todo OK
    # get_tray(tag, "Vertical +0 grados (4 sensores)", (2,3))
    # get_tray_media(tag, "Vertical +0 grados (4 sensores)", (2,3), 3)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-06-29--18h45m" #Solo 1 OK
    # get_tray(tag, "Espiral +0 grados (6 sensores)", (2,3))
    # get_tray_media(tag, "Espiral +0 grados (6 sensores)", (2,2), 3)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-06-29--12h02m" #Todo OK
    # get_tray(tag, "Espiral +90 grados (6 sensores)", (2,2))
    # get_tray_media(tag, "Espiral +90 grados (6 sensores)", (2,2), 3)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-06-29--12h26m" #Solo 2 OK
    # get_tray(tag, "Espiral +90 grados (4 sensores)", (2,2))

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-06-29--10h56m" # Solo el primero OK
    # get_tray(tag, "Espiral +0 grados (6 sensores)", (2,2))

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-06-29--11h30m" #Solo 2 OK
    # get_tray(tag, "Espiral +0 grados (4 sensores)", (2,2))
    # get_tray_media(tag, "Espiral +0 grados (4 sensores)", (2,2), 2)

    # 2/7 -----------------------------------------------------------------------

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/RAND2020-07-02--10h38m" #Todo OK
    # get_tray(tag, "Aleatorio +0 grados (6 sensores)", (2,3))
    # get_tray_media(tag, "Aleatorio +0 grados (6 sensores)", (2,3), 3)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/RAND2020-07-02--11h36m" #Todo OK
    # get_tray(tag, "Aleatorio +0 grados (4 sensores)", (2,3))
    # get_tray_media(tag, "Aleatorio +0 grados (4 sensores)", (2,3), 3)

    tag = "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-07-02--13h08m" #Todo OK
    # get_tray(tag, "Aleatorio +0 grados (6 sensores)", (2,3))
    get_tray_media(tag, "Espiral +0 grados (6 sensores)", (2,3), 2)

main()

        
