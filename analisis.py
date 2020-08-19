import numpy as np
import matplotlib.pyplot as plt
from plot import plot_4, plot_1, plot_2, plot_3
from get_data import read_tag_data_from_file, get_tag_data, get_odom_data, get_tray_sep, get_tray_fisica, get_ptos_fisica


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
            
            # print(add)
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

            print(f"{punto['x_real']:.4f} \t {punto['y_real']:.4f} \t {data[0]} +- {data[1]} \t {data[2]} +- {data[3]} \t " +
                  f"{diff_x} - {diff_y} - {ratio_diff}")

        # for k in range(len(matriz)):
        #     matriz[k] = np.flip(matriz[k],0)
        #     matriz_var[k] = np.flip(matriz_var[k],0)

        # plot_4(matriz, matriz_var, ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title + f" - Trayectoria {i+1}")
        # plot_1(matriz[0], 'Diferencia X')

def get_tray_media(tag, title, dim, num, corr=False):

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

            if corr:
                if cont == 3:
                    cont = 0
                    add = add + 0.02
                else:
                    cont = cont + 1 

            # diff_x = punto['x_real'] - data[0]- 0.1  
            # diff_x = punto['x_real'] - data[0] + add
            diff_x = punto['x_real'] - data[0]
            # diff_x = punto['x_real'] - data[0]- 0.1 + add 
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

    return np.array([matriz, matriz_var])

    # plt.boxplot([matriz[0].reshape(35), matriz[1].reshape(35)], notch=True)
    # plt.hist(matriz[0].reshape(35), bins=np.linspace(-30,30, 9))
    # plt.hist2d(matriz[0].reshape(35), matriz[1].reshape(35))
    # print(matriz[0].reshape(35))
    # plt.show()
    # plot_4(matriz, matriz_var, ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title)
    # plot_2(matriz[0], matriz_var[0], title)
    # plot_1(matriz[0], 'Diferencia X')



def plot_media(tag, title, dim, num, corr=False):

    matriz, matriz_var = get_tray_media(tag, title, dim, num, corr)

    plot_4(matriz, matriz_var, ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title)

def plot_media_total(tags, corr, dim, num, title, file_name, save):
    matriz_int = np.empty((len(tags), 4, 2*dim[1] +1, 2*dim[0] +1))
    matriz = np.zeros((4, 2*dim[1] +1, 2*dim[0] +1))
    matriz_std = np.full((4, 2*dim[1] +1, 2*dim[0] +1), 9999.0)

    for i in range(len(tags)):
        matriz_int[i] = get_tray_media(tags[i], "", dim, num[i], corr[i])[0]
    
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            for k in range(matriz.shape[2]):
                matriz[i,j,k] = np.average([ matriz_int[l,i,j,k] for l in range(len(tags)) ])
                matriz_std[i,j,k] = np.std([ matriz_int[l,i,j,k] for l in range(len(tags)) ])


    print(np.average(matriz[2]))
    print(np.std(matriz[2]))

    # plot_4(matriz, matriz_std, ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title)
    # plot_1(matriz[2], title)
    plot_3(matriz, matriz_std, title, file_name, save)
    # plot_4(matriz, np.full(matriz.shape, 9999.0), ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title)

    # for i in range(matriz.shape[1]):
    #     for j in range(matriz.shape[2]):
    #         with open("Media_tota.txt", 'a') as f:
    #             print(f"{i-dim[1]}\t{j-dim[0]}\t{matriz[0,i,j]}\t{matriz_std[0,i,j]}\t{matriz[1,i,j]}\t{matriz_std[1,i,j]}\t{matriz[2,i,j]}\t{matriz_std[2,i,j]}\t{matriz[3,i,j]}", file=f)


def plot_fisica(tag, num, title, corr=False):
    # matriz = np.zeros((4, 5, 5))
    # matriz_var = np.zeros((4, 5, 5))

    for i in range(num):
        matriz = get_tray_fisica(tag, i, title, corr)[0]
        matriz_var = get_tray_fisica(tag, i, title, corr)[1]
    
        plot_4(matriz, matriz_var, ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title)

def plot_media_fisica(tag, num, title, corr=False):
    matriz_int = np.zeros((4, 5, 5))
    matriz_int_var = np.zeros((4, 5, 5))
    matriz = np.zeros((4, 5, 5))
    matriz_var = np.zeros((4, 5, 5))

    for i in range(num):
        matriz_int = get_tray_fisica(tag, i, title, corr)[0]
        matriz_int_var = get_tray_fisica(tag, i, title, corr)[1]
        matriz = matriz + matriz_int
        matriz_var = matriz_var + matriz_int_var
    
    matriz = matriz / num
    matriz_var = matriz_var / num

    plot_4(matriz, matriz_var, ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title)

def plot_media_total_fisica(tags, title, corr=False):
    matriz_int = np.array((4, 5, 5))
    matriz = np.zeros((4, 5, 5))

    for i in range(len(tags)):
        matriz_int = get_tray_fisica(tags[i], i, title, corr)[0]
        matriz = matriz + matriz_int
    
    matriz = matriz / len(tags)

    matriz = np.ma.masked_where(matriz==0.0, matriz)

    plot_4(matriz, np.full(matriz.shape, 9999.0), ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title)

def plot_ptos_fisica(tags, nums, labels):

    title = ["Diferencia X", "Diferencia Y", "Diferencia POS"]

    for k in range(3):
        puntos = np.zeros((len(tags), 16*np.max(nums)))

        for i in range(len(tags)):
            for j in range(nums[i]):
                puntos[i, (16*j):(16*j+16)] = get_ptos_fisica(tags[i], j, True)[0][k]

        plt.boxplot((puntos[0], puntos[1], puntos[2][:32]), labels=labels)
        # plt.hist(puntos[0])
        # print(puntos[2][:32])
        # plt.hist(puntos[2][:32], bins=np.linspace(-30,30, 25))
        # plt.hist2d(puntos, puntos)
        plt.title(title[k])
        plt.show()

def plot_error(tag, dim, corr=False, num=1):
    
    for i in range(num):
        x = get_tray_sep(tag, i, dim, False)[0,0]
        x_sens = get_tray_sep(tag, i, dim, False)[1,0]
        x = x.reshape(x.size)
        x_sens = x_sens.reshape(x_sens.size)

        y = get_tray_sep(tag, i, dim, False)[0,1]
        y_sens = get_tray_sep(tag, i, dim, False)[1,1]
        y = y.reshape(y.size)
        y_sens = y_sens.reshape(y_sens.size)

def main():

    tags_4 = np.array(["D:/Descargas/Universidad/TFG/analisis/datos/VERT2020-06-29--16h00m", 
                    "D:/Descargas/Universidad/TFG/analisis/datos/RAND2020-07-02--11h36m"])

    corr_4 = np.array([False, False])     
    num_4 = np.array([3,3,3])           
    
    tags_6 = np.array(["D:/Descargas/Universidad/TFG/analisis/datos/VERT2020-06-29--16h55m", 
                    "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-07-02--13h08m",
                    "D:/Descargas/Universidad/TFG/analisis/datos/RAND2020-07-02--10h38m"])

    corr_6 = np.array([False, False, True])
    num_6 = np.array([3,2,3])

    plot_media_total(tags_4, corr_4, (2,3), num_4, "4 sensores", "4sensores", False)              
    plot_media_total(tags_6, corr_6, (2,3), num_6, "6 sensores", "6sensores", False)              


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
    # plot_media(tag, "Vertical +0 grados (6 sensores)", (2,3), 3)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/VERT2020-06-29--17h21m" #Tercero del de arriba, OK
    # get_tray(tag, "Vertical +0 grados (4 sensores)", (2,3))

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/VERT2020-06-29--16h00m" # Todo OK
    # get_tray(tag, "Vertical +0 grados (4 sensores)", (2,3))
    # plot_media(tag, "Vertical +0 grados (4 sensores)", (2,3), 3)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-06-29--18h45m" #Solo 1 OK
    # get_tray(tag, "Espiral +0 grados (6 sensores)", (2,3))
    # plot_media(tag, "Espiral +0 grados (6 sensores)", (2,2), 3)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-06-29--12h02m" #Todo OK
    # get_tray(tag, "Espiral +90 grados (6 sensores)", (2,2))
    # plot_media(tag, "Espiral +90 grados (6 sensores)", (2,2), 3)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-06-29--12h26m" #Solo 2 OK
    # get_tray(tag, "Espiral +90 grados (4 sensores)", (2,2))

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-06-29--10h56m" # Solo el primero OK
    # get_tray(tag, "Espiral +0 grados (6 sensores)", (2,2))

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-06-29--11h30m" #Solo 2 OK
    # get_tray(tag, "Espiral +0 grados (4 sensores)", (2,2))
    # plot_media(tag, "Espiral +0 grados (4 sensores)", (2,2), 2)

    # 2/7 -----------------------------------------------------------------------

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/RAND2020-07-02--10h38m" #Todo OK
    # get_tray(tag, "Aleatorio +0 grados (6 sensores)", (2,3))
    # plot_media(tag, "Aleatorio +0 grados (6 sensores)", (2,3), 3)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/RAND2020-07-02--11h36m" #Todo OK
    # get_tray(tag, "Aleatorio +0 grados (4 sensores)", (2,3))
    # plot_media_total(tag, "Aleatorio +0 grados (4 sensores)", (2,3), 3)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/ESP2020-07-02--13h08m" #Todo OK
    # get_tray(tag, "Aleatorio +0 grados (6 sensores)", (2,3))
    # plot_media(tag, "Espiral +0 grados (6 sensores)", (2,3), 2, True)

    # plot_error(tag, (2,3))


    # -----------------------------------------------------------------------------------
    #  EDIFIO FISICA
    # -----------------------------------------------------------------------------------

    # 22/7  -----------------------------------------------------------------------

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/FIS2020-07-22--12h12m" #Todo OK
    # get_tray_fisica(tag, "Física (4 sensores)")
    # plot_media_fisica(tag, 3, "Física (4 sensores)")
    # plot_fisica(tag, 3, "Física (4 sensores)")

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/FIS2020-07-22--13h21m" #Todo OK
    # get_tray_fisica(tag, "Física (4 sensores)")
    # plot_media_fisica(tag, 2, "Física (6 sensores)")
    # plot_fisica(tag, 2, "Física (6 sensores)")
    # plot_media_fisica(tag, 2, "Física (6 sensores - corregido)", True)
    # plot_fisica(tag, 2, "Física (6 sensores - corregido)", True)

    # 23/7  -----------------------------------------------------------------------

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/FIS2020-07-23--10h58m" #Solo 1, OK
    # get_tray_fisica(tag, "Física (4 sensores)")
    # plot_media_fisica(tag, 1, "Física (6 sensores)", False)
    # plot_fisica(tag, 1, "Física (6 sensores)", False)
    # plot_media_fisica(tag, 1, "Física (6 sensores - corregido)", True)
    # plot_fisica(tag, 1, "Física (6 sensores - corregido)", True)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/FIS2020-07-23--12h36m" #Todo OK
    # get_tray_fisica(tag, "Física (4 sensores)")
    # plot_media_fisica(tag, 3, "Física (8 sensores)", False)
    # plot_fisica(tag, 1, "Física (8 sensores)", False)
    # plot_media_fisica(tag, 3, "Física (8 sensores - corregido)", True)
    # plot_fisica(tag, 1, "Física (8 sensores - corregido)", True)



    # 24/7  -----------------------------------------------------------------------

    # tags_fisica = np.array(["D:/Descargas/Universidad/TFG/analisis/datos/FIS2020-07-24--11h12m",
    #                         "D:/Descargas/Universidad/TFG/analisis/datos/FIS2020-07-24--12h49m",
    #                         "D:/Descargas/Universidad/TFG/analisis/datos/FIS2020-07-24--13h26m"])

    # leyenda_fisica = np.array(["8 sensores",
    #                         "6 sensores",
    #                         "4 sensores"])
    
    # nums_fisica = np.array([3,3,2])
    
    # plot_ptos_fisica(tags_fisica, nums_fisica, leyenda_fisica)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/FIS2020-07-24--11h12m" #Todo OK
    # get_tray_fisica(tag, "Física (4 sensores)")
    # plot_media_fisica(tag, 3, "Física (8 sensores - mapa nuevo)", False)
    # plot_fisica(tag, 3, "Física (8 sensores - mapa nuevo)", False)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/FIS2020-07-24--12h49m" #Todo OK
    # get_tray_fisica(tag, "Física (4 sensores)")
    # plot_media_fisica(tag, 3, "Física (6 sensores - mapa nuevo)", False)
    # plot_fisica(tag, 3, "Física (6 sensores - mapa nuevo)", False)

    # tag = "D:/Descargas/Universidad/TFG/analisis/datos/FIS2020-07-24--13h26m" #Todo OK
    # get_tray_fisica(tag, "Física (4 sensores)")
    # plot_media_fisica(tag, 2, "Física (4 sensores - mapa nuevo)", False)
    # plot_fisica(tag, 2, "Física (4 sensores - mapa nuevo)", False)

main()

        
