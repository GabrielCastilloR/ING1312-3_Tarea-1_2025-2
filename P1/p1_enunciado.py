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
print("Previo al intercambio...")
print("Valor C: ", C)
print("Valor D: ", D)
print("Valor Temp: ", Temp)
print("-"*30)

#Comienza el intercambio
Temp = C
C = D
D = Temp
Temp = None

print("Posterior al intercambio...")
print("Valor C: ", C)
print("Valor D: ", D)
print("Valor Temp: ", Temp)

print("-"*30)
