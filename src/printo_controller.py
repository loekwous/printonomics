from events import EventQueue
from events.app_events import MenuEvent, SettingEvent
import logging
from abc import ABC, abstractmethod
from frame_factory import FrameFactory
import customtkinter as ctk

from settings_manager import Setting


class FrameManagerInterface(ABC):
    """Interface for managing frames in the Printo application."""

    @property
    @abstractmethod
    def frame(self, frame):
        """Set the current frame."""
        pass

    @frame.setter
    @abstractmethod
    def frame(self):
        """Get the current frame."""
        pass

    @abstractmethod
    def clear(self):
        """Clear the current frame."""
        pass

class PrintoController:
    def __init__(self, frame_manager: FrameManagerInterface, event_queue: EventQueue):
        self.frame_manager = frame_manager
        self.event_queue = event_queue

    def process(self):
        if event := self.event_queue.get():
            event.trigger()
            if isinstance(event, MenuEvent):
                try:
                    new_frame = FrameFactory.create_frame(event.item, self.frame_manager)
                    self.frame_manager.frame = new_frame
                    self.settings = FrameFactory.settings.save_settings()
                except ValueError as e:
                    logging.error(f"Error creating frame, event is probably not implemented: {e}")
                    self.frame_manager.clear()
            elif isinstance(event, SettingEvent):
                match event.setting.name:
                    case "Dark mode":
                        event.setting.value = bool(event.value)
                        FrameFactory.settings.set_setting(event.setting)
                        ctk.set_appearance_mode("dark" if event.value else "light")
                    case "Font size":
                        pass
            else:
                logging.warning(f"Unknown event type: {type(event)}")