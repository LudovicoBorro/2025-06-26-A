import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleBuildGraph(self, e):
        yearMin = self._view._ddYear1.value
        yearMax = self._view._ddYear2.value

        if yearMin is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, seleziona un anno minimo!", color="red"))
            self._view.update_page()
            return

        if yearMax is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, seleziona un anno massimo!", color="red"))
            self._view.update_page()
            return

        yearMinInt = int(yearMin)
        yearMaxInt = int(yearMax)

        if yearMinInt > yearMaxInt:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, l'anno minimo deve essere più piccolo dell'anno massimo!", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(yearMinInt, yearMaxInt)
        nodes, edges = self._model.graphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {nodes} nodi e {edges} archi."))
        self._view.update_page()

    def handlePrintDetails(self, e):
        if not self._model.isGraphOk():
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, devi prima creare il grafo!", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        maxComp = self._model.getMaxConnComp()
        self._view.txt_result.controls.append(ft.Text("Stampa dettagli:"))
        for node in maxComp:
            self._view.txt_result.controls.append(ft.Text(f"{node[0]} -- {node[1]}"))
        self._view.update_page()

    def handleCercaDreamChampionship(self, e):
        if not self._model.isGraphOk():
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, devi prima creare il grafo!", color="red"))
            self._view.update_page()
            return

        soglia = self._view._txtInSoglia.value
        numEd = self._view._txtInNumDiEdizioni.value
        yearMin = self._view._ddYear1.value
        yearMax = self._view._ddYear2.value

        if soglia is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserisci un valore di soglia!", color="red"))
            self._view.update_page()
            return

        if numEd is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserisci un valore per numero di edizioni!", color="red"))
            self._view.update_page()
            return

        try:
            sogliaInt = int(soglia)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserisci un valore numerico per la soglia!", color="red"))
            self._view.update_page()
            return

        try:
            numEdInt = int(numEd)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserisci un valore numerico per il numero di edizioni!", color="red"))
            self._view.update_page()
            return

        bestPath, bestScore = self._model.bestInsieme(sogliaInt, numEdInt, yearMin, yearMax)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Trovato un cammino ottimo con score: {bestScore}"))
        for node in bestPath:
            self._view.txt_result.controls.append(ft.Text(node))
        self._view.update_page()

    def fillDDYears(self):
        years = self._model.getAllYears()
        yearsOptions = list(map(lambda x: ft.dropdown.Option(x), years))
        self._view._ddYear1.options = yearsOptions
        self._view._ddYear2.options = yearsOptions
        self._view.update_page()