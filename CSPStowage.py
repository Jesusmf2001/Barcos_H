import sys

from constraint import *

path, contenedores, mapa = sys.argv
mapa = open(mapa, "r").readlines()

# Eliminar los espacios en blanco en el mapa
for i, fila in enumerate(mapa):
    print(fila.strip())
    mapa[i] = fila.replace(" ", "")

contenedores = open(contenedores, "r").readlines()


def problem(mapa, contenedores):
    problem = Problem()
    variables = []
    for i, contenedor in enumerate(contenedores):
        dominio = domain(contenedor, mapa)
        problem.addVariable(str(i + 1), dominio)
        variables.append(str(i + 1))
    problem.addConstraint(notEqual, variables)
    problem.addConstraint(under, variables)
    return problem.getSolutions()


def notEqual(*args):
    for i in range(len(args)):
        for j in range(i + 1, len(args)):
            if i != j and args[i] == args[j]:
                return False
    return True


def under(*args):
    for i in range(len(args)):
        for j in range(len(args)):
            if i != j:
                if mapa[args[i][1] + 1][args[i][0]] == "X":
                    valores.append(True)
                else:
                    valores.append(args[i][0] == args[j][0] and args[i][1] == args[j][1] - 1)
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
    mat = [[" " for _ in range(columnas)] for _ in range(filas)]
    for key in sol.keys():
        mat[sol[key][1]][sol[key][0]] = key
    for fila in mat:
        print(fila)