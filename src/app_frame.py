import customtkinter as ctk
from settings_manager import SettingsManager
from events.app_event_queue import EventQueue

class AppFrame(ctk.CTkFrame):
    """An interface for managing frames in the application."""

    def __init__(self, settings: SettingsManager, event_queue: EventQueue, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.frames = {}
        self.settings: SettingsManager = settings
        self.event_queue: EventQueue = event_queue

    def add_frame(self, name: str, frame: ctk.CTkFrame):
        """Add a frame to the interface."""
        self.frames[name] = frame
        frame.pack(fill="both", expand=True)

    def remove_frame(self, name: str):
        """Remove a frame from the interface."""
        if name in self.frames:
            self.frames[name].pack_forget()
            del self.frames[name]