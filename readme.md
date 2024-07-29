# Práctica 2 - Satisfacción de restricciones y búsqueda heurística

## Introducción
Este trabajo consiste en la implementación del algoritmo A* para resolver un problema de búsqueda heurística

## Como instalar las librerías de nuestro trabajo

Debemos instalar python3 en Linux con el siguiente comando:

`sudo apt install python3 && sudo apt install python3-pip`

Debemos instalar las librerías del archivo requirements.txt

`pip install -r requirements.txt`

## Recomendación

A la hora de trabajar en python, para no mezclar dependencias ni librerías instaladas evitando así posibles conflictos, es recomendable usar un venv para aislar los proyectos python

Primero, debemos instalar un paquete que nos permite la manipulación del venv:

`sudo apt install python3-venv`

Si se está trabajando desde Windows, se deberá descargar el instalador desde la web de Python:

[https://www.python.org/downloads/]()

Se puede crear un venv mediante el siguiente comando:

`python3 -m venv .venv`

Para poder acceder al venv, se debe introducir el siguiente comando:

`source ./.venv/bin/activate`

Desde Windows, se debe acceder de la siguiente manera:

`venv\Scripts\activate.bat `

Para poder salir del venv, se debe introducir lo siguiente:

`deactivate`

## Notas adicionales:

Para poder visualizar de manera óptima los comentarios de nuestro proyecto, ya que se verán sin color y de la siguiente forma (#!, #?), se deberá instalar una extensión de Visual Studio llamada "**Better comments**"

Para poder ejecutar un script .sh, se deberá abrir una Bash (en Windows se puede abrir la Bash de Git por ejemplo) y usar el siguiente comando:

`sh ./parte-X/YYY-calls.sh`

donde X corresponde a la parte de la práctica (1 o 2) y donde YYY corresponde al nombre del .sh (CSP para parte 1 y ASTAR para parte 2)
