# -*- coding: utf-8 -*-
__docformat__ = "google"
"""
.. include:: ../README.md
"""

"""
<section> #Problema 2 Extra.

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


def getValidInput(prompt, dtype='str'):
	"""<func> getValidInput(prompt, dtype='str') : Obtiene un input válido dependiendo del tipo de dato y el valor del mismo.

	Args:
		prompt (str): Texto que se mostrará en la consola para pedir un input
		dtype (str, optional): Tipo de dato deseado. Por defecto es 'str'.

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
					if value <= 0: # Fuerza la excepción ValueError, ya que el dato ingresado es <= 0
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
			print('ERROR: El valor ingresado es inválido! Porfavor ingrese un numero entero positivo.')

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
	
	def printStairState(self, isFinal=False):
		"""<method> Uso: self.printStairState(**isFinal=False): Imprime el estado actual de la simulación

		Args:
			isFinal (bool, optional): Define si se mostrará el resumen final. Por defecto es False.
		"""     
		#Convierte self.dTime a formato hh:mm:ss
		mins = int(self.dTime//60)
		secs = int(self.dTime - 60*mins)
		hours = int(mins//60)
		mins -= 60*hours
		

		counts = self.CatCount()# Contiene una lista de la forma [activeCount, sunkCount, safeCount]
		catGroups = [[],[],[]] # Contiene una matriz irregular de tamaño 3xn. Cada columna contiene una lista de n instancias únicas del objeto Cat que tienen el mismo valor para la propiedad status
		for cat in self.cats:
			match cat.status:
				case 'active':
					catGroups[0].append(cat)
				case 'sunk':
					catGroups[1].append(cat)
				case 'safe':
					catGroups[2].append(cat)

		# Añade formato condicional al texto en la línea 125
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
		
	def raiseWater(self, n, dt):
		"""<method> Uso: self.raiseWater(n, dt) : Mueve la marea n escalones en un intervalo de tiempo dt.

		Args:
			n (int): Cantidad de escalones que avanza la marea.
			dt (int, float): Intervalo de tiempo en segundos. https://docs.python.org/3/library/time.html#time.sleep para más información

		Returns:
			bool: Determina si la simulación termina.
		"""     
		time.sleep(dt) #Se hace la espera correspondiente
		# Se actualizan las propiedades correspondientes
		self.dTime += dt
		self.waterPos += n

		# Se verifica si la marea alcanzó el final de la escalera o no
		if self.waterPos >= self.N: #La marea llegó al final de la escalera
			print('La marea ha hundido la escalera por completo!')
			self.printStairState()
			print('+'+'='*100+'+')
			print('Finalizando la Simulación...')
			return False # Devuelve False para detener la simulación

		else: #La marea no ha alcanzado el final de la escalera
			self.updateCats() #Se actualizan las propiedades pos y status de cada gato
			counts = self.CatCount() #Se obtienen conteos para cada status(active, sunk, safe)
			
			total = len(self.cats) #Sanity Check // Se verifica que no se hayan perdido gatos
			if total != (counts[0] + counts[1] + counts[2]):
				print('CRITICAL ERROR MSG: Perdida de datos inesperada... Finalizando aplicacion...')
				return False # Devuelve False para detener la simulación
			else: ##Sanity Check // No se han perdido gatos, por ende se continúa
				if counts[1] == total: # Sí todos los gatos se hundieron
					print('Oh no! Todos los gatitos se hundieron :c ...')
					self.printStairState(isFinal=True)
					print('+'+'='*100+'+')
					print('Finalizando la Simulación...')
					return False # Devuelve False para detener la simulación
				elif counts[2] == total: #Sí todos los gatos se salvaron
					print('Felicidades! Todos los gatitos han escapado!')
					self.printStairState(isFinal=True)
					print('+'+'='*100+'+')
					print('Finalizando la Simulación...')
					return False # Devuelve False para detener la simulación
				elif counts[0] == 0: #Sí no quedan gatos que puedan moverse
					print('No quedan gatitos capaces de continuar moviendose!')
					self.printStairState(isFinal=True)
					print('+'+'='*100+'+')
					print('Finalizando la Simulación...')
					return False # Devuelve False para detener la simulación
				else: #Sí quedan gatos por moverse y la marea no ha llegado a la cima de la escalera
					self.printStairState()
					return True # Devuelve True para continuar la simulación
	
	def updateCats(self):
		"""<method> Uso: self.updateCats() : Actualiza la posición y estado de los elementos de self.cats

		Raises:
			exit(0) : Falla critica, dado que self.cats es una lista vacía.
		"""     
		# Declaración de variables por conveniencia
		sunkGate = self.waterPos # Posición actual de la marea
		escapeGate = self.N # Umbral de escape
		
		if self.isCatsVoid: # Sanity Check // Verifica que self.cats no este vacío
			print('CRITICAL ERROR MSG: No hay un conjunto de gatos definido...\nFinalizando aplicacion...')
			sys.exit(0)
		else: # Sanity Check // self.cats no está vacío
			for cat in self.cats: #Itera sobre la lista de gatos
				pos = cat.pos
				if (pos > sunkGate) and (pos < escapeGate): # El gato está entre la marea y el final de la escalera
					cat.setStatus('active') # Fija status como 'active'
				elif (pos <= sunkGate): # El gato se hundió
					cat.setStatus('sunk') # Fija status como 'sunk'
					print('Oh no! {} se ha hundido!'.format(cat.name))
				elif (pos >= escapeGate): # El gato escapó
					cat.setStatus('safe') # Fija status como 'safe'
					cat.setPosition(self.N + 1) # Fija la posición del gato para evitar valores excesivamente altos
					print('Felicitaciones! {} ha logrado escapar'.format(cat.name))

	def CatCount(self):
		"""<method> Uso: self.CatCount() : Realiza un conteo por estado de los elementos en self.cats

		Returns:
			List: Lista que contiene los conteos(int) por estado de los elementos de self.cats. Es de la forma [int, int, int]  
		"""     
		activeCount = 0
		sunkCount = 0
		safeCount = 0
		for cat in self.cats:
			match cat.status:
				case 'active':
					activeCount += 1
				case 'sunk':
					sunkCount += 1
				case 'safe':
					safeCount += 1
		return [activeCount, sunkCount, safeCount]

	def update(self, nCats=1, nWater=1, dt=10, isFair=True, isRandomized=False):
		"""<method> Uso: self.update(nCats=1, nWater=1, dt=10, isFair=True, isRandomized=False) : Avanza la simulación.

		Args:
			nCats (int, optional): Cantidad de escalones que se mueve cada gato. Por defecto es 1.
			nWater (int, optional): Cantidad de escalones que se mueve la marea. Por defecto es 1.
			dt (int, optional): Intervalo de tiempo en segundos. Por defecto es 10.
			isFair (bool, optional): Determina si la marea se mueve la misma cantidad de escalones que los gatos. Por defecto es True.
			isRandomized (bool, optional): Determina si el movimiento de los gatos y la marea es aleatorio. Por defecto es False.

		Returns:
			bool: Llama al metodo self.raiseWater y repite su respuesta.
		"""     
		# Verifica si está usando la configuración aleatoria
		if isRandomized:
			# Verifica si está usando la configuración de movimiento justo
			if isFair:
				nCats = random.randint(1, (self.N))
				nWater = nCats
			else:
				nCats = random.randint(1, (self.N))
				nWater = random.randint(1, (self.N))
		else:
			# Verifica si está usando la configuración de movimiento justo
			if isFair:
				if nCats != nWater: # Sanity Check
					print("ERROR MSG: Se ha configurado mov. justo, pero los movimientos de la marea y los gatitos son distintos...\n	Se continuará usando el valor menor...")
					if nCats < nWater:
						nWater = nCats
					else:
						nCats = nWater
				else:
					nCats, nWater = nCats, nWater #Sanity Check
		
		# Actualiza la posición de los gatos con status 'active'
		for cat in self.cats:
			if (cat.status == 'active'):
				cat.setPosition(cat.pos + nCats)
			else:
				pass
		return self.raiseWater(nWater, dt) #Devuelve bool

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
		self.name, self.pos, self.status = name, pos, status
	
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

def __main__(): 
	"""<func> __main__() : Función de ejecución primaria. Al llamarla se ejecuta el módulo.
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
		iswaterLess = False
		# Analogamente al input para la cantidad de gatos, se reintentará este input hasta que el usuario finalice la aplicación o la posición inicial de la marea sea válida.
		while not isWaterLess:
			waterPos0 = getValidInput('Ingrese el escalón donde partirá la marea: ', 'int')
			print('+'+'-'*100+'+')
			if waterPos0 < (nSteps - nCats):
				isWaterLess = True
			else:
				print('ERROR: El valor ingresado es demasiado alto, no se podrá hacer la configuración inical correctamente...')
				print('Porfavor reintente...')
				waterPos0 = None
				isWaterLess = False
	else:
		waterPos0 = 0
	
	# Da la opción de nombrar a los gatos y crea la lista de objetos Cat
	areNamed = getValidInput('¿Desea nombrar a sus gatitos?(y/n) ', 'bool')
	print('+'+'-'*100+'+')
	catList = []
	if areNamed: # Crea la lista de objetos Cat, usando nombres ingresados por el usuario
		print(('Creando {} gatitos...\n'+'\nA continuacion nombre a sus gatitos...\n'+'+'+'-'*100+'+').format(str(nCats)))
		for i in range(0, nCats):
			name = getValidInput('Ingrese el nombre del gatito n° {}: '.format(str(i+1)), 'str')
			catList.append(Cat(name, i+1))
	else: # Crea la lista de objetos Cat, usando nombres autogenerados
		print(('Creando {} gatitos...\n'+'+'+'-'*100+'+').format(str(nCats)))
		for i in range(0, nCats):
			name = 'GATO #{}'.format(str(i+1))
			catList.append(Cat(name, i+1))
	
	# Crea la instancia stair del objeto Stair con la configuración dada
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
	while isRunning:
		isRunning = stair.update(nCats=1, nWater=1, dt=10, isFair=isFair, isRandomized=isRandomized) #stair.update devuelve un bool que será False si y sólo si se cumplen las condiciones necesarioas para finalizar la simulación