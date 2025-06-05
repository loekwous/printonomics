import customtkinter as ctk
from app.events.app_events import FrameEvent
from app.settings.settings_manager import SettingsManager
from .events import AppEvent, EventQueue
from abc import ABC, abstractmethod


class AppFrameInterface(ABC, ctk.CTkFrame):
    """An interface for managing frames in the application."""

    @abstractmethod
    def set_queue(self, event_queue: EventQueue):
        """Set the event queue for the interface."""
        pass

    @abstractmethod
    def on_event(self, event: AppEvent):
        """Handle an event."""
        pass

    @abstractmethod
    def _push_event(self, event: AppEvent):
        """Push an event to the queue. only used internally."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the interface. used for buttons"""
        pass


class AppFrameSkeleton(AppFrameInterface):
    """A skeleton implementation of the AppFrameInterface"""

    def __init__(
        self, settings: SettingsManager, event_queue: EventQueue, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.frames = {}
        self.settings: SettingsManager = settings
        self.event_queue: EventQueue = event_queue
        self._name = ""

    def set_queue(self, event_queue: EventQueue):
        """Set the event queue for the interface."""
        self.event_queue = event_queue

    def on_event(self, event: AppEvent):
        """Handle an event. This method should be overridden in subclasses."""
        raise NotImplementedError("This method should be overridden in subclasses")

    @property
    def name(self) -> str:
        """Get the name of the interface. used for buttons"""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set the name of the interface. used for buttons"""
        self._name = value

    def _push_event(self, event: AppEvent):
        """Push an event to the queue. only used internally"""
        if not isinstance(event, FrameEvent):
            raise TypeError("Only FrameEvent childs can be pushed from a frame")
        if self.event_queue:
            self.event_queue.put(event)
        else:
            raise ValueError("Event queue is not set in the frame")
