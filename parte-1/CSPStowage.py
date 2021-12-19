import sys

from constraint import *

_, path, mapaNombre, contenedoresNombre = sys.argv
mapa = open(path + '/' + mapaNombre + '.txt', "r").readlines()

# Eliminar los espacios en blanco en el mapa
for i, fila in enumerate(mapa):
    mapa[i] = fila.replace(" ", "")

contenedores = open(path + '/' + contenedoresNombre + '.txt', "r").readlines()
#  Generamos un diccionario de la forma idContenedor: puerto que nos ayudará a generar una restricción mas adelante
puertos = {contenedor[0]: int(contenedor[4]) for contenedor in contenedores}


def problem(mapa, contenedores):
    """ Devuelve las soluciones al problema dado un mapa y unos contenedores.
    El mapa y los contenedores son el resultado de leer sus ficheros.
    """
    problem = Problem()
    variables = []
    # Generamos las variables junto con sus dominios y las añadimos al problema.
    for i, contenedor in enumerate(contenedores):
        dominio = domain(contenedor, mapa)
        problem.addVariable(str(i + 1), dominio)
        variables.append(str(i + 1))
    # Añadimos las restricciones, sus funciones definidas y explicadas abajo.
    problem.addConstraint(notEqual, variables)
    problem.addConstraint(under, variables)
    problem.addConstraint(notOn, variables)

    sols = problem.getSolutions()

    # Si no hemos obtenido soluciones quitamos la restricción que obliga a los contenedores del puerto 1 a estar encima
    # de los del puerto 2, ya que si no es posible aún así queremos obtener las soluciones posibles.
    if len(sols) == 0:
        problem.reset()
        problem = Problem()
        variables = []
        for i, contenedor in enumerate(contenedores):
            dominio = domain(contenedor, mapa)
            problem.addVariable(str(i + 1), dominio)
            variables.append(str(i + 1))
        problem.addConstraint(notEqual, variables)
        problem.addConstraint(under, variables)

        sols = problem.getSolutions()

    # Generamos el fichero de salida y escribimos el resultado
    salida = open(f'{path}/{mapaNombre}-{contenedoresNombre}.output.txt', 'w')
    salida.write(f'Numero de soluciones: {len(sols)}\n')
    for sol in sols:
        salida.write(str(sol) + '\n')

    return sols


def domain(contenedor, mapa):
    """
    Devuelve el dominio de un contenedor que llega como parámetro.

    :param contenedor:
    :param mapa:
    :return dominio de un contenedor como una lista de posiciones:
    """
    domain = []
    # Si el contenedor es de tipo S entonces el dominio son todas las celdas menos las que tienen una X, es decir,
    # las que tienen N o E
    if contenedor[2] == "S":
        for index_f, fila in enumerate(mapa):
            for index_c, elem in enumerate(fila):
                if elem == "N" or elem == "E":
                    domain.append([index_c, index_f])
    # Si el contenedor es de tipo R entonces el dominio son todas las celdas que tengan el valor E
    elif contenedor[2] == "R":
        for index_f, fila in enumerate(mapa):
            for index_c, elem in enumerate(fila):
                if elem == "E":
                    domain.append([index_c, index_f])
    return domain


def notEqual(*args):
    """
        Devuele False en caso de que dos contenedores tengan asignada la misma celda
    """
    for i in range(len(args)):
        for j in range(i + 1, len(args)):
            if i != j and args[i] == args[j]:
                return False
    return True


def under(*args):
    """
        Sirve para evitar que los contenedores esten flotando. Siempre deben tener o bien un contenedor
        abajo o una celda con valor X
    """
    todosDebajo = []
    for i in range(len(args)):
        debajo = []
        for j in range(len(args)):
            # Comparamos si un contenedor A tiene algún contenedor B o una X
            # Si es el caso añadimos a su lista el valor True.
            if i != j:
                # Es necesario lanzar este bloque try ya que podriamos
                # tener un error out of index en caso de estar comprobando el suelo.
                # En este caso tambien añadimos True, ya que es posible colocar un contenedor en el suelo.
                try:
                    if mapa[args[i][1] + 1][args[i][0]] == "X":
                        debajo.append(True)
                        break
                    else:
                        debajo.append(args[i][0] == args[j][0] and args[i][1] == args[j][1] - 1)
                except:
                    debajo.append(True)
                    break
        # Si alguno de estos valores es True es que esta apoyado
        todosDebajo.append(any(debajo))
    # Si TODOS los contenedores tienen uno debajo o el suelo entonces devolvemos True
    return all(todosDebajo)


def notOn(*args):
    """
        Sirve para poner los contenedores que van al puerto 1 por encima de los que van al puerto 2
    """
    todosEncima = []
    for i in range(len(args)):
        encima = []
        for j in range(len(args)):
            # Comprobamos si un contenedor A que va al puerto 1 y otro B que va al puerto 2 estan en el orden correcto
            # Es decir los del puerto 1 encima de los del 2
            if i != j:
                if puertos[str(int(i) + 1)] == 1 and puertos[str(int(j) + 1)] == 2:
                    if args[i][0] == args[j][0]:
                        encima.append(args[i][1] != args[j][1] + 1)
                    else:
                        encima.append(True)
        # Para que se cumpla la condición todos los valores de la lista deben ser True,
        # ya que si hay alguno que no lo es habría un contenedor de puerto 2 encima de otro puerto 1.
        todosEncima.append(all(encima))
    # Es necesario que todos los contenedores cumplan la condición.
    return all(todosEncima)


def printSol(sol):
    """
       Función auxiliar para imprimir una solución del problema de manera visual
    """
    columnas = len(mapa[0]) - 1
    filas = len(mapa)
    m = []
    for f in mapa:
        m.append(f.split(" "))
    posx = []
    for col, fil in enumerate(m):
        for f in fil:
            cont = 0
            for elem in f:
                if elem == 'X':
                    posx.append([cont, col])
                cont += 1
    mat = [[" " for _ in range(columnas)] for _ in range(filas)]
    for c, f in posx:
        mat[f][c] = 'X'
    for key in sol.keys():
        mat[sol[key][1]][sol[key][0]] = key
    for fila in mat:
        print(fila)


problem(mapa, contenedores)
