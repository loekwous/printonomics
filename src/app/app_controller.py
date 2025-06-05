from typing import Callable
import logging
from abc import ABC, abstractmethod
from .frame_factory import FrameFactory
from .events import (
    AppEvent,
    MenuEvent,
    ControllerEvent,
    FrameEvent,
    SettingEvent,
    EventQueue,
)


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


class AppControlLogicInterface(ABC):
    """Interface for the application control logic."""

    @abstractmethod
    def init(self):
        """Initialize the control logic."""
        pass

    @abstractmethod
    def set_queue(EventQueue):
        """Set the event queue for the application."""
        pass

    @abstractmethod
    def on_event(event: AppEvent):
        """Handle an event from the event queue."""
        pass

    @abstractmethod
    def _push_event(event: AppEvent):
        """Push an event to the event queue. for internal use only."""
        pass


class AppControllerSkeleton(AppControlLogicInterface):
    """A skeleton implementation of the AppControlLogicInterface"""

    def init(self):
        raise NotImplementedError("init method must be implemented in subclasses")

    def set_queue(self, event_queue: EventQueue):
        self.event_queue = event_queue

    def on_event(self, event: AppEvent):
        raise NotImplementedError("on_event method must be implemented in subclasses")

    def _push_event(self, event: AppEvent):
        if not isinstance(event, ControllerEvent):
            raise TypeError(
                "Only ControllerEvent childs can be pushed from a controller"
            )
        if self.event_queue:
            self.event_queue.put(event)
        else:
            raise ValueError("Event queue is not set in the controller")


class AppController:
    def __init__(self, frame_manager: FrameManagerInterface, event_queue: EventQueue):
        self.frame_manager = frame_manager
        self.event_queue = event_queue
        self._controllers = []

    def add_controller(self, controller: AppControlLogicInterface):
        controller.set_queue(self.event_queue)
        self._controllers.append(controller)
        controller.init()

    def _handle_menu_event(self, event: MenuEvent):
        # Try to create a new frame based on the menu event
        try:
            new_frame = FrameFactory.create_frame(event.item, self.frame_manager)
            self.frame_manager.frame = new_frame
            FrameFactory.settings.save_settings()
        except ValueError as e:
            logging.error(
                f"Error creating frame, event is probably not implemented: {e}"
            )
            self.frame_manager.clear()

    def _handle_frame_event(self, event: FrameEvent):
        # Handle frame events, such as switching frames or updating the current frame
        if hasattr(self.frame_manager.frame, "on_event"):
            self.frame_manager.frame.on_event(event)

    def _update_event_handlers(self):
        """Create a mapping of event types to their handlers."""
        all_controller_handlers = [
            controller.on_event for controller in self._controllers
        ]

        self._event_routing: dict[type, list[Callable[[AppEvent], None]]] = {
            MenuEvent: [
                self._handle_menu_event,
                *all_controller_handlers,
            ],
            SettingEvent: [
                *all_controller_handlers,
            ],
            ControllerEvent: [
                (self._handle_frame_event),
            ],
            FrameEvent: [
                *all_controller_handlers,
            ],
        }

    def process_events(self):
        """Process all events currently in the event queue"""
        self._update_event_handlers()

        available_events = iter(lambda: self.event_queue.get(), None)

        for event in available_events:
            for event_type, handlers in self._event_routing.items():
                if isinstance(event, event_type):
                    for handler in handlers:
                        handler(event)
