import flet as ft
from soundboard.data_store import DataStore
from soundboard.ui import UserInterface

def main(page: ft.Page):
    data_store = DataStore()
    ui = UserInterface(data_store=data_store, page=page)
    ui.mount()
    page.add(ui)
    page.update()

ft.app(target=main)
