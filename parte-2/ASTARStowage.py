import sys
from clases import Mapa, Contenedor

_, path, mapaNombre, contenedoresNombre, heuristica = sys.argv

contenedores = open(path + '/' + contenedoresNombre + '.txt', "r").readlines()
contenedores = [Contenedor(*contenedor.split(" ")) for contenedor in contenedores]
mapa = open(path + '/' + mapaNombre + '.txt', "r").readlines()
mapa = Mapa(mapa, contenedores)


class AStar:
    def __init__(self, mapa, contenedores):
        self.mapa = mapa
        self.contenedores = contenedores


    def expand_node(self, node):
        if self.canExpandCharge(node):
            print(1)
            for contenedor in node.elem.contenedores:
                if not contenedor.cargado:
                    nodos = self.expandCharge(node, contenedor)
                    print(nodos)
                    for charge_node in nodos:
                        node.hijos.append(charge_node)
        if self.canExpandDischarge(node):
            for contenedor in self.contenedores:
                if not contenedor.descargado and contenedor.puerto == node.elem.puerto:
                    nodo = self.expandDischarge(node, contenedor)
                    node.hijos.append(nodo)

        if self.canExpandPort():
            list_h = self.expandPort(node)
            for node_h in list_h:
                node.hijos.append(node_h, padre= node, coste= 3500)

        return node.hijos

    def canExpandCharge(self, node):
        return len(list(filter(lambda contenedor: not contenedor.cargado, node.elem.contenedores))) > 0

    def expandCharge(self, node, contenedor):
        nodos = []
        posiciones = node.elem.dondeCargar(contenedor)
        for pos in posiciones:
            coste = node.elem.costeCargar(pos[0])
            nodo = Node(node.elem, padre=node, coste=coste)
            nodo.elem.cargarContenedor(contenedor, pos[0], pos[1])
            nodos.append(nodo)

        return nodos

    def canExpandDischarge(self, node):
        return len(list(filter(lambda contenedor: not contenedor.descargado, node.elem.contenedores))) > 0

    def expandDischarge(self, node, contenedor):
        node.elem.descargarContenedor(contenedor)
        nodo = Node(node.elem, padre=node, coste=node.elem.costeDescargar(contenedor))
        return nodo

    def canExpandPort(self):
        return self.mapa.puerto != 0 or all(list(filter(lambda contenedor: not contenedor.cargado, node.elem.contenedores)))

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
            print(nodeMin.elem)
            if nodeMin.heuristica == 0:
                return True
            else:
                nodos.remove(nodeMin)
                hijos = self.expand_node(nodeMin)


class Node:
    def __init__(self, elem, padre=None, coste=0):
        self.padre = padre
        if self.padre is not None:
            self.id = self.padre.id + 1
        else:
            self.id = 0
        self.elem = elem
        self.hijos = []
        self.coste = coste + (padre.coste if padre is not None else 0)
        self.heuristica = self.calcHeursitica()
        self.f = self.heuristica + self.coste

    def calcHeursitica(self):
        cont_no_cargados = len(list(filter(lambda contenedor: not contenedor.cargado, contenedores)))
        cont_no_descargados = len(list(filter(lambda contenedor: not contenedor.descargado, contenedores)))
        return (cont_no_cargados * (10 + len(self.elem.mapa))) + \
               (cont_no_descargados * (15 + (2 * len(self.elem.mapa)))) + ((2 - self.elem.viajes) * 3500)

    def __gt__(self, other):
        return self.f > other.f

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return str(self.f)

AStar(mapa, contenedores).findSolution()
