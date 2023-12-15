# FORMA DE EJECUTAR EL SCRIPT EN TERMINAL:
# (desde el directorio /parte_2/)
# sh ASTAR-calls.sh

##### EJECUCIÓN DE TEST INICIAL -> EJEMPLO ENUNCIADO CON UNA MATRIZ 10X10 #####
# NOTA: este test tarda demasiado en ejecutarse,así que se ha preferido dejar comentado y no 
#       tomarlo en consideración al no conseguir ejecutarse en un tiempo razonable
# python ASTARTraslados.py ./ASTAR-tests/mapa_enunciado.csv 

##### EJECUCIÓN DEL PRIMER TEST -> EJEMPLO FACTIBLE CON UNA MATRIZ 5X5 #####
python ASTARTraslados.py ./ASTAR-tests/mapa1.csv 1
python ASTARTraslados.py ./ASTAR-tests/mapa1.csv 2
python ASTARTraslados.py ./ASTAR-tests/mapa1.csv 3
python ASTARTraslados.py ./ASTAR-tests/mapa1.csv 4
python ASTARTraslados.py ./ASTAR-tests/mapa1.csv 5

##### EJECUCIÓN DEL SEGUNDO TEST -> EJEMPLO FACTIBLE  1 N y 2 C #####
python ASTARTraslados.py ./ASTAR-tests/mapa2.csv 1
python ASTARTraslados.py ./ASTAR-tests/mapa2.csv 2
python ASTARTraslados.py ./ASTAR-tests/mapa2.csv 3
python ASTARTraslados.py ./ASTAR-tests/mapa2.csv 4
python ASTARTraslados.py ./ASTAR-tests/mapa2.csv 5

##### EJECUCIÓN DEL TERCER TEST -> EJEMPLO FACTIBLE MUCHOS CONTAGIOSOS #####
python ASTARTraslados.py ./ASTAR-tests/mapa3.csv 1
python ASTARTraslados.py ./ASTAR-tests/mapa3.csv 2
python ASTARTraslados.py ./ASTAR-tests/mapa3.csv 3
python ASTARTraslados.py ./ASTAR-tests/mapa3.csv 4
python ASTARTraslados.py ./ASTAR-tests/mapa3.csv 5

##### EJECUCIÓN DEL CUARTO TEST -> EJEMPLO FACTIBLE MUCHOS NO CONTAGIOSOS #####
python ASTARTraslados.py ./ASTAR-tests/mapa4.csv 1
python ASTARTraslados.py ./ASTAR-tests/mapa4.csv 2
python ASTARTraslados.py ./ASTAR-tests/mapa4.csv 3
python ASTARTraslados.py ./ASTAR-tests/mapa4.csv 4
python ASTARTraslados.py ./ASTAR-tests/mapa4.csv 5

##### EJECUCIÓN DEL QUINTO TEST -> EJEMPLO FACTIBLE 2 PARKINGS #####
python ASTARTraslados.py ./ASTAR-tests/mapa5.csv 1
python ASTARTraslados.py ./ASTAR-tests/mapa5.csv 2
python ASTARTraslados.py ./ASTAR-tests/mapa5.csv 3
python ASTARTraslados.py ./ASTAR-tests/mapa5.csv 4
python ASTARTraslados.py ./ASTAR-tests/mapa5.csv 5

##### EJECUCIÓN DEL SEXTO TEST -> EJEMPLO FACTIBLE TODO CENTROS Y PACIENTES #####
python ASTARTraslados.py ./ASTAR-tests/mapa6.csv 1
python ASTARTraslados.py ./ASTAR-tests/mapa6.csv 2
python ASTARTraslados.py ./ASTAR-tests/mapa6.csv 3
python ASTARTraslados.py ./ASTAR-tests/mapa6.csv 4
python ASTARTraslados.py ./ASTAR-tests/mapa6.csv 5

#### EJECUCIÓN DEL TEST 7 -> EJEMPLO FACTIBLE CON RECARGA DE ENERGÍA #####
python ASTARTraslados.py ./ASTAR-tests/mapa7.csv 1
python ASTARTraslados.py ./ASTAR-tests/mapa7.csv 2
python ASTARTraslados.py ./ASTAR-tests/mapa7.csv 3
python ASTARTraslados.py ./ASTAR-tests/mapa7.csv 4
python ASTARTraslados.py ./ASTAR-tests/mapa7.csv 5


####### CASOS IMPOSIBLES ########

##### EJECUCIÓN DEL TEST 8 -> EJEMPLO SIN SOLUCIÓN NO HAY PARKING #####
python ASTARTraslados.py ./ASTAR-tests/mapa8.csv 1
python ASTARTraslados.py ./ASTAR-tests/mapa8.csv 2
python ASTARTraslados.py ./ASTAR-tests/mapa8.csv 3
python ASTARTraslados.py ./ASTAR-tests/mapa8.csv 4
python ASTARTraslados.py ./ASTAR-tests/mapa8.csv 5

# ##### EJECUCIÓN DEL TEST 9 -> EJEMPLO SIN SOLUCIÓN CAMINO BLOQUEADO #####
python ASTARTraslados.py ./ASTAR-tests/mapa9.csv 1
python ASTARTraslados.py ./ASTAR-tests/mapa9.csv 2
python ASTARTraslados.py ./ASTAR-tests/mapa9.csv 3
python ASTARTraslados.py ./ASTAR-tests/mapa9.csv 4
python ASTARTraslados.py ./ASTAR-tests/mapa9.csv 5

# ##### EJECUCIÓN DEL TEST 10 -> EJEMPLO SIN SOLUCIÓN VEHÍCULO SIN CARGA #####
python ASTARTraslados.py ./ASTAR-tests/mapa10.csv 1
python ASTARTraslados.py ./ASTAR-tests/mapa10.csv 2
python ASTARTraslados.py ./ASTAR-tests/mapa10.csv 3
python ASTARTraslados.py ./ASTAR-tests/mapa10.csv 4
python ASTARTraslados.py ./ASTAR-tests/mapa10.csv 5

# ##### EJECUCIÓN DEL TEST 11 -> EJEMPLO SIN SOLUCIÓN VEHÍCULO SIN CARGA RECOGIENDO A ALGUNOS #####
python ASTARTraslados.py ./ASTAR-tests/mapa11.csv 1
python ASTARTraslados.py ./ASTAR-tests/mapa11.csv 2
python ASTARTraslados.py ./ASTAR-tests/mapa11.csv 3
python ASTARTraslados.py ./ASTAR-tests/mapa11.csv 4
python ASTARTraslados.py ./ASTAR-tests/mapa11.csv 5
