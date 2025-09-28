# -*- coding: utf-8 -*-
__docformat__ = "google" #Da formato de los docstrings a pdoc3
"""Problema 2.
    
    Autor:			Gabriel Andres Castillo Rosales
    RUT:			19.679.401-8
    Docente:		Matias Pastene Orellana
    Curso:			ING1312
    Seccion:		3
    Descripcion:    Solución base P2 de tarea 1.
    """

s0 = 'GATO 1'
s1 = 'GATO 2'
s2 = 'GATO 3'

s3 = None
s4 = None
s5 = None

import time
for i in range(3):
	# TO DO
		#Inicio código añadido por Gabriel Andrés Castillo Rosales
	dt = 10*(i + 1)
	match i:
		case 0:
			print('+'+'-'*50+'+')
			print('Estado inicial:')
			print('Escalón 1: ', s0)
			print('Escalón 2: ', s1)
			print('Escalón 3: ', s2)
			print('Escalón 4: ', s3)
			print('Escalón 5: ', s4)
			print('Escalón 6: ', s5)
			time.sleep(10)
			s3 = s2
			s2 = s1
			s1 = s0
			s0 = 'Hundido'
		case 1:
			s4 = s3
			s3 = s2
			s2 = s1
			
			s0 = 'Hundido'
			s1 = s0
		case 2:
			s5 = s4
			s4 = s3
			s3 = s2
			
			s0 = 'Hundido'
			s1 = s0
			s2 = s1
		case _:
			break
		
	print('+'+'-'*50+'+')
	print('Tiempo elapsado: {} segundos.'.format(str(dt)))
	print('Escalón 1: ', s0)
	print('Escalón 2: ', s1)
	print('Escalón 3: ', s2)
	print('Escalón 4: ', s3)
	print('Escalón 5: ', s4)
	print('Escalón 6: ', s5)
		#Fin código añadido por Gabriel Andrés Castillo Rosales
	time.sleep(10)