from abc import ABC


class AppEvent(ABC):
    """An event that is triggered by the application. this class is used to define the interface for all events in the application.
    It is an abstract base class that defines the methods that must be implemented by all events.
    """


class MenuEvent(AppEvent):
    """An event that is triggered by the menu. This class is used to define the interface for all menu events in the application.
    It is an abstract base class that defines the methods that must be implemented by all menu events.
    """

    def __init__(self, menu_item: str):
        self.item = menu_item


class ControllerEvent(AppEvent):
    """An event that is triggered by the controller. This class is used to define the interface for all controller events in the application.
    It is an abstract base class that defines the methods that must be implemented by all controller events.
    """

    def __init__(self, controller_name: str):
        self.controller_name = controller_name


class FrameEvent(AppEvent):
    """An event that is triggered by the frame. This class is used to define the interface for all frame events in the application.
    It is an abstract base class that defines the methods that must be implemented by all frame events.
    """

    def __init__(self, frame_name: str):
        self.frame_name = frame_name


class SettingEvent(AppEvent):
    """An event that is triggered by a setting change. This class is used to define the interface for all setting events in the application.
    It is an abstract base class that defines the methods that must be implemented by all setting events.
    """

    def __init__(self, setting, value):
        self.setting = setting
        self.value = value
