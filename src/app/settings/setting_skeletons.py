from typing import Any
import customtkinter as ctk
from .settings_manager import SettingInterface
from ..events import SettingEvent


class BasicSettingSkeleton(SettingInterface):
    """A skeleton implementation of a basic setting."""

    def __init__(self, name: str, default_value: str = "", *args, **kwargs):
        super().__init__(name=name, default_value=default_value, *args, **kwargs)
        self.value = default_value

    def with_description(self, description: str) -> "BasicSettingSkeleton":
        """Set the description for the setting."""
        self.description = description
        return self

    def _check_value(self, value: Any) -> Any:
        raise NotImplementedError("Subclasses must implement _check_value method")

    def _get_value_object(self) -> tuple[ctk.Variable, ctk.CTkBaseClass]:
        raise NotImplementedError("Subclasses must implement _get_value_object method")

    def get_frame(self, frame_root) -> ctk.CTkFrame:
        """Create a frame for the basic setting."""
        self.frame = ctk.CTkFrame(frame_root)
        self.frame.configure(bg_color="grey", corner_radius=2, border_width=1)

        self.label = ctk.CTkLabel(
            self.frame, text=self.name, font=("Arial", 18, "bold")
        )
        self.label.pack(padx=10, pady=10, anchor="center")

        self.variable, self.value_entry = self._get_value_object()
        if self.variable is None:
            self.value_entry.configure(command=self._on_change)
        else:
            self.variable.trace_add("write", lambda *args: self._on_change())

        self.value_entry.pack(side="right", padx=10, pady=10, anchor="e")

        if hasattr(self, "description"):
            self.description_label = ctk.CTkLabel(
                self.frame,
                text=self.description,
                font=("Arial", 16, "italic"),
                text_color="grey",
            )
            self.description_label.pack(padx=10, pady=5)

        return self.frame

    def _on_change(self):
        """Handle the change in the entry value."""
        value = self.variable.get() if self.variable else self.value_entry.get()
        checked_value = self._check_value(value)
        if checked_value is not None:
            self.value = checked_value
            self.value_entry.configure(bg_color="transparent")
            if self._queue:
                self._queue.put(SettingEvent(self.name, self.value))
        else:
            self.value_entry.configure(bg_color="red")


class BoolSettingSkeleton(BasicSettingSkeleton):
    """A skeleton implementation of a boolean setting."""

    def __init__(self, name: str, default_value: bool = False, *args, **kwargs):
        super().__init__(name=name, default_value=default_value, *args, **kwargs)
        self.value = default_value

    def _check_value(self, value: Any) -> bool:
        """Check if the value is a boolean."""
        return bool(value)

    def _get_value_object(self) -> tuple[None, ctk.CTkSwitch]:
        """Create a switch for the boolean setting."""
        return None, ctk.CTkSwitch(
            self.frame,
            text="Enable",
            variable=ctk.IntVar(value=int(self.value)),
        )


class IntSliderSettingSkeleton(BasicSettingSkeleton):
    """A skeleton implementation of an integer slider setting."""

    def __init__(
        self,
        name: str,
        default_value: int = 0,
        min_value: int = 0,
        max_value: int = 100,
        *args,
        **kwargs,
    ):
        super().__init__(
            name=name,
            default_value=default_value,
            min_value=min_value,
            max_value=max_value,
            *args,
            **kwargs,
        )
        self.value = default_value

    def _check_value(self, value: Any) -> int:
        """Check if the value is an integer."""
        return int(value)

    def _get_value_object(self) -> tuple[ctk.Variable, ctk.CTkSlider]:
        """Create a slider for the integer setting."""
        self.variable = ctk.IntVar(value=self.value)
        self.combi_frame = ctk.CTkFrame(self.frame)
        self.combi_slider = ctk.CTkSlider(
            self.combi_frame,
            variable=self.variable,
            from_=self.min_value,
            to=self.max_value,
            number_of_steps=(self.max_value - self.min_value),
        )
        self.combi_slider.pack(side="left", padx=10, pady=10)
        self.combi_label = ctk.CTkLabel(
            self.combi_frame,
            textvariable=self.variable,
            font=("Arial", 16, "bold"),
        )
        self.combi_label.pack(side="right", padx=10, pady=10)

        return (self.variable, self.combi_frame)


class StringSettingSkeleton(BasicSettingSkeleton):
    """A skeleton implementation of a string setting."""

    def __init__(self, name: str, default_value: str = "", *args, **kwargs):
        super().__init__(name=name, default_value=default_value, *args, **kwargs)
        self.value = default_value

    def _check_value(self, value: Any) -> str:
        """Check if the value is a string."""
        if isinstance(value, str):
            if value == "":
                return None
            return value
        raise ValueError(f"Expected string for setting '{self.name}', got {value}")

    def _get_value_object(self) -> tuple[ctk.Variable, ctk.CTkEntry]:
        """Create an entry for the string setting."""
        self.variable = ctk.StringVar(value=self.value)
        return self.variable, ctk.CTkEntry(self.frame, textvariable=self.variable)
