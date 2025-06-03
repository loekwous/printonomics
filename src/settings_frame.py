from events import EventQueue
from app_frame import AppFrame
from settings_manager import Setting, SettingType
from events.app_events import SettingEvent
import customtkinter as ctk


class SettingElementFrame(ctk.CTkFrame):
    def __init__(self, event_queue: EventQueue, setting: Setting, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setting = setting
        
        ctk.CTkLabel(self, text=setting.name, font=("Arial", 16)).pack(pady=10, padx=20)
        
        if setting.setting_type == SettingType.STRING:
            self.setting_input = ctk.CTkEntry(self, placeholder_text=setting.value)
        elif setting.setting_type == SettingType.INTEGER:
            # self.setting_input = ctk.CTkEntry(self, placeholder_text=str(setting.value))
            self.setting_input = ctk.CTkSlider(self, from_=setting.min_value, to=setting.max_value, number_of_steps=setting.max_value - setting.min_value,
                                               command=lambda value: event_queue.put(SettingEvent(setting, value)))
        elif setting.setting_type == SettingType.BOOLEAN:
            self.setting_input = ctk.CTkSwitch(self, text="", command=lambda: event_queue.put(SettingEvent(setting, self.setting_input.get())))
            self.setting_input.select() if setting.value else self.setting_input.deselect()
        elif setting.setting_type == SettingType.FLOAT:
            self.setting_input = ctk.CTkEntry(self, placeholder_text=str(setting.value))
        else:
            raise ValueError(f"Unsupported setting type: {setting.setting_type}")
        
        self.setting_input.pack(side="right", anchor="center", pady=10, padx=20)


class SettingsFrame(AppFrame):
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
        
        for setting_name in self.settings.settings:
            self.setting_frames.append(
                SettingElementFrame(self.event_queue, self.settings.settings[setting_name], self.scrollable_frame)
            )
            self.setting_frames[-1].pack(fill="x", padx=10, pady=5)