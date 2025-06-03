from abc import ABC, abstractmethod
import logging


class AppEvent(ABC):
    """An event that is triggered by the application. this class is used to define the interface for all events in the application.
    It is an abstract base class that defines the methods that must be implemented by all events.
    """
    @abstractmethod
    def trigger(self):
        """Trigger the event. This method must be implemented by all events."""
        pass


class MenuEvent(AppEvent):
    """An event that is triggered by the menu. This class is used to define the interface for all menu events in the application.
    It is an abstract base class that defines the methods that must be implemented by all menu events.
    """
    def __init__(self, item: str):
        self.item = item

    def trigger(self):
        """Trigger the menu event."""
        logging.info(f"Menu event triggered for item: {self.item}")
        # Here you can add functionality for each menu item click
        # For example, open a new window or perform an action based on the item clicked


class SettingEvent(AppEvent):
    """An event that is triggered by a setting change. This class is used to define the interface for all setting events in the application.
    It is an abstract base class that defines the methods that must be implemented by all setting events.
    """
    def __init__(self, setting, value):
        self.setting = setting
        self.value = value

    def trigger(self):
        """Trigger the setting event."""
        logging.info(f"Setting event triggered for {self.setting.name} with value: {self.value}")
        # Here you can add functionality to handle the setting change