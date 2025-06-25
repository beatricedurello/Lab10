import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._stato = None

    def handleCalcola(self, e):
        txtInput = self._view._txtAnno.value
        if txtInput == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Inserire un anno.", color="red"))
            self._view.update_page()
            return

        try:
            anno = int(txtInput)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Il valore inserito non è un numero", color="red"))
            self._view.update_page()
            return

        if anno < 1816 or anno > 2016:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Possono essere inseriti solo anni tra il 1816 e il 2016", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(anno)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumCompConnesse()} componenti connesse."))
        self._view._txt_result.controls.append(ft.Text("Di seguito il dettaglio sui nodi."))
        for n in self._model.getAllNodi():
            self._view._txt_result.controls.append(ft.Text(f"{n} -- {self._model.getNumeroVicini(n.CCode)} vicini."))

        self._view._ddStato.disabled = False
        self._view._btnStatiRaggiungibili.disabled = False
        self._view._ddStato.options.clear()
        for n in self._model.getAllNodi():
            self._view._ddStato.options.append(ft.dropdown.Option(text=n.StateNme, data=n, on_click=self.handleSceltaStato))
        self._stato = None

        self._view.update_page()

    def handleStatiRaggiungibili(self, e):
        if self._stato is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione, selezioneare uno stato"))
            self._view.update_page()
            return

        statiRaggiungibili = self._model.calcolaRaggiungibiliV1(self._stato)

        if len(statiRaggiungibili) == 0:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Nessuno stato raggiungibile da {self._stato}."))
            self._view.update_page()
            return


        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Stati raggiungibili da {self._stato}: "))
        for s in statiRaggiungibili:
            self._view._txt_result.controls.append(ft.Text(s))
        self._view.update_page()

    def handleSceltaStato(self, e):
        self._stato = e.control.data

