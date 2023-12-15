# FORMA DE EJECUTAR EL SCRIPT EN TERMINAL:
# sh parte_2/ASTAR-calls.sh

##### EJECUCIÓN DE TEST INICIAL -> EJEMPLO ENUNCIADO CON UNA MATRIZ 10X10 #####
# NOTA: este test tarda demasiado en ejecutarse,así que se ha preferido dejar comentado y no 
#       tomarlo en consideración al no conseguir ejecutarse en un tiempo razonable
#python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa_enunciado.csv 

##### EJECUCIÓN DEL PRIMER TEST -> EJEMPLO FACTIBLE CON UNA MATRIZ 5X5 #####
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa1.csv 1
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa1.csv 2
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa1.csv 3
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa1.csv 4
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa1.csv 5

##### EJECUCIÓN DEL SEGUNDO TEST -> EJEMPLO FACTIBLE  1 N y 2 C #####
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa2.csv 1
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa2.csv 2
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa2.csv 3
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa2.csv 4
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa2.csv 5

##### EJECUCIÓN DEL TERCER TEST -> EJEMPLO FACTIBLE MUCHOS CONTAGIOSOS #####
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa3.csv 1
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa3.csv 2
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa3.csv 3
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa3.csv 4
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa3.csv 5

##### EJECUCIÓN DEL CUARTO TEST -> EJEMPLO FACTIBLE MUCHOS NO CONTAGIOSOS #####
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa4.csv 1
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa4.csv 2
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa4.csv 3
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa4.csv 4
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa4.csv 5

##### EJECUCIÓN DEL QUINTO TEST -> EJEMPLO FACTIBLE 2 PARKINGS #####
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa5.csv 1
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa5.csv 2
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa5.csv 3
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa5.csv 4
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa5.csv 5

##### EJECUCIÓN DEL SEXTO TEST -> EJEMPLO FACTIBLE TODO CENTROS Y PACIENTES #####
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa6.csv 1
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa6.csv 2
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa6.csv 3
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa6.csv 4
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa6.csv 5

######## CASOS IMPOSIBLES ########

##### EJECUCIÓN DEL TEST -> EJEMPLO SIN SOLUCIÓN NO HAY PARKING #####
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa7.csv 1
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa7.csv 2
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa7.csv 3
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa7.csv 4
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa7.csv 5

##### EJECUCIÓN DEL SEGUNDO TEST -> EJEMPLO SIN SOLUCIÓN CAMINO BLOQUEADO #####
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa7.csv 1
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa8.csv 2
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa8.csv 3
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa8.csv 4
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa8.csv 5

##### EJECUCIÓN DEL TEST -> EJEMPLO SIN SOLUCIÓN VEHÍCULO SIN CARGA #####
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa9.csv 1
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa9.csv 2
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa9.csv 3
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa9.csv 4
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa9.csv 5

##### EJECUCIÓN DEL TEST -> EJEMPLO SIN SOLUCIÓN VEHÍCULO SIN CARGA RECOGIENDO A ALGUNOS #####
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa10.csv 1
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa10.csv 2
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa10.csv 3
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa10.csv 4
python parte_2/ASTARTraslados.py parte_2/ASTAR-tests/mapa10.csv 5

