from __future__ import annotations

from rich.console import RenderableType
from rich.panel import Panel
from rich.style import Style
from textual import events
from textual.reactive import Reactive, watch
from textual.widget import Widget

from .. import styles
from ..azure import ArtifactTagProperties, ContainerRegistry
from ..renderables import RepositoryPropertiesRenderable


class TagPropertiesWidget(Widget):
    """A tag properties widget. Used to display tag properties."""

    has_focus: Reactive[bool] = Reactive(False)

    def __init__(self) -> None:
        """A tag properties widget. Used to display tag properties."""

        name = self.__class__.__name__
        super().__init__(name=name)
        self.selected_tag: ArtifactTagProperties | None = None
        self.renderable: RepositoryPropertiesRenderable | None = None
        self.value: str = ""
        self.client: ContainerRegistry = self.app.client

    async def on_mount(self) -> None:
        """Actions that are executed when the widget is mounted."""

        watch(self.app, "selected_tag", self.update)

    def on_focus(self) -> None:
        """Sets has_focus to true when the item is clicked."""

        self.has_focus = True

    def on_blur(self) -> None:
        """Sets has_focus to false when an item no longer has focus."""

        self.has_focus = False

    async def clear(self) -> None:
        """Clears the widget."""

        self.selected_tag = None
        self.renderable = None
        self.refresh(layout=True)

    async def update(self, selected_tag: ArtifactTagProperties) -> None:
        """Updates the widget with new tag properties.

        Args:
            selected_tag (ArtifactTagProperties): A tag properties object.
        """

        if selected_tag:
            self.selected_tag = selected_tag
            await self.app.set_focus(self)

        self.refresh(layout=True)

    def on_key(self, event: events.Key) -> None:
        """Handle a key press.

        Args:
            event (events.Key): The event containing the pressed key.
        """

        if self.renderable is None or self.selected_tag is None:
            return

        self.refresh(layout=True)

    def render_table(self) -> None:
        """Renders the table."""

        self.renderable = RepositoryPropertiesRenderable(
            properties=self.selected_tag,
            value="",
        )

    def render(self) -> RenderableType:
        """Render the widget.

        Returns:
            RenderableType: Object to be rendered
        """

        self.render_table()
        assert isinstance(self.renderable, RepositoryPropertiesRenderable)
        return Panel(
            renderable=self.renderable,
            title=f"[{styles.GREY}]( ℹ️ properties )[/]",
            border_style=Style(
                color=styles.LIGHT_PURPLE if self.has_focus else styles.PURPLE
            ),
            expand=True,
            box=styles.BOX,
        )
