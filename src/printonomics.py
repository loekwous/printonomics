import customtkinter as ctk
import logging
from PIL import Image
from events.app_events import MenuEvent
from events import EventQueue
from frame_factory import FrameFactory
from printo_controller import PrintoController, FrameManagerInterface


#setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TitleBar(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(border_width=1, corner_radius=1, fg_color="transparent")

        self.PADDING = {"padx": 10, "pady": 10}
        self.TITLE_STYLE = {"font": ("TkDefaultFont", 48, "bold"), "text_color": "silver", "bg_color": "transparent"}
        self.CREDITS_STYLE = {"font": ("TkDefaultFont", 12, "italic"), "text_color": "white", "bg_color": "transparent"}

        self.title_label = ctk.CTkLabel(
            self, text="Printonomics", **self.TITLE_STYLE
        )
        self.title_label.pack(side="left", anchor="w", **self.PADDING, expand=True, fill="both")

        self.credits_label = ctk.CTkLabel(
            self, text="by Loek Lankhorst © 2025", **self.CREDITS_STYLE
        )
        self.credits_label.pack(side="right", anchor="s", **self.PADDING)


class PrintonomicsMenu(ctk.CTkFrame):
    def __init__(self, event_queue: EventQueue, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_queue = event_queue

        self.PADDING = {"padx": 10, "pady": 10}

        pil_logo_image = Image.open("assets/printonomics.jpg")
        self.logo_image = ctk.CTkImage(light_image=pil_logo_image, size=(140, 140))
        self.logo_label = ctk.CTkLabel(self, image=self.logo_image, text="", bg_color="transparent")
        self.logo_label.pack(side="top", anchor="w", **self.PADDING)
        
        self.label = ctk.CTkLabel(self, text="Menu", font=("TkDefaultFont", 24, "bold"))
        self.label.pack(**{**self.PADDING, "pady": (100, 100)})

        self.menu_items: list[str] = ["Project", "Settings", "Help"]
        self.buttons: list[ctk.CTkButton] = []

        self.create_buttons()
    
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
            button.pack(**self.PADDING, fill="x", )
            self.buttons.append(button)


class ApplicationFrame(ctk.CTkFrame, FrameManagerInterface):
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


class Printonomics(ctk.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_queue = EventQueue()
        FrameFactory.set_event_queue(self.event_queue)

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.title("Printonomics")
        self.geometry(f"{int(screen_width * 0.6)}x{int(screen_height * 0.6)}+{int(screen_width * 0.1)}+{int(screen_height * 0.1)}")
        self.minsize(800, 600)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.after(300, lambda: self.iconbitmap("assets/printonomics.ico"))

        self.menu = PrintonomicsMenu(event_queue=self.event_queue, master=self)
        self.menu.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.title_bar = TitleBar(self)
        self.title_bar.grid(row=0, column=1, sticky="nsew")

        self.app_frame = ApplicationFrame(self)
        self.app_frame.grid(row=1, column=1, sticky="nsew")

        self._controller = PrintoController(self.app_frame, self.event_queue)

        self.periodic_event_handler()

    def periodic_event_handler(self):
        """Handle periodic events."""
        self._controller.process()
        self.after(100, self.periodic_event_handler)


if __name__ == "__main__":
    app = ctk.CTk()
    printonomics = Printonomics(app)
    printonomics.mainloop()
