from functools import partial
import flet as ft
from flet import UserControl
from typing import Any

from pathlib import Path
from soundboard.data_store import DataStore
from soundboard.sound import SoundBite

class UserInterface(UserControl):

    def __init__(self, data_store: DataStore, page: ft.Page, **kwargs: Any):
        super().__init__(**kwargs)
        self.data_store = data_store
        self.page = page
        self.playing = False
        self.paused = False

    def build(self):
        self.all_play_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            selected_icon=ft.icons.STOP,
            on_click=lambda _: self.all_play_toggle(),
            selected=self.playing,
            style=ft.ButtonStyle(color={"selected": ft.colors.LIGHT_BLUE, "": ft.colors.BLUE})
        )
        self.all_pause_button = ft.IconButton(
            icon=ft.icons.PAUSE,
            selected_icon=ft.icons.PAUSE,
            on_click=lambda _: self.all_pause_toggle(),
            selected=self.paused,
            style=ft.ButtonStyle(color={"selected": ft.colors.LIGHT_BLUE, "": ft.colors.BLUE}),
        )
        self.global_volume_slider = ft.Slider(
            value=0.8,
            min=0,
            max=1,
            on_change=lambda _: self.volume_change(),
        )

        self.top_row = ft.Row(
            [
                ft.ElevatedButton(
                    text="Pick Files",
                    on_click=lambda _: self.pick_files_dialog.pick_files(allow_multiple=True),
                ),
                ft.Row([
                self.all_play_button,
                self.all_pause_button,
                self.global_volume_slider,
                ],
                ),
            ]
        )
        self.sounds = ft.Column()
        return ft.Column([self.top_row, self.sounds])

    def volume_change(self):
        for sound in self.sounds.controls:
            sound.volume_change()

    def add_sound(self, file: str):
        name = Path(file).stem
        bite = SoundBite(name = name, path = file, global_volume_slider=self.global_volume_slider, global_ui=self)
        self.sounds.controls.append(bite)
        self.update()
        bite.mount(self.page)
        self.page.update()

    def refresh_sounds(self):
        for file in self.data_store.loop_unadded_files():
            self.add_sound(file)
            self.data_store.mark_file_as_added(file)

    def all_play_toggle(self):
        if self.playing:
            for sound in self.sounds.controls:
                sound.hard_stop()
        else:
            for sound in self.sounds.controls:
                sound.hard_play()
        self.sound_bite_change()

    def all_pause_toggle(self):
        if self.paused:
            for sound in self.sounds.controls:
                sound.hard_unpause()
        else:
            for sound in self.sounds.controls:
                sound.hard_pause()
        self.sound_bite_change()

    def button_update(self):
        self.all_play_button.selected = self.playing
        self.all_pause_button.selected = self.paused
        self.all_pause_button.bgcolor = ft.colors.INVERSE_PRIMARY if self.paused else None
        self.update()

    def sound_bite_change(self):
        self.playing = any([sound.playing for sound in self.sounds.controls])
        self.paused = all([sound.paused for sound in self.sounds.controls])
        self.button_update()


    def add_file_picker(self):
        def pick_files_result(e: ft.FilePickerResultEvent, data_store: DataStore):
            for file in e.files:
                if file.path not in data_store["files"]:
                    data_store.add_file(file.path)
            self.refresh_sounds()
        new_pick_files_result = partial(pick_files_result, data_store = self.data_store)
        self.pick_files_dialog = ft.FilePicker(on_result=new_pick_files_result)

    def mount(self):
        self.add_file_picker()
        self.page.overlay.append(self.pick_files_dialog)
