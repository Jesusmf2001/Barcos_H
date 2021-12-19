import sys

from constraint import *

_, path, mapaNombre, contenedoresNombre = sys.argv
mapa = open(path + '/' + mapaNombre + '.txt', "r").readlines()

# Eliminar los espacios en blanco en el mapa
for i, fila in enumerate(mapa):
    mapa[i] = fila.replace(" ", "")

contenedores = open(path + '/' + contenedoresNombre + '.txt', "r").readlines()
#  Obtenemos un diccionario en el que asignamos pares contenedor: puerto.
#  En contenedor[0] se encuentra la ID y en contenedor[4] en número de puerto
puertos = {contenedor[0]: int(contenedor[4]) for contenedor in contenedores}


def problem(mapa, contenedores):
    problem = Problem()
    variables = []
    for i, contenedor in enumerate(contenedores):
        dominio = domain(contenedor, mapa)
        problem.addVariable(str(i + 1), dominio)
        variables.append(str(i + 1))
    problem.addConstraint(notEqual, variables)
    problem.addConstraint(under, variables)
    problem.addConstraint(notOn, variables)

    sols = problem.getSolutions()

    if len(sols) == 0:
        problem.reset()
        variables = []
        for i, contenedor in enumerate(contenedores):
            dominio = domain(contenedor, mapa)
            problem.addVariable(str(i + 1), dominio)
            variables.append(str(i + 1))
        problem.addConstraint(notEqual, variables)
        problem.addConstraint(under, variables)

        sols = problem.getSolutions()

    salida = open(f'{path}/{mapaNombre}-{contenedoresNombre}.output.txt', 'w')
    salida.write(f'Numero de soluciones: {len(sols)}\n')
    for sol in sols:
        salida.write(str(sol) + '\n')

    return sols


def domain(contenedor, mapa):
    domain = []
    if contenedor[2] == "S":
        for index_f, fila in enumerate(mapa):
            for index_c, elem in enumerate(fila):
                if elem == "N" or elem == "E":
                    domain.append([index_c, index_f])
    elif contenedor[2] == "R":
        for index_f, fila in enumerate(mapa):
            for index_c, elem in enumerate(fila):
                if elem == "E":
                    domain.append([index_c, index_f])
    return domain


def notEqual(*args):
    for i in range(len(args)):
        for j in range(i + 1, len(args)):
            if i != j and args[i] == args[j]:
                return False
    return True


def under(*args):
    valoresJefe = []
    for i in range(len(args)):
        valores = []
        for j in range(len(args)):
            if i != j:
                try:
                    if mapa[args[i][1] + 1][args[i][0]] == "X":
                        valores.append(True)
                    else:
                        valores.append(args[i][0] == args[j][0] and args[i][1] == args[j][1] - 1)
                except:
                    valores.append(True)
        valoresJefe.append(any(valores))
    return all(valoresJefe)


def notOn(*args):
    valoresJefe = []
    for i in range(len(args)):
        valores = []
        for j in range(len(args)):
            if i != j:
                if puertos[str(int(i) + 1)] == 1 and puertos[str(int(j) + 1)] == 2:
                    if args[i][0] == args[j][0]:
                        valores.append(args[i][1] != args[j][1] + 1)
                    else:
                        valores.append(True)
        valoresJefe.append(all(valores))
    return all(valoresJefe)


def printSol(sol):
    columnas = len(mapa[0]) - 1
    filas = len(mapa)
    m = []
    for f in mapa:
        m.append(f.split(" "))
    posx = []
    for col, fil in enumerate(m):
        for f in fil:
            cont = 0
            for caca in f:
                if caca == 'X':
                    posx.append([cont, col])
                cont += 1
    mat = [[" " for _ in range(columnas)] for _ in range(filas)]
    for c, f in posx:
        mat[f][c] = 'X'
    for key in sol.keys():
        mat[sol[key][1]][sol[key][0]] = key
    for fila in mat:
        print(fila)


sols = problem(mapa, contenedores)
