import numpy as np

def read_tag_data_from_file(tag):

    file = "D:/Descargas/Universidad/TFG/analisis/sensores/" + tag + ".txt"

    return np.fromregex(file, r"POS,(.+),(.+),(.+),(.+)", [('x', np.float64), ('y', np.float64), ('z', np.float64), ('qf', np.int32)])[1:]

def get_tag_data(tag):
    '''
        Funcion para leer los datos de los sensores.
    ''' 
    data = read_tag_data_from_file(tag)

    x_data = np.average(data['x'])
    y_data = np.average(data['y'])
    x_data_var = np.std(data['x'])
    y_data_var = np.std(data['y'])
    qf = np.average(data['qf'])
    qf_var = np.std(data['qf'])

    return np.array([x_data, x_data_var, y_data, y_data_var, qf, qf_var])

def get_odom_data(tray, intent, dim, corr=False, kin=False):
    '''
        Funcion para leer los datos de amcl_pose
    ''' 

    file = tray + "-" + str(intent) + ".txt"

    try:
        puntos = np.loadtxt(file, delimiter='\t', dtype={'names': ('x_teo', 'y_teo', 'tag', 'x_real', 'x_real_var', 'y_real', 'y_real_var', 'yaw', 'trash'),
                                                    'formats': ('f4', 'f4', 'S35', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4')})
    except IndexError:
        puntos = np.loadtxt(file, delimiter='\t', dtype={'names': ('x_teo', 'y_teo', 'tag', 'x_real', 'y_real', 'trash'),
                                                    'formats': ('f4', 'f4', 'S35', 'f4', 'f4', 'f4')})

    matriz = np.zeros((2, 2*dim[1] +1, 2*dim[0] + 1))   

    add = 0
    cont = 0
    for punto in puntos:
        if corr:
            if cont == 3:
                cont = 0
                add = add + 0.03
            else:
                cont = cont + 1 

        if kin:
            matriz[0][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * punto['x_real'] + add - 0.1 #Eje x
        else:
            matriz[0][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * punto['x_real'] + add #Eje x
        matriz[1][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * punto['y_real'] #Eje y

    return matriz

def get_tray_lab(tag, title, dim, num, corr, kin):
    matriz_int = np.zeros((num, 4, 2*dim[1] +1, 2*dim[0] +1))
    matriz = np.zeros((4, 2*dim[1] +1, 2*dim[0] +1))
    matriz_var = np.zeros((4, 2*dim[1] +1, 2*dim[0] +1))

    for i in range(num):
        matriz_int[i][:2] = get_odom_data(tag)
        for j in range(matriz.shape[0]):
            for k in range(matriz.shape[1]):
                matriz_int[i][2][j][k] = np.sqrt(np.power(diff_x, 2) + np.power(diff_y, 2))


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

def get_ptos_fisica(tag, intent, POS=False):
    file = tag + "-" + str(intent) + ".txt"

    try:
        puntos = np.loadtxt(file, delimiter='\t', dtype={'names': ('x_teo', 'y_teo', 'tag', 'x_real', 'x_real_var', 'y_real', 'y_real_var', 'yaw', 'trash'),
                                                    'formats': ('f4', 'f4', 'S35', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4')})
    except IndexError:
        puntos = np.loadtxt(file, delimiter='\t', dtype={'names': ('x_teo', 'y_teo', 'tag', 'x_real', 'y_real', 'trash'),
                                                    'formats': ('f4', 'f4', 'S35', 'f4', 'f4', 'f4')})

    ptos = np.empty((4,len(puntos)))
    ptos_var = np.empty((4,len(puntos)))     

    for i in range(len(puntos)):
        data = get_tag_data(puntos[i]['tag'].decode('UTF-8')) 
        
        diff_x = puntos[i]['x_real'] - data[0] - 0.1
        diff_y = puntos[i]['y_real'] - data[2]
        # diff_x = puntos[i]['x_real']
        # diff_y = puntos[i]['y_real']
        # diff_x = data[0]
        # diff_y = data[2]

        ptos[0][i] = 100 * diff_x
        ptos[1][i] = 100 * diff_y
        if POS:
            ptos[2][i] = 100 * np.sqrt(np.power(diff_x, 2) + np.power(diff_y, 2))
        ptos[3][i] = data[4]

        # Matriz varianzas
        ptos_var[0][i] = 100 * data[1]
        ptos_var[1][i] = 100 * data[3]
        ptos_var[2][i] = 9999.0
        ptos_var[3][i] = data[5]

    return np.array((ptos, ptos_var))

def get_tray_fisica(tag, intent, title, corr):

    matriz = np.zeros((4, 5, 5))
    matriz_var = np.zeros((4, 5, 5))  

    ptos, ptos_var = get_ptos_fisica(tag, intent)
    
    # Metemos los puntos en la matriz
    for k in range(4):
        matriz[k][4] = ptos[k][8:13][::-1]
        matriz[k][0] = ptos[k][0:5]
        matriz[k][1:4][:,0] = ptos[k][13:][::-1]
        matriz[k][1:4][:,4] = ptos[k][5:8]

        # Metemos los puntos en la matriz de varianzas
        matriz_var[k][4] = ptos_var[k][8:13][::-1]
        matriz_var[k][0] = ptos_var[k][0:5]
        matriz_var[k][1:4][:,0] = ptos_var[k][13:][::-1]
        matriz_var[k][1:4][:,4] = ptos_var[k][5:8]

    # Correccion
    if corr:
        matriz[1][4] = matriz[1][4] + 40
        matriz[1][1:4][:,0] = matriz[1][1:4][:,0] + 40

    # Posicion, después de todo por si hay que corregir
    matriz[2] = np.sqrt(np.power(matriz[0], 2) + np.power(matriz[1], 2))

    return np.array((matriz, matriz_var))

def get_tray(tag, title, dim, corr=False):
    # Deprecated.

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

            if corr:
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

    return np.array(matriz, matriz_var)
            # print(data)

            # print(f"{punto['x_real']:.4f} \t {punto['y_real']:.4f} \t {data[0]} +- {data[1]} \t {data[2]} +- {data[3]} \t " +
            #       f"{diff_x} - {diff_y} - {ratio_diff}")

        # for k in range(len(matriz)):
        #     matriz[k] = np.flip(matriz[k],0)
        #     matriz_var[k] = np.flip(matriz_var[k],0)

        # plot_4(matriz, matriz_var, ['Diferencia X', 'Diferencia Y', 'Diferencia POS', "Factor de calidad"], title + f" - Trayectoria {i+1}")
        # plot_1(matriz[0], 'Diferencia X')

def get_tray_sep(tag, num, dim, corr=False, kin=False):

    # for i in range(num):
    file = tag + "-" + str(num) + ".txt"

    add = 0
    cont=0

    try:
        puntos = np.loadtxt(file, delimiter='\t', dtype={'names': ('x_teo', 'y_teo', 'tag', 'x_real', 'x_real_var', 'y_real', 'y_real_var', 'yaw', 'trash'),
                                                    'formats': ('f4', 'f4', 'S35', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4')})
    except IndexError:
        puntos = np.loadtxt(file, delimiter='\t', dtype={'names': ('x_teo', 'y_teo', 'tag', 'x_real', 'y_real', 'trash'),
                                                    'formats': ('f4', 'f4', 'S35', 'f4', 'f4', 'f4')})

    matriz = np.zeros((2, 2*dim[1] +1, 2*dim[0] +1))         
    matriz_sens = np.zeros((2, 2*dim[1] +1, 2*dim[0] +1))       

    for punto in puntos:
        data = get_tag_data(punto['tag'].decode('UTF-8')) 

        add = 0
        cont = 0
        
        if corr:
            if cont == 3:
                cont = 0
                add = add + 0.03
            else:
                cont = cont + 1 

        if kin:
            matriz[0][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * (punto['x_real'] + add - 0.1) #Eje x
        else:
            matriz[0][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * (punto['x_real'] + add) #Eje x
        
        matriz[1][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * punto['y_real'] #Eje y

        # Matriz sensor
        matriz_sens[0][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * data[0]
        matriz_sens[1][int(punto['y_teo'])+ dim[1]][int(punto['x_teo'])+ dim[0]] = 100 * data[2]

    return np.array((matriz, matriz_sens))