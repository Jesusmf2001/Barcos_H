import sys
from clases import Mapa, Contenedor

_, path, mapaNombre, contenedoresNombre, heuristica = sys.argv

mapa = open(path + '/' + mapaNombre + '.txt', "r").readlines()
mapa = Mapa(mapa)

contenedores = open(path + '/' + contenedoresNombre + '.txt', "r").readlines()
contenedores = [Contenedor(*contenedor.split(" ")) for contenedor in contenedores]


class AStar:
    def __init__(self, mapa, contenedores, heuristica_n):
        self.list = [False] * len(contenedores)
        self.mapa = mapa
        self.contenedores = contenedores
        self.heuristica = self.calcHeuristica(heuristica_n)
        self.coste = 0

    def calcHeuristica(self, heuristica_n=1):
        cont_no_cargados = len(self.contenedores) - self.mapa.cargados()
        cont_no_descargados = []
        for contenedor in contenedores:
            if not contenedor.descargado:
                cont_no_descargados.append(contenedor)
        if heuristica_n == 1:
            return (cont_no_cargados * (10 + len(self.mapa))) + (
                len(cont_no_descargados) * (15 + (2 * len(self.mapa)))) + (2 * 3500)

    def getHeuristica(self):
        return self.heuristica

    def addCoste(self, add):
        self.coste += add

    def getCoste(self):
        return self.coste

    def expand_node(self, node):

        if self.canExpandCharge():
            for contenedor in self.contenedores:
                if not contenedor.cargado:
                    charge_node, charge_cost = self.expandCharge(node, contenedor)
                    node.hijos[charge_node] = charge_cost

        if self.canExpandDischarge():
            for contenedor in self.contenedores:
                if not contenedor.descargado:
                    discharge_node, discharge_cost = self.expandDischarge(node, contenedor)
                    node.hijos[discharge_node] = discharge_cost

        if self.canExpandPort():
            list_h = self.expandPort(node)
            for node_h in list_h:
                node.hijos[node_h] = 3500
        return node.hijos

    def canExpandCharge(self):
        return not (self.canExpandDischarge())

    def expandCharge(self, node, contenedor):
        node_h = Node(node.elem, padre=node)
        node_h.elem = node_h.elem.cargarContenedor(contenedor)
        coste = node.costeCargar(contenedor)
        return node_h, coste

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
        node_h = Node(node.elem, padre=node)
        list_h = []
        if node_h.elem.puerto == 1:
            node_h.elem.puerto = 2
            list_h.append(node_h)
        elif node_h.elem.puerto == 2:
            node_h.elem.puerto = 1
            list_h.append(node_h)
        elif node_h.elem.puerto == 0:
            node_h.elem.puerto = 1
            list_h.append(node_h)
            node_h.elem.puerto = 2
            list_h.append(node_h)
        return list_h

    def findSolution(self):
        nodos = []
        raiz = Node(mapa)
        self.expand_node(raiz)
        for hijos in raiz.hijos:
            nodos.append(hijos)



class Node:
    def __init__(self, elem, padre=None):
        self.padre = padre
        self.elem = elem
        self.hijos = {}
        self.f = 0
        if self.padre:
            self.f += self.padre.f


