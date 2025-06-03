import customtkinter as ctk
from app_frame import AppFrame
from help_content import HELP_SECTIONS
from settings_manager import SettingsManager

class HelpSection(ctk.CTkFrame):
    """A section that contains help information."""

    def __init__(self, title: str, content: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(border_width=1, corner_radius=1, fg_color="transparent")

        # Create a label to display the section title
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 16, "bold"),
            justify="left"
        )
        self.title_label.pack(padx=10, pady=5)
        # Create a label to display the help content
        self.help_label = ctk.CTkLabel(
            self,
            text=content,
            justify="left",
            wraplength=500
        )
        self.help_label.pack(padx=10, pady=5)


class HelpFrame(AppFrame):
    """A frame that displays help information."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(border_width=1, corner_radius=1, fg_color="transparent")

        self._help_sections: list[HelpSection] = []

        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            width=400,
            height=300,
            corner_radius=10,
            fg_color="transparent"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a label to display help information
        self.help_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="This is the help section. Here you can find information about how to use the application.",
            justify="left",
            wraplength=400
        )
        self.help_label.pack(padx=20, pady=20)

        self.build_sections()

    def build_sections(self):
        """Builds the help sections."""
        # Clear existing sections
        for section in self._help_sections:
            section.destroy()
        self._help_sections.clear()

        for section in HELP_SECTIONS:
            section = HelpSection(
                title=section["title"],
                content=section["text"],
                master=self.scrollable_frame
            )
            section.pack(fill="x", padx=10, pady=5)
            self._help_sections.append(section)