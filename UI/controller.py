import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._chosen_location = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model

    def fill_dd_providers(self):
        providers = self.model.providers
        providers_dd = map(lambda p: ft.dropdown.Option(p), providers)
        self.view.dd_provider.options.extend(providers_dd)
        self.view.update_page()

    def handle_crea_grafo(self, e):
        provider = self.view.dd_provider.value
        if provider is None:
            self.view.create_alert("Selezionare un provider")
            return
        d_str = self.view.txt_IN_distanza.value
        if d_str == "":
            self.view.create_alert("Inserire una distanza")
            return
        try:
            d_float = float(d_str)
        except ValueError:
            self.view.create_alert("Inserisci un numero")
            return
        self.model.build_graph(provider, d_float)
        self.view.txt_result.controls.clear()
        n_nodi, n_archi = self.model.get_graph_details()
        self.view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente: il grafo ha {n_nodi} nodi e "
                                                     f"{n_archi} archi"))
        self.fill_dd_target()
        self.view.update_page()

    def handle_analisi_grafo(self, e):
        self.model.get_nodes_neighbors()
        self.view.txt_result.controls.clear()
        neighbors_tuple = self.model.get_nodes_neighbors()
        self.view.txt_result.controls.append(ft.Text(f"Vertici con più vicini: "))
        for neighbor in neighbors_tuple:
            self.view.txt_result.controls.append(ft.Text(f"{neighbor[0]} --> {neighbor[1]} vicini"))
        self.view.update_page()

    def fill_dd_target(self):
        self.view.dd_target.options.clear()
        for location in self.model.graph.nodes:
            self.view.dd_target.options.append(ft.dropdown.Option(data=location,
                                                                  text=location,
                                                                  on_click=self.read_location))

    def read_location(self, e):
        if e.control.data is None:
            self._chosen_location = None
        self._chosen_location = e.control.data

    @property
    def chosen_location(self):
        return self._chosen_location

    def handle_calcola_percorso(self, e):
        s = self.view.txt_IN_string.value
        target = self._chosen_location
        if s == "":
            self.view.create_alert("Inserire una stringa")
            return
        if target is None:
            self.view.create_alert("Selezionare una location")
            return
        path, source = self.model.get_percorso(target, s)
        if len(path) == 0:
            self.view.create_alert(f"Percorso non trovato tra {source} e {self.chosen_location}")
            return
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il percorso trovato ha lunghezza {self.model.best_len}"))
        for location in self.model.best_sol:
            self.view.txt_result.controls.append(ft.Text(f"{location}"))
        self.view.update_page()


