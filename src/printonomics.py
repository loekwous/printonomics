import customtkinter as ctk
import logging

from help_frame import HelpFrame

from app import AppFrameSkeleton, Application, AppControllerSkeleton
from app.events import ControllerEvent, FrameEvent, SettingEvent
from app.settings import (
    BoolSettingSkeleton,
    IntSliderSettingSkeleton,
    StringSettingSkeleton,
)


# setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DemoControlEvent(ControllerEvent):
    def __init__(self):
        super().__init__("DemoControlEvent")


class DemoFrameEvent(FrameEvent):
    def __init__(self):
        super().__init__("DemoFrameEvent")


class FrameDemo(AppFrameSkeleton):
    def __init__(self, settings, event_queue, *args, **kwargs):
        super().__init__(settings, event_queue, *args, **kwargs)
        self._name = "FrameDemo"
        logging.info("FrameDemo initialized")

        self.button = ctk.CTkButton(
            self,
            text="Trigger Demo Event",
            command=lambda: self._push_event(DemoFrameEvent()),
        )
        self.button.pack(pady=20)

        self.label = ctk.CTkLabel(
            self, text="Nothing", font=("TkDefaultFont", 24, "bold")
        )
        self.label.pack(pady=20)

        self.setting_label = ctk.CTkLabel(
            self, text="Setting Value: " + str(self.settings.get_setting("Henk").value)
        )
        self.setting_label.pack(pady=20)

    def on_event(self, event):
        if isinstance(event, SettingEvent):
            self.label.configure(text=event.value)
        elif isinstance(event, DemoControlEvent):
            self.label.configure(text="Clicked")


class ControlDemo(AppControllerSkeleton):
    def init(self):
        logging.info("ControlDemo initialized")

    def on_event(self, event):
        if isinstance(event, DemoFrameEvent):
            self._push_event(DemoControlEvent())


class Printonomics(Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_new_frame("Help", HelpFrame)

        self.add_option(
            [
                BoolSettingSkeleton(name).with_description("Persional setting")
                for name in [
                    "Wim",
                    "Henk",
                ]
            ]
            + [
                StringSettingSkeleton("Naam"),
                IntSliderSettingSkeleton("Slider", 0, 0, 100).with_description(
                    "Set maximum volage of HVB [V]"
                ),
            ]
        )
        self.add_new_frame("FrameDemo", FrameDemo)
        self.add_controller(ControlDemo())
        self.set_icon("assets/printonomics.ico")
        self.set_logo("assets/printonomics.jpg")
        self.refresh_rate = 100


if __name__ == "__main__":
    app = ctk.CTk()
    printonomics = Printonomics(
        name="printonomics", copyright="Loek © 2025", master=app
    )
    printonomics.mainloop()
