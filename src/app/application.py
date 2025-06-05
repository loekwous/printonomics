import customtkinter as ctk
import logging
from PIL import Image
import sys
import os

from app.app_frame import AppFrameInterface
from .events.app_events import MenuEvent
from .events.app_event_queue import EventQueue
from .frame_factory import FrameFactory
from app.app_controller import (
    AppControlLogicInterface,
    AppController,
    FrameManagerInterface,
)
from .settings.settings_manager import SettingInterface
from .settings.settings_frame import SettingsFrame


# setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class AppTitleBar(ctk.CTkFrame):
    def __init__(self, title: str, copyright: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(border_width=1, corner_radius=1, fg_color="transparent")

        self.PADDING = {"padx": 10, "pady": 10}
        self.TITLE_STYLE = {
            "font": ("TkDefaultFont", 48, "bold"),
            "text_color": "silver",
            "bg_color": "transparent",
        }
        self.CREDITS_STYLE = {
            "font": ("TkDefaultFont", 12, "italic"),
            "text_color": "white",
            "bg_color": "transparent",
        }

        self.title_label = ctk.CTkLabel(self, text=title, **self.TITLE_STYLE)
        self.title_label.pack(
            side="left", anchor="w", **self.PADDING, expand=True, fill="both"
        )

        self.credits_label = ctk.CTkLabel(self, text=copyright, **self.CREDITS_STYLE)
        self.credits_label.pack(side="right", anchor="s", **self.PADDING)


class AppMenu(ctk.CTkFrame):
    def __init__(self, event_queue: EventQueue, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_queue = event_queue

        self.PADDING = {"padx": 10, "pady": 10}

        self.logo_label = ctk.CTkLabel(
            self, text="", bg_color="transparent", width=140, height=140
        )
        self.logo_label.pack(side="top", anchor="w", **self.PADDING)

        self.label = ctk.CTkLabel(self, text="Menu", font=("TkDefaultFont", 24, "bold"))
        self.label.pack(**{**self.PADDING, "pady": (100, 100)})

        self.menu_items: list[str] = []
        self.buttons: list[ctk.CTkButton] = []

        self.create_buttons()

    def set_logo(self, logo_path: str):
        """Set the logo image for the menu."""
        pil_logo_image = Image.open(logo_path)
        height_ratio = pil_logo_image.height / pil_logo_image.width
        self.logo_image = ctk.CTkImage(
            light_image=pil_logo_image, size=(140, int(140 * height_ratio))
        )
        self.logo_label.configure(image=self.logo_image)

    def on_button_click(self, item: str):
        """Handle button click events."""
        self.event_queue.put(MenuEvent(item.lower()))

    def create_buttons(self):
        """Create buttons for the menu."""
        # Clear existing buttons
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()

        # Create new buttons
        for item in self.menu_items:
            button = ctk.CTkButton(
                self, text=item, command=lambda item=item: self.on_button_click(item)
            )
            button.pack(
                **self.PADDING,
                fill="x",
                side="bottom",
            )
            self.buttons.append(button)


class AppActionFrame(ctk.CTkFrame, FrameManagerInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(border_width=1, corner_radius=1, fg_color="transparent")
        self.current_frame: ctk.CTkFrame = None

    @property
    def frame(self) -> ctk.CTkFrame:
        """Get the current frame."""
        return self.current_frame

    @frame.setter
    def frame(self, frame: ctk.CTkFrame):
        """Set the current frame."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    def clear(self):
        """Clear the current frame."""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None


class Application(ctk.CTkToplevel):

    def __init__(
        self,
        name: str = "MyApplication",
        copyright: str = "Loek © 2025",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.event_queue = EventQueue()
        FrameFactory.set_event_queue(self.event_queue)

        self._refresh_rate = 100  # milliseconds

        # If theme file not found, try to load from PyInstaller bundle
        if hasattr(sys, "_MEIPASS"):
            theme_path = os.path.join(sys._MEIPASS, "assets", "theme.json")
        else:
            theme_path = "assets/theme.json"
        ctk.set_default_color_theme(theme_path)

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.title("Printonomics")
        self.geometry(
            f"{int(screen_width * 0.6)}x{int(screen_height * 0.6)}"
            + f"+{int(screen_width * 0.1)}+{int(screen_height * 0.1)}"
        )
        self.minsize(800, 600)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.menu = AppMenu(event_queue=self.event_queue, master=self)
        self.menu.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.title_bar = AppTitleBar(title=name, copyright=copyright, master=self)
        self.title_bar.grid(row=0, column=1, sticky="nsew")

        self.app_frame = AppActionFrame(self)
        self.app_frame.grid(row=1, column=1, sticky="nsew")

        self._controller = AppController(self.app_frame, self.event_queue)

        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.add_new_frame("Settings", SettingsFrame)

        self._periodic_task()

    def _on_closing(self):
        """Handle the window closing event."""
        logging.info("Application is closing.")
        FrameFactory.settings.save_settings()
        self.quit()
        self.destroy()

    def set_icon(self, icon_path: str):
        self.after(300, lambda: self.iconbitmap(icon_path))

    def set_logo(self, logo_path: str):
        self.menu.set_logo(logo_path)

    @property
    def refresh_rate(self) -> int:
        """Get the refresh rate in milliseconds."""
        return self._refresh_rate

    @refresh_rate.setter
    def refresh_rate(self, value: int):
        """Set the refresh rate in milliseconds."""
        if value <= 0:
            raise ValueError("Refresh rate must be a positive integer.")
        self._refresh_rate = value
        logging.info(f"Refresh rate set to {self._refresh_rate} milliseconds")

    def _periodic_task(self):
        """Handle periodic events."""
        self._controller.process_events()
        self.after(self._refresh_rate, self._periodic_task)

    def add_new_frame(self, name: str, frame_type: AppFrameInterface):
        """Add a new frame to the application."""
        if not issubclass(frame_type, AppFrameInterface):
            raise ValueError("Frame must be a type of AppFrameInterface")
        FrameFactory.frames[f"{name.lower()}"] = frame_type
        self.menu.menu_items.append(name)
        self.menu.create_buttons()
        logging.info(f"Added new frame: {name.lower()}")

    def add_controller(self, controller: AppControlLogicInterface):
        """Add a new controller to the application."""
        if not isinstance(controller, AppControlLogicInterface):
            raise ValueError(
                "Controller must be an instance of AppControlLogicInterface"
            )
        self._controller.add_controller(controller)
        logging.info(f"Added new controller: {controller.__class__.__name__}")

    def add_option(
        self,
        option: (
            SettingInterface | list[SettingInterface] | tuple[SettingInterface, ...]
        ),
    ):
        """Add a new option or multiple options to the application."""
        options = option
        if isinstance(option, (list, tuple)):
            for opt in options:
                self.add_option(opt)
        else:
            if not isinstance(option, SettingInterface):
                raise ValueError("Option must be an instance of SettingInterface")
            option.set_queue(self.event_queue)
            FrameFactory.settings.add_setting(option)
            logging.info(f"Added new option: {option.__class__.__name__}")
