import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        for a in self._model.getAnni():
            self._view.ddyear.options.append(ft.dropdown.Option(a))
        self._view.update_page()

    def fillShape(self,e):
        self._view.ddshape.options.clear()
        if e.control.value == None:
            print("seleziona un anno")
            return
        for s in self._model.getShape(e.control.value):
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()

    def handle_graph(self, e):
        self._model.buildGraph(self._view.ddyear.value,self._view.ddshape.value)
        tupla = self._model.getTupla()
        self._view.txt_result.controls.append(ft.Text(f"{self._model.getDetails()}"))
        for t in tupla:
            self._view.txt_result.controls.append(ft.Text(f"Nodo {t[0]}, somma pesi su archi = {t[1]}"))
        self._view.update_page()
    def handle_path(self, e):
        path,score=self._model.getCammino()
        self._view.txtOut2.controls.append(ft.Text(f"Peso cammino massimo {score}"))
        for i in range(0, len(path)-1):
            self._view.txtOut2.controls.append(ft.Text(f"{path[i]}--> {path[i+1]}: weight {self._model.grafo[path[i]][path[i+1]]["weight"]}, distance {self._model.getDistance(path[i],path[i+1])}"))
        self._view.update_page()