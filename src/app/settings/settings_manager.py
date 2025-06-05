import json
from dataclasses import dataclass
import os
import os.path
import logging
from abc import ABC, abstractmethod
import customtkinter as ctk
import queue


@dataclass
class SettingInterface(ABC):
    name: str
    default_value: any = None
    min_value: any = None
    max_value: any = None
    value: any = None  # Current value of the setting
    options: list[str] = None  # For LIST type settings

    def __post_init__(self):
        self._queue: queue.Queue = None

    def set_queue(self, queue: queue.Queue):
        """
        Sets the queue for the setting.
        This is used to communicate changes in the setting value.
        """
        self._queue = queue

    @abstractmethod
    def get_frame(self, frame_root) -> ctk.CTkFrame:
        """
        Returns a CTkFrame that contains the setting.
        This method should be implemented by subclasses
        to provide the specific UI for the setting.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class SettingsManager:
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.settings_raw = {"settings": []}
        self.settings: dict[str, SettingInterface] = {}
        self.load_raw_settings()

    def add_setting(self, setting: SettingInterface):
        if not isinstance(setting, SettingInterface):
            raise TypeError("Setting must be an instance of SettingInterface.")

        if setting.name in self.settings:
            raise KeyError(f"Setting '{setting.name}' already exists.")

        if setting.name in [item["name"] for item in self.settings_raw["settings"]]:
            logging.debug(
                f"Setting '{setting.name}' already exists in raw settings. Overwriting."
            )
            # Attempt to populate the setting from raw data
            self._try_populate_setting(setting)

        self.settings[setting.name] = setting

        logging.debug(f"Added setting: {setting.name}")

    def _try_populate_setting(self, setting: SettingInterface) -> None:
        """
        Attemps to populate a setting from raw data.
        """
        for raw_setting in self.settings_raw["settings"]:
            if raw_setting["name"] == setting.name:
                for key, value in raw_setting.items():
                    if hasattr(setting, key):
                        setattr(setting, key, value)
                logging.debug(
                    f"Populated setting '{setting.name}' from raw data: {raw_setting}"
                )
                return

    def load_raw_settings(self):
        try:
            if not os.path.exists(self.settings_file):
                logging.debug(
                    f"Settings file {self.settings_file} not found. Creating a new one."
                )

            with open(self.settings_file, "r") as file:
                self.settings_raw = json.load(file)
        except FileNotFoundError:
            self.settings_raw = {}
        except json.JSONDecodeError:
            print(
                "Error decoding JSON from settings file. Starting with empty settings."
            )
            self.settings_raw = {}

    @property
    def setting_names(self):
        return list(self.settings.keys())

    def create_raw_settings(self):
        self.settings_raw["settings"] = []
        for item in self.settings.values():
            filtered_dict = {
                k: v
                for k, v in item.__dict__.items()
                if isinstance(v, (str, int, float, bool, list))
            }
            self.settings_raw["settings"].append(filtered_dict)

    def save_settings(self):
        self.create_raw_settings()
        with open(self.settings_file, "w") as file:
            json.dump(self.settings_raw, file, indent=4)

    def get_setting(self, key, default=None) -> SettingInterface:
        return self.settings.get(key, default)
