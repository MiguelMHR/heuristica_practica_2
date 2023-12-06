#!/usr/bin/env python
# -*- coding: utf-8 -*-

import constraint

problem = constraint.Problem()

# Tamaño del parking
dimensiones = (5, 6)
# Plazas especiales
plazas_especiales = [(1,1), (1,2), (2,1), (4,1), (5,1), (5, 2)]

# NOTA: los índices de las plazas empiezan en 1, no en 0

"""
[1,1] [1,2] (1,3) (1,4) (1,5) (1,6) >>
[2,1] (2,2) (2,3) (2,4) (2,5) (2,6) >>
(3,1) (3,2) (3,3) (3,4) (3,5) (3,6) >>
[4,1] [4,2] (4,3) (4,4) (4,5) (4,6) >>
[5,1] [5,2] (5,3) (5,4) (5,5) (5,6) >>

"""

# Los vehículos con congelador solo pueden ir en las plazas especiales
dominio_vehiculos_congelador = plazas_especiales

# El resto de vehículos pueden ir en cualquier plaza
dominio_vehiculos = [(i, j) for i in range(1, dimensiones[0] + 1) for j in range(1, dimensiones[1] + 1)]

# Diccionarios para guardar las variables (vehículos)
# Transporte Sanitario Urgente (TSU): puede no tener congelador (x) o tenerlo (c)
tsu = {"x": [], "c": []}
# Transporte Individual no Urgente (TNU): puede no tener congelador (x) o tenerlo (c)
tnu = {"x": [], "c": []}

# Lista con todos los vehículos
vehiculos = []

# Creamos las variables
tsu["x"].append("5-TSU-X")
tsu["c"].append("1-TSU-C")
tsu["c"].append("8-TSU-C")
tnu["x"].append("2-TNU-X")
tnu["x"].append("3-TNU-X")
tnu["x"].append("6-TNU-X")
tnu["c"].append("4-TNU-C")
tnu["c"].append("7-TNU-C")

# Añadimos los vehículos a la lista
for i in tsu["x"]:
    vehiculos.append(i)
for i in tsu["c"]:
    vehiculos.append(i)
for i in tnu["x"]:
    vehiculos.append(i)
for i in tnu["c"]:
    vehiculos.append(i)

# Añadimos las variables al problema
for i in tsu["x"]:
    problem.addVariable(i, dominio_vehiculos)
for i in tsu["c"]:
    problem.addVariable(i, dominio_vehiculos_congelador)
for i in tnu["x"]:
    problem.addVariable(i, dominio_vehiculos)
for i in tnu["c"]:
    problem.addVariable(i, dominio_vehiculos_congelador)

# Restricciones

# 1. Todo vehículo tiene que tener asignada una plaza y solo una
problem.addConstraint(constraint.AllDifferentConstraint())

# 2. Dos vehículos distintos, no pueden ocupar la misma plaza
# La anterior restricción ya lo impone

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
solution = problem.getSolution()

print(solution)
print(len(solutions))

# TODO: Leer datos de un fichero y escribir la solución en otro fichero