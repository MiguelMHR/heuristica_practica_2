# Práctica 2 - Satisfacción de restricciones y búsqueda heurística

## Como instalar las librerías de nuestro trabajo

Debemos instalar python3 en Linux con el siguiente comando:

`sudo apt install python3 && sudo apt install python3-pip`

Debemos instalar las librerías del archivo requirements.txt

`pip install -r requirements.txt`

## Recomendación

A la hora de trabajar en python, para no mezclar dependencias ni librerías instaladas evitando así posibles conflictos, es recomendable usar un venv para aislar los proyectos python

Primero, debemos instalar un paquete que nos permite la manipulación del venv:

`sudo apt install python3-venv`

Se puede crear un venv mediante el siguiente comando:

`python3 -m venv .venv`

Para poder acceder al venv, se debe introducir el siguiente comando:

`source ./.venv/bin/activate`

Para poder salir del venv, se debe introducir lo siguiente:

`deactivate`
