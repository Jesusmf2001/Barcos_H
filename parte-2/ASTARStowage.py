import sys
from clases import Mapa, Contenedor

_, path, mapaNombre, contenedoresNombre, heuristica = sys.argv

mapa = open(path + '/' + mapaNombre + '.txt', "r").readlines()
mapa = Mapa(mapa)

contenedores = open(path + '/' + contenedoresNombre + '.txt', "r").readlines()
contenedores = [Contenedor(*contenedor.split(" ")) for contenedor in contenedores]


class AStar:
    def __init__(self, mapa, contenedores):
        self.list = [False] * len(contenedores)
        self.mapa = mapa
        self.contenedores = contenedores
        self.coste = 0

    def expand_node(self, node):

        if self.canExpandCharge():
            for contenedor in self.contenedores:
                if not contenedor.cargado:
                    nodos = self.expandCharge(node, contenedor)
                    for charge_node in nodos:
                        node.hijos.append(charge_node)
        if self.canExpandDischarge():
            for contenedor in self.contenedores:
                if not contenedor.descargado and contenedor.puerto == node.elem.puerto:
                    nodo = self.expandDischarge(node, contenedor)
                    node.hijos.append(nodo)

        if self.canExpandPort():
            list_h = self.expandPort(node)
            for node_h in list_h:
                node.hijos[node_h] = 3500

        return node.hijos

    def canExpandCharge(self):
        return not (self.canExpandDischarge())

    def expandCharge(self, node, contenedor):
        nodos = []
        posiciones = node.elem.dondeCargar(contenedor)
        for pos in posiciones:
            coste = node.elem.costeCargar(contenedor, pos[0], pos[1])
            nodo = Node(node.elem, padre=node, coste=coste)
            nodo.elem.cargarContenedor(pos[0], pos[1])
            nodos.append(nodo)
        return nodos

    def canExpandDischarge(self):
        return all(self.list)

    def expandDischarge(self, node, contenedor):
        node_h = Node(node.elem, padre=node)
        node_h.elem = node_h.elem.descargarContenedor(contenedor)
        coste = node.elem.costeDescrgar(contenedor)
        return node_h, coste

    def canExpandPort(self):
        return self.mapa.puerto != 0 or all(self.list)

    def expandPort(self, node):

        list_h = []
        if node.elem.puerto == 1:
            node_h = Node(node.elem, padre=node)
            node_h.elem.puerto = 2
            list_h.append(node_h)
        elif node.elem.puerto == 2:
            node_h = Node(node.elem, padre=node)
            node_h.elem.puerto = 1
            list_h.append(node_h)
        elif node.elem.puerto == 0:
            node_h = Node(node.elem, padre=node)
            node_h.elem.puerto = 1
            list_h.append(node_h)
            node_h.elem.puerto = 2
            list_h.append(node_h)
        return list_h

    def findSolution(self):
        nodos = []
        raiz = Node(mapa)
        hijos = self.expand_node(raiz)
        while True:
            for hijo in hijos:
                nodos.append(hijo)
            nodeMin = min(nodos)
            if nodeMin.heuristica == 0:
                return True
            else:
                nodos.pop(nodeMin)
                self.expand_node(nodeMin)

class Node:
    def __init__(self, elem, padre=None):
        self.padre = padre
        self.elem = elem
        self.hijos = []
        self.coste = coste + (padre.coste if padre is not None else 0)
        self.heuristica = self.calcHeursitica()
        self.f = self.heuristica + self.coste

    def calcHeursitica(self):
        cont_no_cargados = len(self.elem.contenedores) - self.elem.cargados()
        cont_no_descargados = []
        for contenedor in self.elem.contenedores:
            if not contenedor.descargado:
                cont_no_descargados.append(contenedor)
        return (cont_no_cargados * (10 + len(self.elem.mapa))) + (
        len(cont_no_descargados) * (15 + (2 * len(self.elem.mapa)))) + ((2 - self.elem.viajes) * 3500)

    def __gt__(self, other):
        return self.f > other.f


AStar(mapa, contenedores).findSolution()
