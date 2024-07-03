import copy

import networkx as nx

from database.DAO import DAO
from geopy.distance import distance

class Model:
    def __init__(self):
        self.grafo = nx.Graph()

    def getCammino(self):
        self.bestPath=[]
        self.bestObj=0
        parziale =[]
        for n in self.grafo.nodes():
            parziale.append(n)
            self.ricorsione(parziale)
            parziale.pop()
        return self.bestPath, self.bestObj

    def getDistance(self,n1,n2):
        return distance((n1.Lat,n1.Lng),(n2.Lat,n2.Lng)).km


    def ricorsione(self,parziale):
        if self.getScore(parziale)> self.bestObj:
            self.bestObj = self.getScore(parziale)
            self.bestPath = copy.deepcopy(parziale)

        for n in self.grafo.neighbors(parziale[-1]):
            if len(parziale)==1:
                lastW = 0
            else:
                lastW = self.grafo[parziale[-2]][parziale[-1]]["weight"]
            if self.grafo[parziale[-1]][n]["weight"] > lastW and n not in parziale:
                parziale.append(n)
                self.ricorsione(parziale)
                parziale.pop()

    def getScore(self, parziale):
        score = 0
        for i in range(0, len(parziale) - 1):
            score += distance((parziale[i].Lat, parziale[i].Lng), (parziale[i + 1].Lat, parziale[i + 1].Lng)).km
        return score


    def getAnni(self):
        return DAO.getAnni()

    def getShape(self,anno):
        return DAO.getShape(anno)

    def buildGraph(self,anno,shape):
        nodes = DAO.getNodes()
        idMap={}
        for n in nodes:
            idMap[n.id]=n
        self.grafo.add_nodes_from(nodes)
        edges = DAO.getEdges(idMap)
        self.grafo.add_edges_from(edges)
        for e in self.grafo.edges:
            self.grafo[e[0]][e[1]]["weight"] = DAO.getPeso(e[0],e[1],anno,shape)
    def getTupla(self):
        tupla = []
        for n in self.grafo.nodes:
            score=0
            for n1 in self.grafo.neighbors(n):
                score += self.grafo[n][n1]["weight"]
            tupla.append((n,score))
        return tupla
    def getDetails(self):
        return f"Il grafo ha {len(self.grafo.nodes)} nodi e {len(self.grafo.edges)} archi"




