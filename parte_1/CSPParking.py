#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import constraint

# ========== LEEMOS LA DIRECCIÓN DEL ARCHIVO ==========
# La dirección del archivo se pasa como argumento al ejecutar el programa
# Ejemplo: python CSPParking.py ./CSP-tests/parking01

# Comprobamos que se ha pasado la dirección del archivo
if len(sys.argv) != 2:
    print("Error: no se ha pasado la dirección del archivo")
    sys.exit(1)

# Obtenemos la dirección del archivo
parking_path = sys.argv[1]

problem = constraint.Problem()

# ========== LEEMOS LOS DATOS DEL FICHERO ==========

"""
Formato del fichero:
<filas>x<columnas>
PE: <posiciones de las plazas especiales separadas por espacios>
<vehículo 1>
<vehículo 2>
...

Formato de los vehículos:
<id>-<tipo>-<presencia_congelador>

Ejemplo:
5x6
PE: (1,1) (1,2) (2,1) (4,1) (5,1) (5,2)
1-TSU-C
2-TNU-X
3-TNU-X
4-TNU-C
5-TSU-X
6-TNU-X
7-TNU-C
8-TSU-C

"""

def read_data(path: str) -> tuple:
    """
    Lee los datos de un fichero
    :param path: ruta del fichero
    :return: tupla con las dimensiones del parking, la lista de plazas especiales y la lista de vehículos
    """
    with open(path, "r", encoding="utf8") as file:
        # Leemos las dimensiones del parking
        dimensiones = file.readline().split("x")
        dimensiones = (int(dimensiones[0]), int(dimensiones[1]))
        # Leemos las plazas especiales, si no hay se devuelve una lista vacía
        try :
            plazas_especiales = file.readline()[4:].split(" ")
            plazas_especiales = [(int(char[1]), int(char[3])) for char in plazas_especiales]
        except:
            plazas_especiales = []
        # Leemos los vehículos
        vehiculos = []
        for line in file:
            vehiculos.append(line.strip())
        return dimensiones, plazas_especiales, vehiculos

# Definimos los datos del problema
dimensiones, plazas_especiales, vehiculos = read_data(parking_path)

# Comprobamos que se han leído bien los datos
# print(dimensiones)
# print(plazas_especiales)
# print(vehiculos)

# NOTA: los índices de las plazas empiezan en 1, no en 0

"""
Ejemplo de parking de tamaño 5x6:
[1,1] [1,2] (1,3) (1,4) (1,5) (1,6) >>
[2,1] (2,2) (2,3) (2,4) (2,5) (2,6) >>
(3,1) (3,2) (3,3) (3,4) (3,5) (3,6) >>
[4,1] [4,2] (4,3) (4,4) (4,5) (4,6) >>
[5,1] [5,2] (5,3) (5,4) (5,5) (5,6) >>

"""

# ========== DEFINIMOS EL DOMINIO DE LAS VARIABLES ==========

# Los vehículos con congelador solo pueden ir en las plazas especiales
dominio_vehiculos_congelador = plazas_especiales

# El resto de vehículos pueden ir en cualquier plaza
dominio_vehiculos = [(i, j) for i in range(1, dimensiones[0] + 1) for j in range(1, dimensiones[1] + 1)]

# ========== DEFINIMOS LAS VARIABLES ==========

# Diccionarios para guardar las variables (vehículos)
# Transporte Sanitario Urgente (TSU): puede no tener congelador (x) o tenerlo (c)
tsu = {"x": [], "c": []}
# Transporte Individual no Urgente (TNU): puede no tener congelador (x) o tenerlo (c)
tnu = {"x": [], "c": []}

# Recorremos la lista de vehículos para categorizarlos
for i in vehiculos:
    # Separamos los datos del vehículo
    datos = i.split("-")
    # Si el vehículo es TSU
    if datos[1] == "TSU":
        # Si tiene congelador
        if datos[2] == "C":
            tsu["c"].append(i)
        # Si no tiene congelador
        else:
            tsu["x"].append(i)
    # Si el vehículo es TNU
    else:
        # Si tiene congelador
        if datos[2] == "C":
            tnu["c"].append(i)
        # Si no tiene congelador
        else:
            tnu["x"].append(i)

# Comprobamos que se han categorizado bien los vehículos
# print(tsu)
# print(tnu)

# Añadimos las variables al problema
for i in tsu["x"]:
    problem.addVariable(i, dominio_vehiculos)
for i in tsu["c"]:
    problem.addVariable(i, dominio_vehiculos_congelador)
for i in tnu["x"]:
    problem.addVariable(i, dominio_vehiculos)
for i in tnu["c"]:
    problem.addVariable(i, dominio_vehiculos_congelador)

# ========== DEFINIMOS LAS RESTRICCIONES ==========

# 1. Todo vehículo tiene que tener asignada una plaza y solo una
# 2. Dos vehículos distintos no pueden ocupar la misma plaza
problem.addConstraint(constraint.AllDifferentConstraint())

# 3. Los vehículos con congelador solo pueden ir en las plazas especiales
# Esto ya se ha tenido en cuenta al definir el dominio de las variables

# 4. Un vehículo TSU no puede tener aparcado en ninguna de las posiciones de
# su misma fila que estén a su derecha, un vehículo TNU

def salida_tsu(pos_vehiculo_tsu, *pos_vehiculos_tnu):
    """
    Comprueba si se cumple la restricción de que los TSU puedan salir sin problemas
    :param pos_vehiculo_tsu: posición del vehículo TSU
    :param pos_vehiculos_tnu: posiciones de los vehículos TNU
    """
    # Si el vehículo TSU está en la última columna, no hay ningún problema
    if pos_vehiculo_tsu[1] == dimensiones[1]:
        return True
    # Si no, comprobamos si hay algún vehículo TNU en la misma fila
    # en cualquiera de las posiciones de la derecha
    else:
        # Recorremos todas las posiciones de la derecha
        for i in range(pos_vehiculo_tsu[1] + 1, dimensiones[1] + 1):
            # Si hay algún vehículo TNU en esa posición
            if (pos_vehiculo_tsu[0], i) in pos_vehiculos_tnu:
                # No se cumple la restricción
                return False
        # Si no se ha devuelto False, entonces se cumple la restricción
        return True

# Añadimos la restricción al problema
for i in tsu["x"]:
    problem.addConstraint(salida_tsu, (i, *tnu["x"], *tnu["c"]))
for i in tsu["c"]:
    problem.addConstraint(salida_tsu, (i, *tnu["x"], *tnu["c"]))

# 5. Todo vehículo debe tener libre o bien la plaza de encima o bien la de debajo
# Si el vehículo está en la fila 1, entonces la plaza de debajo debe estar libre obligatoriamente
# Si el vehículo está en la última fila, entonces la plaza de encima debe estar libre obligatoriamente
def maniobrabilidad(*pos_vehiculos):
    """
    Comprueba si se cumple la restricción de maniobrabilidad
    :param pos_vehiculos: lista con las posiciones de los vehículos
    :return: True si se cumple la restricción, False si no
    """
    for i in pos_vehiculos:
        # Si el vehículo está en la fila 1
        if i[0] == 1:
            # Si la plaza de debajo está ocupada
            if (i[0] + 1, i[1]) in pos_vehiculos:
                # No se cumple la restricción
                return False
        # Si el vehículo está en la última fila
        elif i[0] == dimensiones[0]:
            # Si la plaza de encima está ocupada
            if (i[0] - 1, i[1]) in pos_vehiculos:
                # No se cumple la restricción
                return False
        # Si el vehículo está en cualquier otra fila
        else:
            # Si la plaza de encima o la de debajo están ocupadas
            # Al menos una de las dos tiene que estar libre
            if (i[0] - 1, i[1]) in pos_vehiculos and (i[0] + 1, i[1]) in pos_vehiculos:
                # No se cumple la restricción
                return False
 
    # Si no se ha devuelto False, entonces se cumple la restricción
    return True

# Añadimos la restricción al problema
problem.addConstraint(maniobrabilidad, vehiculos)


# Computamos la solución
solutions = problem.getSolutions()

# Computamos una solución aleatoria
# solution = problem.getSolution()

# print(solution)
# print(len(solutions))

# ========== GENERAMOS EL FICHERO DE SALIDA ==========
"""
Formato del fichero:
"N. Sol:", <número de soluciones>
<solución 1>

<solución 2>

...

Formato de la solución:
tablero en formato de matriz csv
Si la plaza está vacía, se escribe un "-"
Si la plaza está ocupada, se escribe "<id>-<tipo>-<presencia_congelador>"

Ejemplo:
"N. Sol:",302
"7-TNU-C","1-TSU-C","5-TSU-X","-","-","-"
"-","-","-","-","-","-"
"2-TNU-X","3-TNU-X","6-TNU-X","-","-","-"
"-","-","-","-","-","-"
"4-TNU-C","8-TSU-C","-","-","-","-"
"""

def write_output(path: str, solutions: list, n_print: int):
    """
    Escribe las soluciones en un fichero
    :param path: ruta del fichero
    :param solutions: lista de soluciones
    """
    with open(path, "w", encoding="utf8") as file:
        # Escribimos el número de soluciones
        file.write("\"N. Sol:\"," + str(len(solutions)) + "\n")
        # Seleccionamos n_print soluciones aleatorias
        solutions = random.sample(solutions, n_print)
        # Escribimos las soluciones
        for i in solutions:
            # i es un diccionario: las claves son los vehículos y los valores son las posiciones
            for j in range(1, dimensiones[0] + 1):
                for k in range(1, dimensiones[1] + 1):
                    # Si la plaza está vacía
                    if (j, k) not in i.values():
                        file.write("\"-\"")
                    # Si la plaza está ocupada
                    else:
                        # Recorremos los vehículos
                        for l in i.keys():
                            # Si la posición del vehículo coincide con la posición actual
                            if i[l] == (j, k):
                                # Escribimos el vehículo
                                file.write("\"" + l + "\"")
                    # Si no es la última plaza de la fila
                    if k != dimensiones[1]:
                        file.write(",")
                # Si no es la última fila
                if j != dimensiones[0]:
                    file.write("\n")
            # Si no es la última solución
            if i != solutions[-1]:
                file.write("\n\n")
            
# Escribimos las soluciones en el fichero
write_output(parking_path + ".csv", solutions, 10)
