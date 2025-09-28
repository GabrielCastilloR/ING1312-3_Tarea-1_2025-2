# -*- coding: utf-8 -*-
__docformat__ = "google"
"""
.. include:: ../README.md
"""
"""description:
Problema 2 Extra.

Autor:			Gabriel Andres Castillo Rosales
RUT:			19.679.401-8
Docente:		Matias Pastene Orellana
Curso:			ING1312
Seccion:		3
Descripcion: 	Módulo extra para P2 de tarea 1. 
				Simulación de la escalera siendo inundada y el escape de los gatos
				usando POO, instanciación, iterables y algunas librerias adicionales.
				Se ignora la condición "sólo puede haber un gato por escalón" para simplificar un poco los condicionales,
				pero dado el código usado, esta debería cumplirse de todas formas para la configuración básica de la simulación. No está testeado para las configs isRandomized=True, isFair=True
				Se hace entrega del módulo listo para ejecutar desde el depurador.
Notas Adicionales:
	- Se usa la convención camelCase para nombrar las variables y funciones.
	- Se usa la convención PascalCase para nombrar objetos.
	- Se usa declaración de variables por compresión cuando se considera conveniente.
	- El código tiene una mezcla de inglés y español, ya que aprendí a usar Python de forma autodidacta. (Youtube, StackExchange, PythonDocs y mucho Google)
	- Las líneas marcadas con "#Sanity Check" cumplen la función de prevenir errores fortuitos.
	- Todas las funciones y objetos tienen comentarios con sus respectivas descripciones.
	- Algunas líneas tienen comentarios con información adicional relevante.
 Dependencias:
	- time
	- random
	- sys
"""
import time
import random, sys # Importa las librerias adicionales random y sys


def getValidInput(prompt, dtype='str', gate=0):
	"""<func> getValidInput(prompt, dtype) : Obtiene un input válido dependiendo del tipo de dato y el valor del mismo.

	Args:
		prompt (str): Texto que se mostrará en la consola para pedir un input
		dtype (str, optional): Tipo de dato deseado. Por defecto es 'str'.
		gate (int, optional): Define un umbral inferior para los valores númericos.

	Raises:
		ValueError: Valor inesperado
		TypeError: Tipo de dato inesperado

	Returns:
		__dtype__: Devuelve el input del usuario en el tipo de dato deseado y con las restricciones de valor deseadas
	""" 
	# Se usa un ciclo while para repetir la interacción hasta que sea válida
	isValid = False
	while not isValid:
		# Se usa el método try-except para el manejo de excepciones
		try:
			match dtype:
				case 'str': # Condiciones para un string válido
					value = str(input(prompt))
					isValid = True
					return value
				case 'int': # Condiciones para un int válido. Para los fines de este módulo siempre deben ser positivos y mayores que cero.
					value = int(input(prompt))
					if value <= gate: # Fuerza la excepción ValueError, ya que el dato ingresado es <= 0
						raise ValueError
					else:
						isValid = True
						return value
				case 'bool': # Condiciones para un bool válido. boolDict se utiliza para añadir localización
					boolDict = {'true':True, 't':True,'si':True, 's':True, 'yes':True, 'y':True, 'v':True, 'verdad':True, 'verdadero':True, '1':True,
					'false':False, 'f':False, 'falso':False, 'falsa':False, 'no':False, 'n':False, '0':False}
					key = str(input(prompt)).lower()
					value = boolDict.get(key)
					if value != None:
						isValid = True
						return value
					else:
						raise TypeError # Fuerza la excepción TypeError, para evitar problemas conocidos del método __bool__()
		except TypeError:
			print('ERROR: El dato ingresado no es un {}! Porfavor ingrese un {}.'.format(dtype, dtype))
		except ValueError:
			print('ERROR: El valor ingresado es inválido! Porfavor ingrese un numero entero mayor que {}.'.format(gate))

class Stair:
	"""<class> Stair : Objeto que define la escalera y maneja la ejecución de la simulación. Solo definir 1 instancia

		Métodos:
			- __init__
			- printStairState
			- raiseWater
			- updateCats
			- CatCount
			- update
	"""    
	def __init__(self, stepsTotal, waterLevel=0, cats=None):
		"""<method> __init__(self, stepsTotal, waterLevel=0, cats=None): Inicializa una instancia del objeto Stair

		Args:
			stepsTotal (int): Cantidad de escalones total
			waterLevel (int, optional): Posicion Inicial de la marea. Por defecto es 0.
			cats (list(typeof(<class Cat>)), optional): Lista que contiene instancias del objeto Cat.Por defecto es None.
		"""     
		self.N = stepsTotal #Cantidad de escalones
		self.dTime = 0 #Tiempo Inicial en segundos, siempre será 0
		self.waterPos = waterLevel #Posición de la marea, por defecto es 0
		# Verifica que se haya entregado un valor para cats y define self.cats y self.isCatsVoid
		if cats != None: 
			self.cats = cats
			self.isCatsVoid = False
		else:
			self.cats = []
			self.isCatsVoid = True
	
	def printStairState(self, catGroups, counts, isFinal=False):
		"""<method> printStairState(self, catGroups, counts, isFinal=False) : Imprime el estado actual de la simulación

		Args:
			catGroups (_type_): _description_
			counts (_type_): _description_
			isFinal (bool, optional): _description_. Defaults to False.
		"""		    
		#Convierte self.dTime a formato hh:mm:ss
		mins = int(self.dTime//60)
		secs = int(self.dTime - 60*mins)
		hours = int(mins//60)
		mins -= 60*hours

		ver = 'Actual'
		if isFinal:
			ver = 'Final'
		
		#Comienza la impresión del estado de la simulación
		print('+'+'-'*100+'+')
		print('Tiempo {}(hh:mm:ss): {}:{}:{}'.format(ver, hours, mins, secs))
		print('Posicion de la marea: escalón n° {}'.format(self.waterPos))
		print('N° Gatitos Activos: 	{}'.format(counts[0]))
		if counts[0] > 0: #Añade formato condicional para mostrar los gatos que correspondan
			for cat in catGroups[0]:
				print('	-> ID: {} - Posición: {}'.format(cat.name, cat.pos))
		print('N° Gatitos Hundidos: 	{}'.format(counts[1]))
		if counts[1] > 0: #Añade formato condicional para mostrar los gatos que correspondan
			for cat in catGroups[1]:
				print('	-> ID: {} - Posición: {}'.format(cat.name, cat.pos))
		print('N° Gatitos A Salvo: 	{}'.format(counts[2]))
		if counts[2] > 0: #Añade formato condicional para mostrar los gatos que correspondan
			for cat in catGroups[2]:
				print('	-> ID: {}'.format(cat.name))
		print('+'+'-'*100+'+')
	
	def parseCats(self):
		"""<method> parseCats(self) : Separa y cuenta las instancias de Cat en self.cats según su estado.

		Returns:
			array: [catGroups, counters] - Donde "catGroups" es una lista de 3 listas con instancias de Cat separadas por estado y "counters" la lista de los largos de estas.
		"""		
		catGroups = [[],[],[]]
		counters = [0, 0, 0]
		for cat in self.cats:
			match cat.status:
				case 'active':
					catGroups[0].append(cat)
					counters[0] += 1
				case 'sunk':
					catGroups[1].append(cat)
					counters[1] += 1
				case 'safe':
					catGroups[2].append(cat)
					counters[2] += 1
		
		return [catGroups, counters]

	def update(self, moveCats=1, moveWater=1, dt=10, isFair=True, isRandomized=False):
		"""<method> update(self, moveCats=1, moveWater=1, dt=10, isFair=True, isRandomized=False) : Actualiza la simulación

		Args:
			moveCats (int, optional): Cantidad de escalones que recorren los gatos. Defaults to 1.
			moveWater (int, optional): Cantidad de escalones que recorre la marea. Defaults to 1.
			dt (int, optional): Intervalo de tiempo elapsado. Defaults to 10.
			isFair (bool, optional): Condicional de movimiento justo. Defaults to True.
			isRandomized (bool, optional): Condicional de movimiento aleatorio. Defaults to False.

		Returns:
			bool: Determina si la simulación continua. Para False, se detiene la simulación
		"""		

		# Verifica si está usando la configuración aleatoria
		if isRandomized:
			# Verifica si está usando la configuración de movimiento justo
			if isFair:
				moveCats = random.randint(1, (self.N))
				moveWater = moveCats
			else:
				moveCats = random.randint(1, (self.N))
				moveWater = random.randint(1, (self.N))
		
		# Mueve la marea y avanza el tiempo
		self.waterPos += moveWater
		self.dTime += dt
		
		# Separa y cuenta los gatos por cat.status
		parsed = self.parseCats()
		catGroups, counters = parsed[0], parsed[1]
		
		# Mueve a los gatos activos
		if counters[0] != 0:
			for cat in catGroups[0]:
				newPos = cat.pos + moveCats
				if newPos > self.N:
					cat.setStatus('safe')
					cat.setPosition(self.N + 1)
					catGroups[2].append(cat)
					counters[2] += 1
					catGroups[0].remove(cat)
					counters[0] -= 1
				
				elif newPos <= self.waterPos:
					cat.setStatus('sunk')
					cat.setPosition(newPos)
					catGroups[1].append(cat)
					counters[1] += 1
					catGroups[0].remove(cat)
					counters[0] -= 1
				else:
					cat.setPosition(newPos)

		if (self.waterPos >= self.N):
			print(" --- MSG: La marea ha alcanzado el final de la escalera... --- ")
			self.printStairState(catGroups, counters, isFinal=True)
			return False

		elif counters[0] == 0:
			print(" --- MSG: No quedan gatos activos ---")
			self.printStairState(catGroups, counters, isFinal=True)
			return False

		else:
			self.printStairState(catGroups, counters, isFinal=False)
			time.sleep(dt)
			return True



class Cat: 
	"""<class> Cat : Objeto que representa a un gato.

		Métodos:
			- __init__
			- setStatus
			- setPosition
	"""
	def __init__(self, name, pos, status='active'):
		"""<method> Uso: Cat(name, pos, status='active') : Inicializa una instancia del objeto Cat.

		Args:
			name (string): Nombre del gato
			pos (int): Posición en la escalera del gato.
			status (str, optional): Estado del gato. Puede ser ('active', 'sunk', 'safe'). Por defecto es 'active'.
		"""     
		self.name, self.pos, self.status, self.wasStatusChangedLast = name, pos, status, False
	
	def setStatus(self, new):
		"""<method> Uso: self.setStatus(new) : Cambia el valor de Cat.status

		Args:
			new (string): Nuevo estado del gato. Puede ser ('active', 'sunk', 'safe')
		"""     
		self.status = new
	def setPosition(self, new):
		"""<method> Uso: self.setPosition(new) : Cambia el valor de Cat.pos

		Args:
			new (int): Nueva posición del gato en la escalera. Debe ser un entero positivo no nulo.
		"""     
		self.pos = new

def main(): 
	"""<func> main() : Función de ejecución primaria. Al llamarla se ejecuta el módulo.
	"""
	# Mensaje de bienvenida
	print('+'+'='*100+'+\n'+'Bienvenido! Esto es un simulador extra para el problema 2 de la tarea 1.\n'+'+'+'='*100+'+')
	print('Comenzando configuracion...')

	# Se obtiene un input para la cantidad de escalones
	nSteps = getValidInput('¿Cuantos escalones tiene la escalera? respuesta: ', 'int')
	print(('Creando {} escalones...\n'+'+'+'-'*100+'+').format(str(nSteps)))
	
	# Se obtiene un input válido para la cantidad de gatos, se reintentará hasta que el usuario finalice la aplicación o la cantidad de gatos ingresada sea menor que la cantidad de escalones
	isCatsLess = False
	while not isCatsLess:
		nCats = getValidInput('¿Cuantos gatitos hay? Recuerde que debe ser menos que la cantidad de escalones\nrespuesta: ', 'int')
		print('+'+'-'*100+'+')
		if nCats < nSteps:
			isCatsLess = True
		else:
			print('ERROR: Hay mas gatitos que escalones! No podemos manejar tanta ternura')
			print('Porfavor reintente...')
			nCats = None
			isCatsLess = False
	
	# Se cobfigura la posición inicial de la marea, por defecto es 0
	isCustomWater = getValidInput('¿Desea fijar una posición inicial para la marea?(y/n) ', 'bool')
	if isCustomWater:
		isWaterLess = False
		# Analogamente al input para la cantidad de gatos, se reintentará este input hasta que el usuario finalice la aplicación o la posición inicial de la marea sea válida.
		while not isWaterLess:
			waterPos0 = getValidInput('Ingrese el escalón donde partirá la marea: ', 'int')
			print('+'+'-'*100+'+')
			if waterPos0 < (nSteps - nCats):
				isWaterLess = True
			else:
				print('ERROR: El valor ingresado es demasiado alto, no se podrá hacer la configuración inical correctamente...')
				print('Porfavor reintente...')
				waterPos0 = 0
				isWaterLess = False
	else:
		waterPos0 = 0
	
	# Da la opción de nombrar a los gatos y se crea la lista de objetos Cat
	areNamed = getValidInput('¿Desea nombrar a sus gatitos?(y/n) ', 'bool')
	print('+'+'-'*100+'+')
	catList = []

	for i in range(0, nCats):
		if areNamed:
			name = getValidInput('Ingrese el nombre del gatito n° {}: '.format(str(i+1)), 'str')
		else:
			name = 'GATO #{}'.format(str(i+1))
		pos = waterPos0 + i + 1
		catList.append(Cat(name, pos, 'active'))
	
	# Se crea la instancia stair del objeto Stair con la configuración dada
	stair = Stair(nSteps, waterLevel=waterPos0, cats=catList)
	catMove, waterMove, dt = 1, 1, 10

	# Comienza la configuración de la simulación
	isRandomized, isFair = None, None
	isCustomConditions = getValidInput('¿Desea usar configuraciones avanzadas para el tiempo y movimientos de la marea y gatitos?(y/n) ', 'bool')
	print('+'+'-'*100+'+')
	if isCustomConditions: # Se usan condiciones personalizadas
		isFair = getValidInput('¿Desea que el moviemiento sea justo? Es decir, que la marea y los gatitos se muevan la misma distancia. (y/n) ', 'bool')
		print('+'+'-'*100+'+')
		isRandomized = getValidInput('La opción de movimiento aleatorio utiliza intervalos de tiempo fijos de 10 segundos.\nAl activarla no podrá configurar el intervalo de tiempo entre movimientos.\n¿Desea que el moviemiento sea aleatorio?(y/n) ', 'bool')
		print('+'+'-'*100+'+')
		if not isRandomized: # Configuración con movimiento NO aleatorio
			if isFair: # Configuración con movimiento justo, es decir, la marea y los gatos se mueven la misma distancia
				dx = getValidInput('Como ha seleccionado movimiento justo, la marea y los gatitos se moverán la misma distancia y esta debe ser un numero entero positivo.\nIngrese la distancia del movimiento: ', 'int')
				print('+'+'-'*100+'+')
				catMove, waterMove = dx, dx
				dt = getValidInput('Ingrese el intervalo de tiempo entre movimientos en segundos. dt: ', 'int')
				print('+'+'-'*100+'+')
			else: # Configuración sin movimiento justo
				print('Como no ha seleccionado movimiento justo, deberá configurar el movimiento de la marea y los gatitos de forma separada y estas deben ser numeros enteros positivos.')
				catMove = getValidInput('Ingrese la distancia del movimiento de los gatitos: ', 'int')
				print('+'+'-'*100+'+')
				waterMove = getValidInput('Ingrese la distancia del movimiento de la marea: ', 'int')
				print('+'+'-'*100+'+')
				dt = getValidInput('Ingrese el intervalo de tiempo entre movimientos en segundos: ', 'int')
		else: # Configuración con movimiento aleatorio
			isRandomized, isFair = False, False
	
	# Se imprime un resumen de las configuraciones de la simulación
	print('+'+'='*100+'+')
	print('+ '+'Resumen de la configuración:')
	print('+ '+'N° escalones = {}'.format(nSteps))
	print('+ '+'N° Gatitos = {}'.format(nCats))
	print('+ '+'Config Avanzada Activada? [{}]'.format(isCustomConditions))
		#Formato Condicional dependiente de la existencia de configuraciones avanzadas
	if isCustomConditions:
		print('+ '+'Mov. Justo? [{}]'.format(isFair))
		print('+ '+'Distancia Mov. Aleatoria? [{}]'.format(isRandomized))
		if not isRandomized:
			print('+ '+'Distancia Mov. Marea = {} escalones por intervalo'.format(waterMove))
			print('+ '+'Distancia Mov. Gatitos = {} escalones por intervalo'.format(catMove))
			print('+ '+'Intervalo entre Mov. = {} segundos'.format(dt))
		else:
			print('+ '+'Distancia Mov. Marea = Aleatoria')
			print('+ '+'Distancia Mov. Gatitos = Aleatoria')
			print('+ '+'Intervalo entre Mov. = 10 segundos')
	else:
		print('+ '+'Distancia Mov. Marea = 1 escalón por intervalo')
		print('+ '+'Distancia Mov. Gatitos = 1 escalón por intervalo')
		print('+ '+'Intervalo entre Mov. = 10 segundos')
	
	# Mensaje de comienzo de la simulación
	print('+'+'='*100+'+')
	print('Comenzando la simulación...')
	print('+'+'='*100+'+')
	
	# Comienzo de la simulación
	isRunning = True
	isFirst = True
	while isRunning:
		if isFirst:
			parsed = stair.parseCats()
			stair.printStairState(parsed[0], parsed[1], isFinal=False)
			isFirst = False
			time.sleep(dt)
		isRunning = stair.update(moveCats=catMove, moveWater=waterMove, dt=dt, isFair=isFair, isRandomized=isRandomized) #stair.update devuelve un bool que será False si y sólo si se cumplen las condiciones necesarioas para finalizar la simulación

if __name__ == "__main__":
	main()