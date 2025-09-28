# -*- coding: utf-8 -*-
"""
    Problema 1.
    
    Docente:		Matias Pastene Orellana
    Curso:			ING1312
    Seccion:		3
    Descripcion:    Código presentado en el enunciado del problema 1 de la tarea 1.
"""
# P 1.1: Variables en memoria
A = 10
B = 20
C = "Hola"
D = 3.1415
B = A
Nombre = input("Ingresa tu nomre: ")
Saludo = C + " " + Nombre + "! Cómo estás?"


# P 1.2: Intercambio de variables
C = "Hola"
D = 3.1415
Temp = None

# Comienzo de la solución propuesta

print("Previo al intercambio...")
print("Valor C: ", C)
print("Valor D: ", D)
print("Valor Temp: ", Temp)
print("-"*30)

    # Comienza el intercambio
Temp = C        # Se asigna el valor de C a Temp
C = D           # Se asigna el valor de D a C
D = Temp        # Se asigna el valor de Temp a D
Temp = None     # Se asigna el valor None a Temp

print("Posterior al intercambio...")
print("Valor C: ", C)
print("Valor D: ", D)
print("Valor Temp: ", Temp)

print("-"*30)