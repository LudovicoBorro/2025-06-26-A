import copy

import networkx as nx
from database.DAO import DAO

class Model:

    def __init__(self):
        self._graph = nx.Graph()
        self._idMapCircuits = {}
        self._bestPath = []
        self._circuitiWPesoMax = {}
        self._bestScore = 0
        self._imprevidibilita = {}

    def bestInsieme(self, k, m, yearMin, yearMax):
        self._imprevidibilita.clear()
        self._bestPath = []
        self._bestScore = 0
        circuiti = self.getMaxConnComp()
        circNumCorse = DAO.getNumCorsePerCircuito(yearMin, yearMax)
        mapCircuiti = {}
        for circ in circNumCorse:
            mapCircuiti[circ[0]] = circ[1]
        circuitiValidi = []
        for circuit in circuiti:
            if mapCircuiti[circuit[0].circuitId] >= m:
                circuitiValidi.append(circuit[0])
        self._calcolaImprev(circuitiValidi)

        print("K =", k)
        print("Circuiti validi:", len(circuitiValidi))

        parziale = []
        for node in circuitiValidi:
            parziale.append(node)
            self._ricorsione(parziale, k)
            parziale.pop()
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, k):
        if len(parziale) == k:
            score = self._getScore(parziale)
            # print(f"SOLUZIONE POTENZIALE TROVATA CON SCORE: {score}")
            if score > self._bestScore:
                print("SOLUZIONE TROVATA", len(parziale))
                self._bestScore = score
                self._bestPath = copy.deepcopy(parziale)
            return

        for vicino in self._graph.neighbors(parziale[-1]):
            if vicino not in parziale and vicino in self._imprevidibilita.keys():
                parziale.append(vicino)
                self._ricorsione(parziale, k)
                parziale.pop()

    def _getScore(self, parziale):
        somma = 0
        for circ in parziale:
            somma += self._imprevidibilita[circ]
        return somma

    def _calcolaImprev(self, circuiti):
        for circuit in circuiti:
            circ = self._idMapCircuits[circuit.circuitId]
            nP = self._circuitiWPesoMax[circ]
            nPtot = 0
            for lista in circ.piazzamenti.values():
                nPtot += len(lista)
            if nPtot == 0:
                imprev = 0
            else:
                imprev = 1 - (nP / nPtot)
            # print(f"Imprevedibilità calcolata per circuito: {circuit.name} -> {imprev}")
            self._imprevidibilita[circuit] = imprev

    def buildGraph(self, yearMin, yearMax):
        self._graph.clear()
        circuits = DAO.getAllCircuits()
        yearsSelezionati = [yearMin]
        while yearsSelezionati[-1] != yearMax:
            yearsSelezionati.append(yearsSelezionati[-1] + 1)
        for circuit in circuits:
            for year in yearsSelezionati:
                piazzamenti = DAO.getPlacementsByCircuitAndYear(circuit.circuitId, year)
                if len(piazzamenti) == 0:
                    continue
                circuit.piazzamenti[year] = piazzamenti
            self._idMapCircuits[circuit.circuitId] = circuit
        self._graph.add_nodes_from(circuits)
        edges = DAO.getAllEdges(yearMin, yearMax)
        for edge in edges:
            circ1 = self._idMapCircuits[edge[0]]
            circ2 = self._idMapCircuits[edge[1]]
            peso = edge[2]
            self._graph.add_edge(circ1, circ2, weight=peso)

    def graphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getMaxConnComp(self):
        self._circuitiWPesoMax.clear()
        maxConn = list(max(nx.connected_components(self._graph), key=len))
        setNodes = set(maxConn)
        nodiOrdinati = []
        for node in maxConn:
            archi = self._graph.edges(node, data=True)
            pesi = [d['weight'] for u, v,   d in archi if v in setNodes]
            pesoMassimo = max(pesi)
            self._circuitiWPesoMax[node] = pesoMassimo
            nodiOrdinati.append((node, pesoMassimo))
        return sorted(nodiOrdinati, key=lambda x: x[1], reverse=True)

    @staticmethod
    def getAllYears():
        return sorted(DAO.getAllYears(), reverse=True)

    def isGraphOk(self):
        return len(self._graph.nodes) > 0 and len(self._graph.edges) > 0