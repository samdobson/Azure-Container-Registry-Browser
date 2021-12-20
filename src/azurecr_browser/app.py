from __future__ import annotations

import asyncio
from itertools import cycle
from typing import Any, MutableMapping

import aiodocker
import click
from azure.containerregistry import RepositoryProperties
from click import Path
from textual.app import App
from textual.keys import Keys
from textual.reactive import Reactive
from textual.widget import Widget

from . import __version__
from .azure import ContainerRegistry
from .config import CLI_HELP, get_config
from .widgets import (
    FlashWidget,
    HeaderWidget,
    HelpWidget,
    RepositoriesWidget,
    SearchWidget,
    ShowFlashNotification,
    TagPropertiesWidget,
    TagsWidget,
)
from .widgets.flash import FlashMessageType


class ACRBrowser(App):

    config_path: str | None = None
    config: MutableMapping[str, Any]
    client: ContainerRegistry
    docker: aiodocker.Docker | None = None
    show_help: Reactive[bool] = Reactive(False)
    selected_tag: Reactive[RepositoryProperties] = Reactive(None)
    selected_repo: Reactive[str] = Reactive("")
    searchable_nodes: Reactive[list[RepositoryProperties]] = Reactive([])
    search_result: Reactive[list[str]] = Reactive([])
    widget_list: cycle[Widget] = cycle([])

    async def on_load(self) -> None:
        """Overrides on_load from App()"""

        self.log("Starting app")
        self.config = get_config(self.config_path)
        self.acr_name = self.config["registry"]
        self.log(f"Registry name: {self.acr_name}")
        self.client = ContainerRegistry(self.acr_name)

        try:
            self.docker = aiodocker.Docker()
        except aiodocker.exceptions.DockerError:
            pass

        await self.bind("h", "toggle_help", "help")
        await self.bind("ctrl+i", "cycle_widget", show=False)
        await self.bind(Keys.Escape, "refocus", show=False)
        await self.bind("/", "select_search", "search")
        await self.bind("q", "quit", "quit")
        if self.docker:
            await self.bind("p", "pull_image", "pull")

    async def on_mount(self) -> None:
        """Overrides on_mount from App()"""

        await self.view.dock(HeaderWidget(), size=7)

        self.search = SearchWidget()
        await self.view.dock(self.search, size=3)

        grid = await self.view.dock_grid()
        grid.add_column(name="repositories")
        grid.add_column(name="tags")
        grid.add_column(name="properties")
        grid.add_row(name="content")

        self.repositories = RepositoriesWidget()
        grid.place(self.repositories)

        self.tags = TagsWidget()
        grid.place(self.tags)

        self.properties = TagPropertiesWidget()
        grid.place(self.properties)

        self.flash = FlashWidget()
        await self.view.dock(self.flash, edge="bottom", z=1)

        self.help = HelpWidget()
        await self.view.dock(self.help, z=1)

        self.widget_list = cycle(
            [self.search, self.repositories, self.tags, self.properties]
        )

        await self.app.set_focus(self.repositories)

    async def watch_show_help(self, show_help: bool) -> None:
        """Watch show_help and update widget visibility.

        Args:
            show_help (bool): Widget is shown if True and not shown if False.
        """
        self.help.visible = show_help

        if self.show_help:
            await self.app.set_focus(self.help)

        self.refresh(layout=True)

    async def action_toggle_help(self) -> None:
        """Toggle the help widget."""

        self.show_help = not self.show_help

    async def run_cmd(self, cmd) -> None:
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        self.log(f"[{cmd!r} exited with {proc.returncode}]")
        if stdout:
            self.log(f"[stdout]\n{stdout.decode()}")
        if stderr:
            self.log(f"[stderr]\n{stderr.decode()}")

    async def action_pull_image(self) -> None:
        """Pull an image with docker."""
        if not self.docker:
            self.log("Docker is not available")
            return
        if not self.selected_repo and not self.selected_tag:
            self.log("No tag selected")
            return
        image = f"{self.selected_repo}:{self.selected_tag.name}"

        await self.handle_show_flash_notification(
            ShowFlashNotification(
                self,
                type=FlashMessageType.INFO,
                value="Image pull started...",
            )
        )

        self.log("Logging in to ACR")
        await self.run_cmd(f"az acr login -n {self.acr_name}")
        self.log(f"Pulling image: {image}")
        await self.run_cmd(f"docker pull {self.acr_name}.azurecr.io/{image}")

    async def action_select_search(self) -> None:
        """Focus on the search widget."""

        await self.app.set_focus(self.search)

    async def handle_show_flash_notification(
        self, message: ShowFlashNotification
    ) -> None:
        """Handle a ShowFlashNotification message.

        Args:
            message (ShowFlashNotification): The message to handle.
        """

        self.log("Handling ShowFlashNotification message")
        await self.flash.update_flash_message(value=message.value, type=message.type)

    async def action_cycle_widget(self) -> None:
        """Cycle through the widgets."""

        current_widget = next(self.widget_list)

        if current_widget.has_focus:
            current_widget = next(self.widget_list)

        await self.set_focus(current_widget)
        self.refresh(layout=True)

    async def action_refocus(self) -> None:
        """Refocus the app."""

        if self.search.has_focus:
            await self.tags.clear()
            await self.properties.clear()
            await self.search.clear()
        else:
            await self.set_focus(self.repositories)
            self.show_help = False


@click.command(help=CLI_HELP)
@click.option(
    "--config",
    default=None,
    envvar="ACR_BROWSER_CONFIG",
    type=Path(file_okay=True, dir_okay=False, exists=False, resolve_path=True),
    help="Explicitly override the config that will be used by azurecr-browser.",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode.",
)
@click.version_option(__version__)
def run(config: str | None, debug: bool) -> None:
    """The entry point.

    Args:
        config (str | None): The config file to use.
        debug (bool): Enable debug mode.
    """

    title = "ACR Browser"
    app = ACRBrowser
    app.config_path = config
    if debug:
        app.run(log="azurecr-browser.log", title=title)
    else:
        app.run()
