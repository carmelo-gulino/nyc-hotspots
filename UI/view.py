import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._dd_target = None
        self._btn_calcola_percorso = None
        self._txt_IN_string = None
        self._btn_analisi_grafo = None
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._dd_provider = None
        self._btn_crea_grafo = None
        self._txt_result = None
        self._txt_IN_distanza = None

    def load_interface(self):
        # title
        self._title = ft.Text("Hello World", color="blue", size=24)
        self._page.controls.append(self._title)

        # ROW 1
        self._dd_provider = ft.Dropdown(label="Provider")
        self._btn_crea_grafo = ft.ElevatedButton(text="Crea grafo", on_click=self._controller.handle_crea_grafo)
        row1 = ft.Row([ft.Container(self._dd_provider, width=300),
                       ft.Container(self._btn_crea_grafo, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        self.controller.fill_dd_providers()

        # ROW 2
        self._txt_IN_distanza = ft.TextField(label="Distanza")
        self._btn_analisi_grafo = ft.ElevatedButton(text="Analizza grafo",
                                                    on_click=self._controller.handle_analisi_grafo)
        row2 = ft.Row([ft.Container(self._txt_IN_distanza, width=300),
                       ft.Container(self._btn_analisi_grafo, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # ROW 3
        self._txt_IN_string = ft.TextField(label="Stringa")
        self._btn_calcola_percorso = ft.ElevatedButton(text="Calcola percorso",
                                                       on_click=self.controller.handle_calcola_percorso)
        row3 = ft.Row([ft.Container(self._txt_IN_string, width=300),
                       ft.Container(self._btn_calcola_percorso, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # ROW 4
        self._dd_target = ft.Dropdown(label="Target")
        row4 = ft.Row([ft.Container(self._dd_target, width=300),
                       ft.Container(None, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row4)

        # List View where the reply is printed
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()

    @property
    def dd_provider(self):
        return self._dd_provider

    @property
    def btn_crea_grafo(self):
        return self._btn_crea_grafo

    @property
    def txt_result(self):
        return self._txt_result

    @property
    def txt_IN_distanza(self):
        return self._txt_IN_distanza

    @property
    def btn_analisi_grafo(self):
        return self._btn_analisi_grafo
    
    @property
    def txt_IN_string(self):
        return self._txt_IN_string
    
    @property
    def btn_calcola_percorso(self):
        return self._btn_calcola_percorso
    
    @property
    def dd_target(self):
        return self._dd_target
