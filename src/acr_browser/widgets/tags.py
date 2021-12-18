from __future__ import annotations

from rich.console import RenderableType
from rich.panel import Panel
from rich.style import Style
from textual import events
from textual.keys import Keys
from textual.reactive import Reactive, watch
from textual.widget import Widget

from .. import styles
from ..azure import ArtifactTagProperties, ContainerRegistry
from ..renderables import TagsTableRenderable


class TagsWidget(Widget):
    """A tags widget. Used to display tags in a repository."""

    has_focus: Reactive[bool] = Reactive(False)

    page: int = 1
    row: int = 0

    def __init__(self) -> None:
        """A tags widget. Used to display tags in a repository."""

        name = self.__class__.__name__
        super().__init__(name=name)
        self.tags: list[ArtifactTagProperties] = []
        self.tag_map: dict[str, ArtifactTagProperties] = {}
        self.renderable: TagsTableRenderable | None = None
        self.reveal: bool
        self.client: ContainerRegistry = self.app.client

    def on_focus(self) -> None:
        """Sets has_focus to true when the item is clicked."""

        self.has_focus = True

    def on_blur(self) -> None:
        """Sets has_focus to false when an item no longer has focus."""

        self.has_focus = False

    async def on_mount(self) -> None:
        """Actions that are executed when the widget is mounted."""

        watch(self.app, "selected_repo", self.update)

    async def clear(self) -> None:
        """Clears the widget."""

        self.tags = []
        self.renderable = None
        self.refresh(layout=True)

    async def update(self, repository_name: str) -> None:
        """Updates the widget with new info.

        Args:
            repository_name (str): The repository name.
        """

        if repository_name:
            self.tags = await self.client.get_tags(repository_name)
            self.tag_map = {t.name: t for t in self.tags}
            await self.app.set_focus(self)

        self.refresh(layout=True)

    def on_key(self, event: events.Key) -> None:
        """Handle a key press.

        Args:
            event (events.Key): The event containing the pressed key.
        """

        if self.renderable is None or len(self.tags) == 0:
            return

        key = event.key
        if key == Keys.Enter:
            row = self.renderable.get_cell_value(0, self.row)
            self.app.selected_tag = self.tag_map[str(row)]

        elif key == Keys.Left:
            self.renderable.previous_page()
        elif key == Keys.Right:
            self.renderable.next_page()
        elif key == "f":
            self.renderable.first_page()
        elif key == "l":
            self.renderable.last_page()
        elif key == Keys.Up:
            self.renderable.previous_row()
        elif key == Keys.Down:
            self.renderable.next_row()

        self.refresh(layout=True)

    def render_table(self) -> None:
        """Render the table."""

        self.renderable = TagsTableRenderable(
            items=self.tags or [],
            title="🏷️  tags",
            page_size=self.size.height - 5,
            page=self.page,
            row=self.row,
        )

    def render(self) -> RenderableType:
        """Render the widget.

        Returns:
            RenderableType: Object to be rendered
        """

        if self.renderable is not None:
            self.page = self.renderable.page
            self.row = self.renderable.row

        self.render_table()
        assert isinstance(self.renderable, TagsTableRenderable)
        return Panel(
            renderable=self.renderable,
            title=f"[{styles.GREY}]( {self.renderable.title} )[/]",
            border_style=Style(
                color=styles.LIGHT_PURPLE if self.has_focus else styles.PURPLE
            ),
            expand=True,
            box=styles.BOX,
        )
