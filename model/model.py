import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._stati = DAO.getAllStati()
        self._grafo = nx.Graph()
        self._idMapStati = {}
        for s in self._stati:
            self._idMapStati[s.CCode] = s

    def buildGraph(self, anno):
        self._grafo.clear()
        self._grafo.add_nodes_from(DAO.getAllNodi(anno, self._idMapStati))
        for e in DAO.getAllEdges(anno, self._idMapStati):
            u = e[0]
            v = e[1]
            self._grafo.add_edge(u,v)

    def getNumeroVicini(self, codStato):
        stato = self._idMapStati[codStato]
        vicini = self._grafo.neighbors(stato)
        tot = 0
        for v in vicini:
            tot += 1
        return tot

    def getNumCompConnesse(self):
        return nx.number_connected_components(self._grafo)

    def getAllNodi(self):
        return self._grafo.nodes

    def calcolaRaggiungibiliV1(self, stato):
        tree = nx.bfs_tree(self._grafo, stato)
        archi = tree.edges()
        nodi = list(tree.nodes())
        return nodi[1:]

    def calcolaRaggiungibiliV2(self, stato):
        visitati = []
        daVisitare = []
        visitati.append(stato)
        vicini = nx.neighbors(self._grafo, stato)
        for v in vicini:
            daVisitare.append(v)
        while len(daVisitare) != 0:
            temp = daVisitare[0]
            daVisitare.remove(temp)
            visitati.append(temp)
            neighbors = list(self._grafo.neighbors(temp))
            for n in neighbors:
                if n not in visitati and n not in daVisitare:
                    daVisitare.append(n)
        visitati.remove(stato)
        return visitati

    def calcolaRaggiungibiliV3(self, n):
        visitati = []
        self._recursion(n, visitati)
        visitati.remove(n)
        return visitati

    def _recursion(self, n, visitati):
        visitati.append(n)
        for c in self._grafo.neighbors(n):
            if c not in visitati:
                self._recursion(c, visitati)
