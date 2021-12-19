import sys

_, path, mapaNombre, contenedoresNombre, heuristica = sys.argv


class Contenedor:
    """
        Representa un contenedor, con una id, un puerto, una posición y buleanos
        representando su estado.
    """
    def __init__(self, id, tipo, puerto):
        self.id = id
        self.refrigerado = True if tipo == "R" else False
        self.puerto = puerto
        self.cargado = False
        self.descargado = False
        self.columna = None
        self.fila = None

    def __repr__(self):
        return f'ID: {self.id}; REFRIGERADO: {self.refrigerado}; PUERTO: {self.puerto}; CARGADO: {self.cargado}'

    def __eq__(self, other):
        return self.id == other.id


class Mapa:
    """
        Representa un mapa. Este contiene la información de las diferentes celdas y los diferentes
        contenedores que contiene. Ademas provee métodos utiles para añddir contenedores y calcular costes.
    """

    def __init__(self, mapa, contenedores):
        self.mapa = [fila.split(" ") for fila in mapa]
        self.contenedores = contenedores
        self.puerto = 0
        self.viajes = 0
        self.mapaContenedores = self.mapa.copy()

    def cargarContenedor(self, contenedor, fila, columna):
        if not contenedor.cargado:
            self.contenedores.append(contenedor)
            self.mapaContenedores[fila][columna] = contenedor
            contenedor.fila = fila
            contenedor.columna = columna
            contenedor.cargado = True

    def descargarContenedor(self, contenedor):
        self.contenedores.remove(contenedor)
        self.mapaContenedores[contenedor.fila][contenedor.columna] = None
        contenedor.fila = None
        contenedor.columna = None
        contenedor.descargado = True

    def dondeCargar(self, contenedor):
        """
            Devuelve un array de posiciones en las que es posible cargar un contenedor
        """
        posiciones = []
        for filaNum, fila in enumerate(self.mapa):
            for colNum, columna in enumerate(fila):
                if self.sePuedeCargar(contenedor, filaNum, colNum):
                    posiciones.append([filaNum, colNum])
        return posiciones

    def sePuedeCargar(self, contenedor, fila, columna):
        """
            Comprueba si es posible cargar un contenedor en una determinada posición
        """
        if isinstance(self.mapaContenedores[fila][columna], Contenedor):
            return False
        try:
            # Try ya que podriamos estar comprobando una posición out of index
            mapa_fc = self.mapaContenedores[fila + 1][columna]
        except:
            mapa_fc = False

        if isinstance(mapa_fc, Contenedor) or mapa_fc == 'X' or not mapa_fc:
            if contenedor.refrigerado:
                return self.mapaContenedores[fila][columna] == 'E'
            else:
                return self.mapaContenedores[fila][columna] != 'X'

    def costeDescargar(self, contenedor):
        return 15 + 2 * (contenedor.fila + 1)

    def costeCargar(self, fila):
        return 10 + fila + 1

    def cargados(self):
        """
            Devuelve el número de contenedores cargados filtrando la lista por los elementos que son de tipo contenedor
        """
        return len(list(filter(lambda contenedor: isinstance(contenedor, Contenedor), self.mapaContenedores)))

    def __repr__(self):
        return str(self.mapa)

    def __eq__(self, other):
        return self.mapaContenedores == other.mapaContenedores
