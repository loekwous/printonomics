from app.app_frame import AppFrameSkeleton
import customtkinter as ctk


class SettingsFrame(AppFrameSkeleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # All settings are packed in a scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=400, height=300)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.setting_frames = []

        self.refresh()

    def refresh(self):
        for setting_frame in self.setting_frames:
            setting_frame.destroy()
        self.setting_frames.clear()

        for name, setting in self.settings.settings.items():
            setting.get_frame(self.scrollable_frame).pack(fill="x", padx=10, pady=5)
