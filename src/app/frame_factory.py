from .app_frame import AppFrameInterface
from app.settings.settings_manager import SettingsManager


class FrameFactory:

    settings = SettingsManager("app_settings.json")
    event_queue = None

    frames: dict[str, AppFrameInterface] = {}

    @staticmethod
    def set_event_queue(event_queue):
        """Set the event queue for the factory."""
        FrameFactory.event_queue = event_queue

    @staticmethod
    def create_frame(frame_type: str, *args, **kwargs) -> AppFrameInterface:
        if not FrameFactory.event_queue:
            raise ValueError("Event queue must be set before creating frames.")

        if frame_type not in FrameFactory.frames:
            raise ValueError(
                f"Frame type '{frame_type}' is not registered in FrameFactory."
            )

        return FrameFactory.frames[frame_type](
            FrameFactory.settings, FrameFactory.event_queue, *args, **kwargs
        )
