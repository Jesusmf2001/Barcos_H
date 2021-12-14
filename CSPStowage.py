import sys

from constraint import *

path, contenedores, mapa = sys.argv
mapa = open(mapa, "r").readlines()

for i, fila in enumerate(mapa):
    print(fila.strip())
    mapa[i] = fila.replace(" ", "")

contenedores = open(contenedores, "r").readlines()


def problem(mapa, contenedores):
    problem = Problem()
    variables = []
    for i, contenedor in enumerate(contenedores):
        dominio = domain(contenedor, mapa)
        problem.addVariable(str(i +1), dominio)
        variables.append(str(i + 1))
    problem.addConstraint(notEqual, variables)

    return problem.getSolutions()

def notEqual(*args):
    for i in range(len(args)):
        for j in range(i + 1, len(args)):
            if i != j and args[i] == args[j]:
                return False
    return True

def under(*args):
    for i in range(len(args)):
        pass

def domain(contenedor, mapa):
    list = []
    if contenedor[2] == "S":
        for index_c, fila in enumerate(mapa):
            for index_f, elem in enumerate(fila):
                if elem == "N" or elem == "E":
                    list.append([index_f, index_c])
    elif contenedor[2] == "R":
        for index_c, fila in enumerate(mapa):
            for index_f, elem in enumerate(fila):
                if elem == "E":
                    list.append([index_f, index_c])
    return list
print(problem(mapa, contenedores)[8])
print(domain(contenedores[4], mapa))