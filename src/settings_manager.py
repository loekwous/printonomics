from email.policy import default
import json
from dataclasses import dataclass
import enum
import os
import os.path
import logging

DEFAULT_SETTINGS = {
    "settings": [
        {
            "name": "Dark mode",
            "setting_type": "boolean",
            "default_value": True,
            "value": True,
        },
        {
            "name": "Font size",
            "setting_type": "integer",
            "default_value": 12,
            "min_value": 8,
            "max_value": 20,
            "value": 12,
        }
    ]
}

class SettingType(enum.Enum):
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    LIST = "list"


@dataclass
class Setting:
    name: str
    setting_type: SettingType
    default_value: any = None
    min_value: any = None
    max_value: any = None
    value: any = None  # Current value of the setting
    options: list[str] = None  # For LIST type settings

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "setting_type": self.setting_type.value,
            "default_value": self.default_value,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "value": bool(self.value),
            "options": self.options if self.options is not None else [],
        }

    @staticmethod
    def from_dict(data: dict) -> 'Setting':
        if 'name' not in data or 'setting_type' not in data:
            raise ValueError("Invalid setting data: 'name' and 'setting_type' are required.")
        
        setting_type = SettingType(data['setting_type'])
        match setting_type:
            case SettingType.STRING:
                return Setting(
                    name=data['name'],
                    setting_type=setting_type,
                    default_value=data.get('default_value', ''),
                    value=data.get('value', data.get('default_value', 0.0),),
                    options=data.get('options', []),  # For LIST type settings
                )
            case SettingType.INTEGER:
                return Setting(
                    name=data['name'],
                    setting_type=setting_type,
                    default_value=data.get('default_value', 0),
                    value=data.get('value', data.get('default_value', 0.0),),
                    min_value=data.get('min_value'),
                    max_value=data.get('max_value'),
                )
            case SettingType.BOOLEAN:
                return Setting(
                    name=data['name'],
                    setting_type=setting_type,
                    default_value=data.get('default_value', False),
                    value=data.get('value', data.get('default_value', 0.0),),
                )
            case SettingType.FLOAT:
                return Setting(
                    name=data['name'],
                    setting_type=setting_type,
                    default_value=data.get('default_value', 0.0),
                    min_value=data.get('min_value'),
                    max_value=data.get('max_value'),
                    value=data.get('value', data.get('default_value', 0.0),),
                )
            case _:
                raise ValueError(f"Unsupported setting type: {setting_type}")


class SettingsManager:
    def __init__(self, settings_file='settings.json'):
        self.settings_file = settings_file
        self.settings_raw = {}
        self.settings: dict[str, Setting] = {}
        self.load_settings()

    def _create_default_settings(self):
        with open(self.settings_file, 'w') as file:
            json.dump(DEFAULT_SETTINGS, file, indent=4)

    def load_settings(self):
        try:
            if not os.path.exists(self.settings_file):
                logging.debug(f"Settings file {self.settings_file} not found. Creating a new one.")
                self._create_default_settings()

            with open(self.settings_file, 'r') as file:
                self.settings_raw = json.load(file)
        except FileNotFoundError:
            self.settings_raw = {}
        except json.JSONDecodeError:
            print("Error decoding JSON from settings file. Starting with empty settings.")
            self.settings_raw = {}

        for setting_data in self.settings_raw.get('settings', []):
            try:
                setting = Setting.from_dict(setting_data)
                self.settings[setting.name] = setting
            except ValueError as e:
                logging.error(f"Error loading setting {setting_data}: {e}")

    @property
    def setting_names(self):
        return list(self.settings_raw.keys())

    def create_raw_settings(self):
        self.settings_raw = {
            "settings": [setting.to_dict() for setting in self.settings.values()]
        }

    def save_settings(self):
        self.create_raw_settings()
        with open(self.settings_file, 'w') as file:
            json.dump(self.settings_raw, file, indent=4)

    def get_setting(self, key, default=None) -> Setting:
        return self.settings.get(key, default)

    def set_setting(self, setting: Setting):
        if setting.name not in self.settings:
            raise KeyError(f"Setting '{setting.name}' does not exist.")
        self.settings[setting.name] = setting