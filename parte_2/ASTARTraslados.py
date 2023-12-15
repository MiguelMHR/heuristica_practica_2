#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" importing libraries """
import sys
import time
import re
import os

# ========== LECTURA DE LA ENTRADA ==========
# Importamos las listas para poder obtener los datos del archivo
def parse_file(path):
    with open(path, "r", encoding="utf8") as archivo:
        resultado = (archivo.read())
        # parseamos el resultado a lista de listas
        # Usa expresiones regulares para dividir el contenido en filas
        filas = re.split(r'\n+', resultado.strip())
        # Divide cada fila en elementos usando ';'
        mapa = [re.split(r';+', fila) for fila in filas]
        # Cambiamos las '1' y '2' por 1 y 2
        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                patron = r'^\d$'
                if re.match(patron, mapa[i][j]):
                    mapa[i][j] = int(mapa[i][j])
        print(mapa)
        return mapa

# ========== ESCRITURA DE LA SALIDA ==========
def salida_solucion_problema(pasos_solucion):
    nombre_archivo = 'parte_2/ASTAR-tests/'+(os.path.basename(sys.argv[1]))[:-4]+'-'+(sys.argv[2])+'.output'
    with open(nombre_archivo, "w", encoding="utf8") as archivo:
        for paso in pasos_solucion:
            archivo.write(paso) 
            
def salida_estadisticas(tiempo_total, coste_total, longitud_solucion, nodos_expandidos):
    nombre_archivo = 'parte_2/ASTAR-tests/'+(os.path.basename(sys.argv[1]))[:-4]+'-'+(sys.argv[2])+'.stats'
    with open(nombre_archivo, "w", encoding="utf8") as archivo:
        archivo.write('Tiempo total: ' + str(tiempo_total) + "\n")
        archivo.write('Coste total: ' + str(coste_total) + "\n")
        archivo.write('Longitud de la solución: ' + str(longitud_solucion) + "\n")
        archivo.write('Nodos expandidos: ' + str(nodos_expandidos) + "\n")

# ========== ESTADOS DEL PROBLEMA ==========
class Estado():
    """ 
    Clase de los nodos para el algoritmo A* 
    Estado:
        - padre: nodo padre del nodo actual
        - x: fila del mapa en la que se encuentra la ambulancia
        - y: columna del mapa en la que se encuentra la ambulancia
        - valor: valor de la casilla justo antes de que la ambulancia se mueva a ella
        - carga: energía que le queda a la ambulancia
        - ubi_n: lista de las coordenadas de los pacientes no contagiosos que quedan por recoger
        - ubi_c: lista de las coordenadas de los pacientes contagiosos que quedan por recoger
        - plazas_n: lista que almacena los pacientes no contagiosos que ya han sido recogidos
                    (puede tener una longitud máxima de 8)
                    Por cada paciente no contagioso recogido, se añade un valor False a la lista
        - plazas_c: lista que puede almacenar tanto pacientes no contagiosos como contagiosos
                    (puede tener una longitud máxima de 2)
                    (Los pacientes no contagiosos solo pueden usar estas plazas 
                    si no hay pacientes contagiosos en ellas)
                    Por cada paciente contagioso recogido, se añade un valor True a la lista
                    Por cada paciente no contagioso recogido, se añade un valor False a la lista
        - ubi_p: coordenadas del parking
        - ubi_cn: lista de las coordenadas de los centros de atención de pacientes no contagiosos
        - ubi_cc: lista de las coordenadas de los centros de atención de pacientes contagiosos
        - coste_g: coste de la función g
        - coste_h: coste de la función h
        - coste_f: coste de la función f (f = g + h)
    Posibles valores de "valor":
        - 1: pasar por esta casilla consume 1 de energía
        - 2: pasar por esta casilla consume 2 de energía
        - N: en esta casilla hay un paciente no contagioso antes de que la ambulancia pase por ella
        - C: en esta casilla hay un paciente contagioso antes de que la ambulancia pase por ella
        - CC: en esta casilla hay un Centro de atención de pacientes Contagiosos
        - CN: en esta casilla hay un Centro de atención de pacientes No contagiosos
        - P: en esta casilla hay un Parking (casilla de salida, de fin y de recarga completa de energía)
        - X: en esta casilla hay un obstáculo (no se puede pasar por ella)
    """
    def __init__(self, padre: object, x: int, y: int, valor: int, nueva_carga: int, ubi_n: list, ubi_c: list,
                 plazas_n: list, plazas_c: list, num_heuristica: int, ubi_p: list = None, ubi_cn: list = None, ubi_cc: list = None):
        """ Constructor de la clase Estado """
        self.padre = padre
        self.x = x
        self.y = y
        self.valor = valor
        self.carga = nueva_carga
        self.ubi_n = ubi_n
        self.ubi_c = ubi_c
        self.plazas_n = plazas_n
        self.plazas_c = plazas_c
        self.ubi_p = padre.ubi_p if ubi_p is None else ubi_p
        self.ubi_cn = padre.ubi_cn if ubi_cn is None else ubi_cn
        self.ubi_cc = padre.ubi_cc if ubi_cc is None else ubi_cc
        self.coste_g = self.calcular_coste_g(padre)
        self.coste_h = self.calcular_coste_h(num_heuristica)
        self.coste_f = self.coste_g + self.coste_h
    
    def calcular_coste_g(self, padre: object) -> int:
        """ Función que calcula el coste g """
        # Si el padre es None, es el nodo inicial
        if padre is None:
            return 0
        # Si el padre no es None, sumamos el coste del padre más el coste de la casilla
        # Si self.valor es int, ese es el coste de la casilla. En caso contrario, es 1.
        return padre.coste_g + (self.valor if isinstance(self.valor, int) else 1)
    
    def calcular_coste_h(self, num_heuristica: int) -> int:
        """ Función que calcula el coste h """
        if num_heuristica == 1:
            return self.heuristica_1()
        elif num_heuristica == 2:
            return self.heuristica_2()
        elif num_heuristica == 3:
            return self.heuristica_3()
        elif num_heuristica == 4:
            return self.heuristica_4()
        elif num_heuristica == 5:
            return self.heuristica_5()
        else:
            raise ValueError("El número de la heurística (num_heuristica) no es válido")
        
    def heuristica_1(self) -> int:
        """ Función que implementa la heurística 1: Dijkstra """
        return 0

    def heuristica_2(self) -> int:
        """ Función que implementa la heurística 1 """
        # Si no quedan pacientes por recoger, la heurística es 0
        if not self.ubi_n and not self.ubi_c:
            return 0
        # Si quedan pacientes por recoger, la heurística es 1
        return 1
    
    def heuristica_3(self) -> int:
        """ Función que implementa la heurística 2 """
        # Si no quedan pacientes por recoger, la heurística es 0
        if not self.ubi_n and not self.ubi_c:
            return 0
        # Si quedan pacientes por recoger, la heurística es el número de pacientes
        return len(self.ubi_n) + len(self.ubi_c)
    
    def heuristica_4(self) -> int:
        """
        Función que implementa la heurística 4

        - Si todavía quedan pacientes no contagiosos por recoger:
            - Se calcula la distancia de Manhattan entre la ambulancia y el paciente no contagioso más cercano
            - A esta distancia, se le suma la distancia de Manhattan entre dicho paciente, y el paciente
              no contagioso más cercano a él
            - Este proceso se repite con todos los pacientes no contagiosos que quedan por recoger
            - A esta suma de distancias, se le suma la distancia de Manhattan entre el último paciente
              no contagioso y el paciente contagioso más cercano a él.
            - Se continúa este proceso hasta que no queden pacientes no contagiosos por recoger
            - Cuando no queden pacientes por recoger, se calcula la distancia de Manhattan entre el último y el parking
        - Si no quedan pacientes no contagiosos por recoger:
            - Se calcula la distancia de Manhattan entre la ambulancia y el paciente contagioso más cercano.
            - A esta distancia, se le suma la distancia de Manhattan entre dicho paciente, y el paciente
              contagioso más cercano a él.
            - Este proceso se repite con todos los pacientes contagiosos que quedan por recoger
            - A esta suma de distancias, se le suma la distancia de Manhattan entre el último paciente
              contagioso y el parking
        """
        # Si no quedan pacientes por recoger, la heurística es la distancia de Manhattan entre la ambulancia y el parking
        if not self.ubi_n and not self.ubi_c:
            return abs(self.x - self.ubi_p[0]) + abs(self.y - self.ubi_p[1])
        # Si quedan pacientes no contagiosos por recoger
        elif self.ubi_n:
            pacientes_n_visitados = []
            distancia_minima_n = 0
            distancia_total = 0
            # Se repite el proceso hasta que no queden pacientes no contagiosos por visitar
            while len(pacientes_n_visitados) < len(self.ubi_n):
                # Se elige el paciente no contagioso más cercano a la ambulancia
                for paciente_n in self.ubi_n:
                    distancia = abs(self.x - paciente_n[0]) + abs(self.y - paciente_n[1])
                    if distancia_minima_n == 0 or distancia < distancia_minima_n:
                        distancia_minima_n = distancia
                        paciente_n_mas_cercano = paciente_n
                # Se añade a la lista de pacientes no contagiosos visitados
                pacientes_n_visitados.append(paciente_n_mas_cercano)
                # Se suma a la distancia total
                distancia_total += distancia_minima_n
            # Cuando no quedan pacientes no contagiosos por visitar, se calcula la distancia de Manhattan
            # entre el último y el paciente contagioso más cercano
            distancia_minima_c = 0
            pacientes_c_visitados = []
            # Se repite el proceso hasta que no queden pacientes contagiosos por visitar
            while len(pacientes_c_visitados) < len(self.ubi_c):
                # Se elige el paciente contagioso más cercano al último paciente no contagioso visitado
                for paciente_c in self.ubi_c:
                    distancia = abs(paciente_n_mas_cercano[0] - paciente_c[0]) + abs(paciente_n_mas_cercano[1] - paciente_c[1])
                    if distancia_minima_c == 0 or distancia < distancia_minima_c:
                        distancia_minima_c = distancia
                        paciente_c_mas_cercano = paciente_c
                # Se añade a la lista de pacientes contagiosos visitados
                pacientes_c_visitados.append(paciente_c_mas_cercano)
                # Se suma a la distancia total
                distancia_total += distancia_minima_c
            # Cuando no quedan pacientes contagiosos por visitar, se calcula la distancia de Manhattan
            # entre el último paciente contagioso y el parking
            distancia_total += abs(paciente_c_mas_cercano[0] - self.ubi_p[0]) + abs(paciente_c_mas_cercano[1] - self.ubi_p[1])
            return distancia_total
        
        # Si no quedan pacientes no contagiosos por recoger
        else:
            pacientes_c_visitados = []
            distancia_minima_c = 0
            distancia_total = 0
            # Se repite el proceso hasta que no queden pacientes contagiosos por visitar
            while len(pacientes_c_visitados) < len(self.ubi_c):
                # Se elige el paciente contagioso más cercano a la ambulancia
                for paciente_c in self.ubi_c:
                    distancia = abs(self.x - paciente_c[0]) + abs(self.y - paciente_c[1])
                    if distancia_minima_c == 0 or distancia < distancia_minima_c:
                        distancia_minima_c = distancia
                        paciente_c_mas_cercano = paciente_c
                # Se añade a la lista de pacientes contagiosos visitados
                pacientes_c_visitados.append(paciente_c_mas_cercano)
                # Se suma a la distancia total
                distancia_total += distancia_minima_c
            # Cuando no quedan pacientes contagiosos por visitar, se calcula la distancia de Manhattan
            # entre el último paciente contagioso y el parking
            distancia_total += abs(paciente_c_mas_cercano[0] - self.ubi_p[0]) + abs(paciente_c_mas_cercano[1] - self.ubi_p[1])
            return distancia_total
    
    def heuristica_5(self) -> int:
        """
        Función que implementa la heurística 5

        Igual que la 4, pero cuando no quedan pacientes por recoger, se tiene en cuenta la distancia
        a los centros de atención si siguen quedando pacientes en la ambulancia
        """
        # Si no quedan pacientes por recoger
        if not self.ubi_n and not self.ubi_c:
            distancia_total = 0
            # Si quedan pacientes contagiosos en la ambulancia
            if self.plazas_c:
                # Se calcula la distancia de Manhattan entre la ambulancia y el centro de atención de pacientes contagiosos más cercano
                distancia_minima_cc = 0
                for centro_c in self.ubi_cc:
                    distancia = abs(self.x - centro_c[0]) + abs(self.y - centro_c[1])
                    if distancia_minima_cc == 0 or distancia < distancia_minima_cc:
                        distancia_minima_cc = distancia
                        centro_c_mas_cercano = centro_c
                distancia_total += distancia_minima_cc
                # Si quedan pacientes no contagiosos en la ambulancia
                if self.plazas_n:
                    # Se calcula la distancia de Manhattan entre el centro de atención de pacientes contagiosos más cercano y el centro de atención de pacientes no contagiosos más cercano
                    distancia_minima_cn = 0
                    for centro_n in self.ubi_cn:
                        distancia = abs(centro_c_mas_cercano[0] - centro_n[0]) + abs(centro_c_mas_cercano[1] - centro_n[1])
                        if distancia_minima_cn == 0 or distancia < distancia_minima_cn:
                            distancia_minima_cn = distancia
                            centro_n_mas_cercano = centro_n
                    distancia_total += distancia_minima_cn
                    # Se calcula la distancia de Manhattan entre el centro de atención de pacientes no contagiosos más cercano y el parking
                    distancia_total += abs(centro_n_mas_cercano[0] - self.ubi_p[0]) + abs(centro_n_mas_cercano[1] - self.ubi_p[1])
                # Si no quedan pacientes no contagiosos en la ambulancia
                else:
                    # Se calcula la distancia de Manhattan entre el centro de atención de pacientes contagiosos más cercano y el parking
                    distancia_total += abs(centro_c_mas_cercano[0] - self.ubi_p[0]) + abs(centro_c_mas_cercano[1] - self.ubi_p[1])
            # Si no quedan pacientes contagiosos en la ambulancia
            else:
                # Si quedan pacientes no contagiosos en la ambulancia
                if self.plazas_n:
                    # Se calcula la distancia de Manhattan entre la ambulancia y el centro de atención de pacientes no contagiosos más cercano
                    distancia_minima_cn = 0
                    for centro_n in self.ubi_cn:
                        distancia = abs(self.x - centro_n[0]) + abs(self.y - centro_n[1])
                        if distancia_minima_cn == 0 or distancia < distancia_minima_cn:
                            distancia_minima_cn = distancia
                            centro_n_mas_cercano = centro_n
                    distancia_total += distancia_minima_cn
                    # Se calcula la distancia de Manhattan entre el centro de atención de pacientes no contagiosos más cercano y el parking
                    distancia_total += abs(centro_n_mas_cercano[0] - self.ubi_p[0]) + abs(centro_n_mas_cercano[1] - self.ubi_p[1])
                # Si no quedan pacientes no contagiosos en la ambulancia
                else:
                    # Se calcula la distancia de Manhattan entre la ambulancia y el parking
                    distancia_total += abs(self.x - self.ubi_p[0]) + abs(self.y - self.ubi_p[1])
            return distancia_total
                   
        # Si quedan pacientes no contagiosos por recoger
        elif self.ubi_n:
            pacientes_n_visitados = []
            distancia_minima_n = 0
            distancia_total = 0
            # Se repite el proceso hasta que no queden pacientes no contagiosos por visitar
            while len(pacientes_n_visitados) < len(self.ubi_n):
                # Se elige el paciente no contagioso más cercano a la ambulancia
                for paciente_n in self.ubi_n:
                    distancia = abs(self.x - paciente_n[0]) + abs(self.y - paciente_n[1])
                    if distancia_minima_n == 0 or distancia < distancia_minima_n:
                        distancia_minima_n = distancia
                        paciente_n_mas_cercano = paciente_n
                # Se añade a la lista de pacientes no contagiosos visitados
                pacientes_n_visitados.append(paciente_n_mas_cercano)
                # Se suma a la distancia total
                distancia_total += distancia_minima_n
            # Cuando no quedan pacientes no contagiosos por visitar, se calcula la distancia de Manhattan
            # entre el último y el paciente contagioso más cercano
            distancia_minima_c = 0
            pacientes_c_visitados = []
            # Se repite el proceso hasta que no queden pacientes contagiosos por visitar
            while len(pacientes_c_visitados) < len(self.ubi_c):
                # Se elige el paciente contagioso más cercano al último paciente no contagioso visitado
                for paciente_c in self.ubi_c:
                    distancia = abs(paciente_n_mas_cercano[0] - paciente_c[0]) + abs(paciente_n_mas_cercano[1] - paciente_c[1])
                    if distancia_minima_c == 0 or distancia < distancia_minima_c:
                        distancia_minima_c = distancia
                        paciente_c_mas_cercano = paciente_c
                # Se añade a la lista de pacientes contagiosos visitados
                pacientes_c_visitados.append(paciente_c_mas_cercano)
                # Se suma a la distancia total
                distancia_total += distancia_minima_c
            # Cuando no quedan pacientes contagiosos por visitar, se calcula la distancia de Manhattan
            # entre el último paciente contagioso y el parking
            distancia_total += abs(paciente_c_mas_cercano[0] - self.ubi_p[0]) + abs(paciente_c_mas_cercano[1] - self.ubi_p[1])
            return distancia_total
        
        # Si no quedan pacientes no contagiosos por recoger
        else:
            pacientes_c_visitados = []
            distancia_minima_c = 0
            distancia_total = 0
            # Se repite el proceso hasta que no queden pacientes contagiosos por visitar
            while len(pacientes_c_visitados) < len(self.ubi_c):
                # Se elige el paciente contagioso más cercano a la ambulancia
                for paciente_c in self.ubi_c:
                    distancia = abs(self.x - paciente_c[0]) + abs(self.y - paciente_c[1])
                    if distancia_minima_c == 0 or distancia < distancia_minima_c:
                        distancia_minima_c = distancia
                        paciente_c_mas_cercano = paciente_c
                # Se añade a la lista de pacientes contagiosos visitados
                pacientes_c_visitados.append(paciente_c_mas_cercano)
                # Se suma a la distancia total
                distancia_total += distancia_minima_c
            # Cuando no quedan pacientes contagiosos por visitar, se calcula la distancia de Manhattan
            # entre el último paciente contagioso y el parking
            distancia_total += abs(paciente_c_mas_cercano[0] - self.ubi_p[0]) + abs(paciente_c_mas_cercano[1] - self.ubi_p[1])
            return distancia_total

    def __str__(self):
        """
        Función que imprime el estado con el siguiente formato:
            (x, y):valor:carga
        Ejemplo: 
            (8,4):P:50
        """
        # En la visualización del mapa, las filas empiezan en 1 y las columnas en 1, no en 0
        # Por ello, sumamos 1 a las coordenadas
        return "({},{})".format(self.x + 1, self.y + 1) + ":" + str(self.valor) + ":" + str(self.carga)

    def __eq__(self, estado):
        """ Función que compara si dos estados son iguales """
        return self.x == estado.x and self.y == estado.y and self.carga == estado.carga and \
               self.ubi_n == estado.ubi_n and self.ubi_c == estado.ubi_c and \
               self.plazas_n == estado.plazas_n and self.plazas_c == estado.plazas_c


# ========== EXPANSIÓN DE ESTADOS (APLICACIÓN DE OPERADORES) ==========
def expandir(estado: Estado, mapa: list, num_heuristica: int, coste_predeterminado: int = 1) -> list:
    """
    Función que expande un estado y devuelve una lista ordenada por el coste f de los estados hijos
    """
    hijos = []
    
    # Si la carga es 0, la ambulancia no se puede mover a ninguna casilla
    if estado.carga == 0:
        return hijos

    # La ambulancia se puede mover a cualquier casilla que no sea un obstáculo en vertical u horizontal
    # Tomamos los valores de las casillas de alrededor
    if estado.y >= 1:
        valor_izquierda = mapa[estado.x][estado.y - 1]
    else:
        valor_izquierda = None
    if estado.y < len(mapa[0]) - 1:
        valor_derecha = mapa[estado.x][estado.y + 1]
    else:
        valor_derecha = None
    if estado.x >= 1:
        valor_arriba = mapa[estado.x - 1][estado.y]
    else:
        valor_arriba = None
    if estado.x < len(mapa) - 1:
        valor_abajo = mapa[estado.x + 1][estado.y]
    else:
        valor_abajo = None
    
    # Comprobamos si se puede mover a la casilla de la izquierda
    if valor_izquierda and valor_izquierda != 'X':
        # Comprobamos si hay un parking en la casilla de la izquierda
        if valor_izquierda == 'P':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_P(estado, coste_predeterminado=coste_predeterminado)
        # Comprobamos si hay un paciente no contagioso en la casilla de la izquierda
        elif valor_izquierda == 'N':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n, valor_izquierda = acciones_casilla_N(estado, "izquierda", valor_izquierda, coste_predeterminado)
        # Comprobamos si hay un paciente contagioso en la casilla de la izquierda
        elif valor_izquierda == 'C':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n, valor_izquierda = acciones_casilla_C(estado, "izquierda", valor_izquierda, coste_predeterminado)
        # Comprobamos si hay un centro de atención de pacientes contagiosos en la casilla de la izquierda
        elif valor_izquierda == 'CC':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_CC(estado, coste_predeterminado)
        # Comprobamos si hay un centro de atención de pacientes no contagiosos en la casilla de la izquierda
        elif valor_izquierda == 'CN':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_CN(estado, coste_predeterminado)
        # Comprobamos si la casilla de la izquierda contiene un valor numérico
        elif isinstance(valor_izquierda, int):
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_numerica(estado, valor_izquierda)        
        else:
            raise ValueError("El valor de la casilla (" + str(estado.x) + "," + str(estado.y - 1) + ") no es válido")

        # Comprobamos si la carga es mayor o igual que 0
        # Si es menor que 0, no se puede mover a esa casilla
        if nueva_carga >= 0:
            # Si la carga es mayor o igual que 0, creamos el estado hijo
            hijo = Estado(estado, estado.x, estado.y - 1, valor_izquierda, nueva_carga, nueva_ubi_n, nueva_ubi_c,
                          nueva_plazas_n, nueva_plazas_c, num_heuristica)
            # Lo añadimos a la lista de hijos
            hijos.append(hijo)

    # Comprobamos si se puede mover a la casilla de la derecha
    if valor_derecha and valor_derecha != 'X':
        # Comprobamos si hay un parking en la casilla de la derecha
        if valor_derecha == 'P':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_P(estado, coste_predeterminado=coste_predeterminado)
        # Comprobamos si hay un paciente en la casilla de la derecha
        elif valor_derecha == 'N':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n, valor_derecha = acciones_casilla_N(estado, "derecha", valor_derecha, coste_predeterminado)
        # Comprobamos si hay un paciente contagioso en la casilla de la derecha
        elif valor_derecha == 'C':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n, valor_derecha = acciones_casilla_C(estado, "derecha", valor_derecha, coste_predeterminado)
        # Comprobamos si hay un centro de atención de pacientes contagiosos en la casilla de la derecha
        elif valor_derecha == 'CC':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_CC(estado, coste_predeterminado)
        # Comprobamos si hay un centro de atención de pacientes no contagiosos en la casilla de la derecha
        elif valor_derecha == 'CN':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_CN(estado, coste_predeterminado)
        # Comprobamos si la casilla de la derecha contiene un valor numérico
        elif isinstance(valor_derecha, int):
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_numerica(estado, valor_derecha)
        else:
            raise ValueError("El valor de la casilla (" + str(estado.x) + "," + str(estado.y + 1) + ") no es válido")
        
        # Comprobamos si la carga es mayor o igual que 0
        # Si es menor que 0, no se puede mover a esa casilla
        if nueva_carga >= 0:
            # Si la carga es mayor o igual que 0, creamos el estado hijo
            hijo = Estado(estado, estado.x, estado.y + 1, valor_derecha, nueva_carga, nueva_ubi_n, nueva_ubi_c,
                          nueva_plazas_n, nueva_plazas_c, num_heuristica)
            # Lo añadimos a la lista de hijos
            hijos.append(hijo)

    # Comprobamos si se puede mover a la casilla de arriba
    if valor_arriba and valor_arriba != 'X':
        # Comprobamos si hay un parking en la casilla de arriba
        if valor_arriba == 'P':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_P(estado, coste_predeterminado=coste_predeterminado)
        # Comprobamos si hay un paciente no contagioso en la casilla de arriba
        elif valor_arriba == 'N':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n, valor_arriba = acciones_casilla_N(estado, "arriba", valor_arriba, coste_predeterminado)
        # Comprobamos si hay un paciente contagioso en la casilla de arriba
        elif valor_arriba == 'C':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n, valor_arriba = acciones_casilla_C(estado, "arriba", valor_arriba, coste_predeterminado)
        # Comprobamos si hay un centro de atención de pacientes contagiosos en la casilla de arriba
        elif valor_arriba == 'CC':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_CC(estado, coste_predeterminado)
        # Comprobamos si hay un centro de atención de pacientes no contagiosos en la casilla de arriba
        elif valor_arriba == 'CN':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_CN(estado, coste_predeterminado)
        # Comprobamos si la casilla de arriba contiene un valor numérico
        elif isinstance(valor_arriba, int):
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_numerica(estado, valor_arriba)
        else:
            raise ValueError("El valor de la casilla (" + str(estado.x - 1) + "," + str(estado.y) + ") no es válido")
        
        # Comprobamos si la carga es mayor o igual que 0
        # Si es menor que 0, no se puede mover a esa casilla
        if nueva_carga >= 0:
            # Si la carga es mayor o igual que 0, creamos el estado hijo
            hijo = Estado(estado, estado.x - 1, estado.y, valor_arriba, nueva_carga, nueva_ubi_n, nueva_ubi_c,
                          nueva_plazas_n, nueva_plazas_c, num_heuristica)
            # Lo añadimos a la lista de hijos
            hijos.append(hijo)

    # Comprobamos si se puede mover a la casilla de abajo
    if valor_abajo and valor_abajo != 'X':
        # Comprobamos si hay un parking en la casilla de abajo
        if valor_abajo == 'P':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_P(estado, coste_predeterminado=coste_predeterminado)
        # Comprobamos si hay un paciente no contagioso en la casilla de abajo
        elif valor_abajo == 'N':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n, valor_abajo = acciones_casilla_N(estado, "abajo", valor_abajo, coste_predeterminado)
        # Comprobamos si hay un paciente contagioso en la casilla de abajo
        elif valor_abajo == 'C':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n, valor_abajo = acciones_casilla_C(estado, "abajo", valor_abajo, coste_predeterminado)
        # Comprobamos si hay un centro de atención de pacientes contagiosos en la casilla de abajo
        elif valor_abajo == 'CC':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_CC(estado, coste_predeterminado)
        # Comprobamos si hay un centro de atención de pacientes no contagiosos en la casilla de abajo
        elif valor_abajo == 'CN':
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_CN(estado, coste_predeterminado)
        # Comprobamos si la casilla de abajo contiene un valor numérico
        elif isinstance(valor_abajo, int):
            nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n = acciones_casilla_numerica(estado, valor_abajo)
        else:
            raise ValueError("El valor de la casilla (" + str(estado.x + 1) + "," + str(estado.y) + ") no es válido")

        # Comprobamos si la carga es mayor o igual que 0
        # Si es menor que 0, no se puede mover a esa casilla
        if nueva_carga >= 0:
            # Si la carga es mayor o igual que 0, creamos el estado hijo
            hijo = Estado(estado, estado.x + 1, estado.y, valor_abajo, nueva_carga, nueva_ubi_n, nueva_ubi_c,
                          nueva_plazas_n, nueva_plazas_c, num_heuristica)
            # Lo añadimos a la lista de hijos
            hijos.append(hijo)
    
    # Ordenamos la lista de hijos por el coste f
    hijos.sort(key=lambda x: x.coste_f)

    return hijos


def recoger_paciente_n(estado: Estado, n_plazas_n: int = 8, n_plazas_c: int = 2) -> (bool, bool):
    """
    Indica si se puede recoger un paciente no contagioso en base a un estado
    (bool, bool) -> (se puede recoger, se recoge en plazas contagiosas)

    Posibles valores de retorno:
    (True, False) -> Se puede recoger y se recoge en plazas no contagiosas
    (True, True) -> Se puede recoger y se recoge en plazas contagiosas
    (False, False) -> No se puede recoger

    Un paciente no contagioso se recoge si hay plazas no contagiosas libres o
    si hay plazas contagiosas libres y no hay ningún paciente contagioso en ellas
    """
    # Comprobamos si hay plazas no contagiosas libres
    if len(estado.plazas_n) < n_plazas_n:
        return True, False
    # Comprobamos si hay plazas contagiosas libres
    if len(estado.plazas_c) < n_plazas_c:
        # Comprobamos si hay algún paciente contagioso en las plazas contagiosas
        if True in estado.plazas_c:     # Los pacientes contagiosos tienen un valor True
            return False, False
    # Si no hay ningún paciente contagioso en las plazas contagiosas, se puede recoger
    return True, True


def recoger_paciente_c(estado: Estado, n_plazas_c: int = 2) -> bool:
    """
    Indica si se puede recoger un paciente contagioso en base a un estado

    Un paciente contagioso se recoge si hay plazas contagiosas libres y no hay ningún paciente
    no contagioso en ellas. También NO debe haber ningún paciente no contagioso restante
    por recoger
    """
    # Comprobamos si quedan pacientes no contagiosos por recoger
    if estado.ubi_n:
        return False
    # Comprobamos si hay plazas contagiosas libres
    if len(estado.plazas_c) < n_plazas_c:
        # Comprobamos si hay algún paciente no contagioso en las plazas contagiosas
        if False in estado.plazas_c:    # Los pacientes no contagiosos tienen un valor False
            return False
    # Si no hay ningún paciente no contagioso en las plazas contagiosas, se puede recoger
    return True

def descargar_pacientes_n(estado: Estado) -> (bool, bool):
    """
    Indica si se pueden descargar pacientes no contagiosos en base a un estado
    (bool, bool) -> (se puede descargar de plazas no contagiosas, se puede descargar de plazas contagiosas)

    Posibles valores de retorno:
    (True, False) -> Se puede descargar de plazas no contagiosas, pero no de plazas contagiosas
    (True, True) -> Se puede descargar de plazas no contagiosas y de plazas contagiosas
    (False, False) -> No se puede descargar de ninguna plaza

    Un paciente no contagioso se puede descargar en un centro de atención de pacientes
    no contagiosos si NO hay ningún paciente contagioso en las plazas de pacientes
    contagiosos
    """
    # Comprobamos si hay algún paciente contagioso en las plazas de pacientes contagiosos
    if True in estado.plazas_c:     # Los pacientes contagiosos tienen un valor True
        return False, False
    # Comprobamos si hay pacientes no contagiosos en las plazas de pacientes no contagiosos
    elif False in estado.plazas_n:
        # Comprobamos si hay pacientes no contagiosos en las plazas de pacientes contagiosos
        if False in estado.plazas_c:
            return True, True
        else:
            return True, False
    else:
        return False, False     # No hay pacientes no contagiosos en ninguna plaza

def acciones_casilla_P(estado: Estado, max_carga: int = 50, coste_predeterminado: int = 1) -> (int, list, list, list, list):
    """
    Función que se ejecuta cuando se genera un estado hijo con un parking en la casilla
    """
    nueva_carga = max_carga
    # La lista de pacientes no contagiosos por recoger se mantiene igual
    nueva_ubi_n = estado.ubi_n.copy()
    # La lista de pacientes contagiosos por recoger se mantiene igual
    nueva_ubi_c = estado.ubi_c.copy()
    # La lista de plazas no contagiosas se mantiene igual
    nueva_plazas_n = estado.plazas_n.copy()
    # La lista de plazas contagiosas se mantiene igual
    nueva_plazas_c = estado.plazas_c.copy()
    return nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n

def acciones_casilla_N(estado:Estado, direccion_movimiento: str, valor_direccion: str | int, coste_predeterminado: int = 1) -> (int, list, list, list, list, int):
    """
    Función que se ejecuta cuando se genera un estado hijo con un paciente no contagioso en la casilla,
    dada una dirección de movimiento
    """
    desplazamiento_x, desplazamiento_y = 0, 0
    if direccion_movimiento == "arriba":
        desplazamiento_x = -1
    elif direccion_movimiento == "abajo":
        desplazamiento_x = 1
    elif direccion_movimiento == "izquierda":
        desplazamiento_y = -1
    elif direccion_movimiento == "derecha":
        desplazamiento_y = 1
    else:
        raise ValueError("La dirección de movimiento no es válida")

    nueva_carga = estado.carga - coste_predeterminado
    # La lista de pacientes contagiosos por recoger se mantiene igual
    nueva_ubi_c = estado.ubi_c.copy()
    # Comprobamos que el paciente no haya sido ya recogido
    if [estado.x + desplazamiento_x, estado.y + desplazamiento_y] in estado.ubi_n:
        # Si hay un paciente no contagioso, lo recogemos si es posible
        se_puede, en_plazas_c = recoger_paciente_n(estado)
        if se_puede:
            # Si se puede recoger, lo recogemos
            # Eliminamos las coordenadas del paciente no contagioso de la lista ubi_n
            nueva_ubi_n = estado.ubi_n.copy()
            nueva_ubi_n.remove([estado.x + desplazamiento_x, estado.y + desplazamiento_y])
            if en_plazas_c:
                # Si se recoge en plazas contagiosas, añadimos un False a la lista plazas_c
                nueva_plazas_c = estado.plazas_c.copy()
                nueva_plazas_c.append(False)
                # Y la lista plazas_n se mantiene igual
                nueva_plazas_n = estado.plazas_n.copy()
            else:
                # Si se recoge en plazas no contagiosas, añadimos un False a la lista plazas_n
                nueva_plazas_n = estado.plazas_n.copy()
                nueva_plazas_n.append(False)
                # Y la lista plazas_c se mantiene igual
                nueva_plazas_c = estado.plazas_c.copy()
        else:
            nueva_ubi_n = estado.ubi_n.copy()
            nueva_plazas_c = estado.plazas_c.copy()
            nueva_plazas_n = estado.plazas_n.copy()
    else:
        nueva_ubi_n = estado.ubi_n.copy()
        nueva_plazas_n = estado.plazas_n.copy()
        nueva_plazas_c = estado.plazas_c.copy()
        # Si el paciente ya había sido recogido, el valor del estado hijo es 1
        valor_direccion = 1
    return nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n, valor_direccion

def acciones_casilla_C(estado: Estado, direccion_movimiento: str, valor_direccion: str | int, coste_predeterminado: int = 1) -> (int, list, list, list, list, int):
    """
    Función que se ejecuta cuando se genera un estado hijo con un paciente contagioso en la casilla,
    dada una dirección de movimiento
    """
    desplazamiento_x, desplazamiento_y = 0, 0
    if direccion_movimiento == "arriba":
        desplazamiento_x = -1
    elif direccion_movimiento == "abajo":
        desplazamiento_x = 1
    elif direccion_movimiento == "izquierda":
        desplazamiento_y = -1
    elif direccion_movimiento == "derecha":
        desplazamiento_y = 1
    else:
        raise ValueError("La dirección de movimiento no es válida")
    
    nueva_carga = estado.carga - coste_predeterminado
    # La lista de pacientes no contagiosos por recoger se mantiene igual
    nueva_ubi_n = estado.ubi_n.copy()
    # Comprobamos que el paciente no haya sido ya recogido
    if [estado.x + desplazamiento_x, estado.y + desplazamiento_y] in estado.ubi_c:
        # Si hay un paciente contagioso, lo recogemos si es posible
        se_puede = recoger_paciente_c(estado)
        if se_puede:
            # Si se puede recoger, lo recogemos
            # Eliminamos las coordenadas del paciente contagioso de la lista ubi_c
            nueva_ubi_c = estado.ubi_c.copy()
            nueva_ubi_c.remove([estado.x + desplazamiento_x, estado.y + desplazamiento_y])
            # Añadimos un True a la lista plazas_c
            nueva_plazas_c = estado.plazas_c.copy()
            nueva_plazas_c.append(True)
            # Y la lista plazas_n se mantiene igual
            nueva_plazas_n = estado.plazas_n.copy()
        else:
            nueva_ubi_c = estado.ubi_c.copy()
            nueva_plazas_c = estado.plazas_c.copy()
            nueva_plazas_n = estado.plazas_n.copy()

    else:
        # Si el paciente ya había sido recogido, el valor del estado hijo es 1
        nueva_ubi_c = estado.ubi_c.copy()
        nueva_plazas_n = estado.plazas_n.copy()
        nueva_plazas_c = estado.plazas_c.copy()
        valor_direccion = 1
    return nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n, valor_direccion

def acciones_casilla_CC(estado: Estado, coste_predeterminado: int = 1) -> (int, list, list, list, list):
    """
    Función que se ejecuta cuando se genera un estado hijo con un centro de atención de pacientes
    contagiosos en la casilla
    """
    nueva_carga = estado.carga - coste_predeterminado
    # La lista de pacientes no contagiosos por recoger se mantiene igual
    nueva_ubi_n = estado.ubi_n.copy()
    # La lista de pacientes contagiosos por recoger se mantiene igual
    nueva_ubi_c = estado.ubi_c.copy()
    # La lista de plazas no contagiosas se mantiene igual
    nueva_plazas_n = estado.plazas_n.copy()
    # La lista de plazas contagiosas se vacía (se descargan todos los pacientes contagiosos)
    nueva_plazas_c = []
    return nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n

def acciones_casilla_CN(estado: Estado, coste_predeterminado: int = 1) -> (int, list, list, list, list):
    """
    Función que se ejecuta cuando se genera un estado hijo con un centro de atención de pacientes
    no contagiosos en la casilla
    """
    nueva_carga = estado.carga - coste_predeterminado
    # La lista de pacientes no contagiosos por recoger se mantiene igual
    nueva_ubi_n = estado.ubi_n.copy()
    # La lista de pacientes contagiosos por recoger se mantiene igual
    nueva_ubi_c = estado.ubi_c.copy()

    nueva_plazas_n = estado.plazas_n.copy()
    nueva_plazas_c = estado.plazas_c.copy()

    # Se comprueba si se pueden descargar pacientes no contagiosos
    se_puede_plazas_n, se_puede_plazas_c = descargar_pacientes_n(estado)
    if se_puede_plazas_n:
        # Si se pueden descargar pacientes no contagiosos de las plazas no contagiosas, se descargan
        # Se eliminan los pacientes no contagiosos de la lista plazas_n
        nueva_plazas_n = []
    if se_puede_plazas_c:
        # Si se pueden descargar pacientes no contagiosos de las plazas contagiosas, se descargan
        # Se eliminan los pacientes no contagiosos de la lista plazas_c
        nueva_plazas_c = []
    return nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n

def acciones_casilla_numerica(estado: Estado, coste: int = 1) -> (int, list, list, list, list):
    """
    Función que se ejecuta cuando se genera un estado hijo con un número en la casilla
    """
    nueva_carga = estado.carga - coste
    # La lista de pacientes no contagiosos por recoger se mantiene igual
    nueva_ubi_n = estado.ubi_n.copy()
    # La lista de pacientes contagiosos por recoger se mantiene igual
    nueva_ubi_c = estado.ubi_c.copy()
    # La lista de plazas no contagiosas se mantiene igual
    nueva_plazas_n = estado.plazas_n.copy()
    # La lista de plazas contagiosas se mantiene igual
    nueva_plazas_c = estado.plazas_c.copy()
    return nueva_carga, nueva_ubi_c, nueva_ubi_n, nueva_plazas_c, nueva_plazas_n

def merge_listas_ordenada(lista_a: list, lista_b: list) -> list:
    """
    Función que inserta una lista ordenada 'b' en otra lista ordenada 'a'
    de forma que la lista resultante siga ordenada
    """
    # Si la lista a está vacía, devolvemos la lista b
    if not lista_a:
        return lista_b
    # Si la lista b está vacía, devolvemos la lista a
    if not lista_b:
        return lista_a
    # Si la lista a y la lista b no están vacías, las combinamos
    # Creamos una lista vacía
    lista_ordenada = []
    # Mientras las dos listas tengan elementos
    while lista_a and lista_b:
        # Si el primer elemento de la lista a es menor o igual que el primer elemento de la lista b
        if lista_a[0].coste_f <= lista_b[0].coste_f:
            # Añadimos el primer elemento de la lista a a la lista ordenada
            lista_ordenada.append(lista_a.pop(0))
        else:
            # Añadimos el primer elemento de la lista b a la lista ordenada
            lista_ordenada.append(lista_b.pop(0))
    # Si la lista a tiene elementos restantes, los añadimos a la lista ordenada
    if lista_a:
        lista_ordenada.extend(lista_a)
    # Si la lista b tiene elementos restantes, los añadimos a la lista ordenada
    if lista_b:
        lista_ordenada.extend(lista_b)
    return lista_ordenada


# ========== ALGORITMO A* ==========
def a_estrella(estado_inicial: Estado, mapa: list, num_heuristica: int):
    """ 
    Función que implementa el algoritmo A* 
    Nota:
        ¿Cómo es un estado meta?
            - Tiene valor 'P'
            - ubi_n = []
            - ubi_c = []
            - plazas_n = []
            - plazas_c = []

    """
    # Iniciamos el cronómetro
    start_time = time.time()
    # Inicializamos las variables
    # Metemos en la lista abierta el estado inicial
    abierta = [estado_inicial]  # Es una lista ordenada por coste_f de los estados a expandir
    # Creamos la lista cerrada
    cerrada = []    # Es una lista de estados ya expandidos
    meta = False    # Indica si se ha expandido un estado meta
    solucion = []   # Lista de estados que forman la solución
    # Mientras la lista abierta no esté vacía y no se haya expandido una meta
    while abierta and not meta:
        # Sacamos el primer elemento de la lista abierta que no esté en la lista cerrada
        estado_actual = abierta.pop(0)
        while estado_actual in cerrada:     # Esto utiliza el método __eq__ de la clase Estado
            estado_actual = abierta.pop(0)
        # Si el estado actual es meta, terminamos
        if (estado_actual.valor == 'P' and not estado_actual.ubi_n and not estado_actual.ubi_c and 
            not estado_actual.plazas_n and not estado_actual.plazas_c):
            meta = True
        else:
            # Si el estado actual no es meta, lo expandimos
            # Añadimos el estado actual a la lista cerrada
            cerrada.append(estado_actual)
            # Expandimos el estado actual
            hijos = expandir(estado_actual, mapa, num_heuristica)
            # Insertamos los hijos (ya ordenados) en la lista abierta (ya ordenada)
            # de forma que la lista abierta siga ordenada
            abierta = merge_listas_ordenada(abierta, hijos)

    # Si se ha expandido una meta, obtenemos la solución
    if meta:
        # Añadimos el estado actual a la lista solucion
        solucion.append(estado_actual)
        # Paramos el cronómetro y guardamos el tiempo total
        tiempo_total = time.time() - start_time
        # Mientras el estado actual tenga padre
        while estado_actual.padre:
            # Añadimos el padre del estado actual a la lista solución
            solucion.append(estado_actual.padre)
            # El estado actual pasa a ser su padre
            estado_actual = estado_actual.padre
        # Invertimos la lista solución
        solucion.reverse()
        # Guardamos los pasos de la solución
        pasos_solucion = ""
        for estado in solucion:
            if estado != solucion[-1]:
                pasos_solucion += str(estado) + "\n"
            else:
                pasos_solucion += str(estado)
        # Guardamos el coste total de la solución
        coste_total = solucion[-1].coste_g
        # Guardamos la longitud de la solución
        longitud_solucion = len(solucion)
        # Guardamos el número de nodos expandidos
        # Le añadimos 1 para incluir el estado meta como nodo expandido
        nodos_expandidos = len(cerrada) + 1

    else:
        # Si no se ha expandido una meta, no hay solución
        # Paramos el cronómetro y guardamos el tiempo total
        tiempo_total = time.time() - start_time
        # Guardamos los pasos de la solución
        pasos_solucion = "No hay solución"
        # Guardamos el coste total de la solución
        coste_total = 0
        # Guardamos la longitud de la solución
        longitud_solucion = 0
        # Guardamos el número de nodos expandidos
        nodos_expandidos = len(cerrada)

    # Devolvemos los resultados
    return pasos_solucion, tiempo_total, coste_total, longitud_solucion, nodos_expandidos


# ========== PROGRAMA PRINCIPAL ==========
def main():
    """ Función principal del programa """
    # Obtenemos el path del fichero y la heurística a utilizar desde la consola, además de hacer comprobaciones adicionales
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print("Error: Se necesita un argumento (el path al test) y un tipo de heurística (1 al 5)")
        sys.exit(1)
    else:
        path = sys.argv[1]
        num_heuristica = int(sys.argv[2])
        if num_heuristica not in [1, 2, 3, 4, 5]:
            print("Error: El tipo de heurística debe ser entre 1 o 5")
            sys.exit(1)
    
    # Leemos el fichero y definimos los parámetros para el A*
    mapa = parse_file(path)
    CARGA_INICIAL = 50
    N_HEURISTICA = num_heuristica
    ubi_inicial = None
    ubi_cn = []
    ubi_cc = []
    ubi_n = []
    ubi_c = []
    # El estado inicial es aquel con valor 'P'
    # Buscamos el estado inicial y las coordenadas de los centros y de los pacientes
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if mapa[i][j] == 'P':
                ubi_inicial = [i, j]
            elif mapa[i][j] == 'CN':
                ubi_cn.append([i, j])
            elif mapa[i][j] == 'CC':
                ubi_cc.append([i, j])
            elif mapa[i][j] == 'N':
                ubi_n.append([i, j])
            elif mapa[i][j] == 'C':
                ubi_c.append([i, j])
    # Si no se ha encontrado el estado inicial, lanzamos una excepción
    if not ubi_inicial:
        raise ValueError("No se ha encontrado el estado inicial")
    # Creamos el estado inicial
    estado_inicial = Estado(None, ubi_inicial[0], ubi_inicial[1], 'P', CARGA_INICIAL, ubi_n, ubi_c, [], [], N_HEURISTICA, ubi_inicial, ubi_cn, ubi_cc)
    
    # Resolvemos el problema
    pasos_solucion, tiempo_total, coste_total, longitud_solucion, nodos_expandidos = a_estrella(estado_inicial, mapa, N_HEURISTICA)
    
    # Creamos los ficheros de salida
    salida_solucion_problema(pasos_solucion)
    salida_estadisticas(tiempo_total, coste_total, longitud_solucion, nodos_expandidos)

if __name__ == '__main__':
    # Llamamos a la función principal
    main()
