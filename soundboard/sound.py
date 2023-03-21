from enum import Enum
import flet as ft

from typing import Any
from flet import (
    IconButton,
    TextField,
    Row,
    UserControl,
    colors,
    icons,
)


class SoundType(Enum):
    BACKGROUND = "Background"
    EFFECT = "Effect"


class ReleaseMode(Enum):
    RELEASE = "release"
    LOOP = "loop"
    STOP = "stop"


class SoundBite(UserControl):
    def __init__(
        self,
        name: str,
        path: str,
        global_volume_slider: ft.Slider = None,
        global_ui=None,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.name = name
        self.path = path
        self.global_volume_slider = global_volume_slider
        self.global_ui = global_ui  # Hacky way to get access to the UI

        # Controls
        self.playing = False
        self.paused = False
        self.looping = False

        # Audio
        self.default_volume = 0.5
        self.audio = ft.Audio(
            src=self.path,
            autoplay=False,
            balance=0,
            volume=self.default_volume * self.global_volume_slider.value,
            on_state_changed=lambda e: self.state_change(e),
        )

    def mount(self, page: ft.Page):
        page.overlay.append(self.audio)
    def name_click(self):
        self.display_name.visible = False
        self.edit_name.visible = True
        self.update()
        self.edit_name.controls[0].focus()

    def name_change(self):
        self.name = self.edit_name.controls[0].value
        self.display_name.visible = True
        self.edit_name.visible = False
        self.display_name.text = self.name
        self.update()
        self.global_ui.sound_bite_change()

<<<<<<< Updated upstream
    def build(self):
=======
    def name_click(self):
        self.display_name.visible = False
        self.edit_name.visible = True
        self.update()
        self.edit_name.controls[0].focus()

    def name_change(self):
        self.name = self.edit_name.controls[0].value
        self.display_name.visible = True
        self.edit_name.visible = False
        self.display_name.text = self.name
        self.update()
        self.global_ui.sound_bite_change()

    def build_components(self):
>>>>>>> Stashed changes
        self.display_name = ft.TextButton(
            text=self.name, on_click=lambda _: self.name_click()
        )
        self.edit_name = ft.Column(
            [
                TextField(
                    value=self.name,
                    on_submit=lambda _: self.name_change(),
                ),
                ft.IconButton(
                    icon=icons.SAVE,
                    on_click=lambda _: self.name_change(),
                ),
            ],
            visible=False,
        )
<<<<<<< Updated upstream
=======
        self.move_button = IconButton(
            icon=icons.ARROW_FORWARD,
            on_click=lambda _: self.global_ui.move_sound(self),
            style=ft.ButtonStyle(color={colors.BLUE}),
        )
>>>>>>> Stashed changes
        self.play_button = IconButton(
            icon=icons.PLAY_ARROW,
            selected_icon=icons.STOP,
            on_click=lambda _: self.play_toggle(),
            selected=self.playing,
            style=ft.ButtonStyle(
                color={"selected": colors.LIGHT_BLUE, "": colors.BLUE}
            ),
        )
        self.volume_slider = ft.Slider(
            value=self.default_volume,
            min=0,
            max=1,
            on_change=lambda _: self.volume_change(),
        )
<<<<<<< Updated upstream
        self.elements = [
            self.display_name,
            self.edit_name,
            self.volume_slider,
            self.play_button
        ]
=======
        self.pause_button = IconButton(
            icon=icons.PAUSE,
            selected_icon=icons.PAUSE,
            on_click=lambda _: self.pause_toggle(),
            selected=self.paused,
            style=ft.ButtonStyle(
                color={"selected": colors.LIGHT_BLUE, "": colors.BLUE}
            ),
        )
        if self.paused:
            self.pause_button.bgcolor = colors.LIGHT_BLUE
        self.loop_button = IconButton(
            icon=icons.LOOP,
            selected_icon=icons.LOOP,
            on_click=lambda _: self.loop_toggle(),
            selected=self.looping,
            style=ft.ButtonStyle(
                color={"selected": colors.LIGHT_BLUE, "": colors.BLUE}
            ),
        )
        if self.looping:
            self.loop_button.bgcolor = colors.LIGHT_BLUE
>>>>>>> Stashed changes

    def build(self):
        "Empty build for abstract class"
        return Row()

    def hard_stop(self):
        self.audio.pause()
        self.playing = False
        self.paused = False
        self.select_button()

    def hard_unpause(self):
        self.audio.resume()
        self.playing = True
        self.paused = False
        self.select_button()

    def hard_play(self):
        self.audio.play()
        self.playing = True
        self.paused = False
        self.select_button()

    def hard_pause(self):
        self.audio.pause()
        self.playing = False
        self.paused = True
        self.select_button()

    def play_toggle(self):
        if self.playing:
            self.audio.pause()
            self.playing = False
            self.paused = False
        else:
            self.audio.play()
            self.playing = True
            self.paused = False
        self.select_button()

    def pause_toggle(self):
        if self.playing:
            self.audio.pause()
            self.paused = True
            self.playing = False
        elif self.paused:
            self.audio.resume()
            self.paused = False
            self.playing = True
        self.select_button()

    def loop_toggle(self):
        if self.looping:
            self.audio.release_mode = ReleaseMode.RELEASE
            self.looping = False
        else:
            self.audio.release_mode = ReleaseMode.LOOP
            self.looping = True
        self.audio.update()
        self.loop_button.selected = self.looping
        self.loop_button.bgcolor = colors.INVERSE_PRIMARY if self.looping else None
        self.update()

    def select_button(self):
        self.pause_button.bgcolor = colors.INVERSE_PRIMARY if self.paused else None
        self.pause_button.selected = self.paused
        self.play_button.selected = self.playing
        self.update()
        self.global_ui.sound_bite_change()

    def volume_change(self):
        self.audio.volume = self.volume_slider.value * self.global_volume_slider.value
        self.audio.update()

    def state_change(self, e):
        if e.data == "completed":
            self.playing = False
            self.paused = False
            self.select_button()


class BackgroundSound(SoundBite):
    def __init__(self, path, name, global_ui, global_volume_slider):
        super().__init__(
            path=path,
            name=name,
            global_ui=global_ui,
            global_volume_slider=global_volume_slider,
        )
        self.type = SoundType.BACKGROUND

    def build(self):
        super().build_components()
        self.elements = [
            self.display_name,
            self.edit_name,
            self.move_button,
            self.volume_slider,
            self.play_button,
            self.pause_button,
            self.loop_button,
        ]

        return Row(self.elements)


class EffectSound(SoundBite):
    def __init__(self, path, name, global_ui, global_volume_slider):
        super().__init__(path, name, global_ui, global_volume_slider)
        self.type = SoundType.EFFECT

    def build(self):
        super().build_components()
        self.elements = [
            ft.Row([self.display_name, self.edit_name, self.move_button]),
            ft.Row([self.play_button, self.volume_slider]),
        ]
        return Row(self.elements)
