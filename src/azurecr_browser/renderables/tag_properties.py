from __future__ import annotations

from azure.containerregistry import ArtifactTagProperties
from rich.console import Console, ConsoleOptions, Group, RenderResult
from rich.table import Table

from .. import styles
from ..util import format_datetime

UP = "\u2191"
DOWN = "\u2193"
LEFT = "\u2190"
RIGHT = "\u2192"


class RepositoryPropertiesRenderable:
    """A repository properties renderable."""

    def __init__(self, properties: ArtifactTagProperties | None, value: str) -> None:
        self.title = f"{properties.name} @ {properties.digest}" if properties else ""
        self.properties = (
            {
                "tag": properties.name,
                "created on": format_datetime(properties.created_on),
                "updated on": format_datetime(properties.last_updated_on)
                if properties.last_updated_on
                else None,
            }
            if properties
            else None
        )
        self.value = value if value else ""

    def __str__(self) -> str:
        return str(self.properties)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        table = Table(box=None, expand=True, show_footer=False, show_header=False)
        table.add_column(style=styles.GREY, no_wrap=True)
        table.add_column(style=f"{styles.ORANGE} bold", no_wrap=True)

        if self.properties:

            # table.title = Text(self.title, no_wrap=True, style=styles.GREEN)
            table.title_justify = "left"
            table.add_row()
            for property, value in self.properties.items():
                table.add_row(property, str(value))

        yield Group(table, self.value)
