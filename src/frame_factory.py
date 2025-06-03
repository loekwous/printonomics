from help_frame import HelpFrame
from settings_frame import SettingsFrame
from settings_manager import SettingsManager


class FrameFactory:

    settings = SettingsManager("settings.json")
    event_queue = None

    @staticmethod
    def set_event_queue(event_queue):
        """Set the event queue for the factory."""
        FrameFactory.event_queue = event_queue

    @staticmethod
    def create_frame(frame_type: str, *args, **kwargs):
        if not FrameFactory.event_queue:
            raise ValueError("Event queue must be set before creating frames.")

        """Factory method to create frames based on the frame type."""
        match frame_type:
            case "help":
                return HelpFrame(FrameFactory.settings, FrameFactory.event_queue, *args, **kwargs)
            case "settings":
                return SettingsFrame(FrameFactory.settings, FrameFactory.event_queue, *args, **kwargs)
            case _:
                raise ValueError(f"Unknown frame type: {frame_type}")