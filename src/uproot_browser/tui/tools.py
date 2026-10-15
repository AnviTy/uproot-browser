from __future__ import annotations

__lazy_modules__ = {"importlib", "importlib.metadata", "textual.app"}

import importlib.metadata

import textual.app
import textual.containers
import textual.widgets

from .. import __version__


class Tools(textual.containers.Container):
    def compose(self) -> textual.app.ComposeResult:
        with textual.widgets.Collapsible(title="Theme", collapsed=False):
            themes = self.app.available_themes
            yield textual.widgets.Select(
                [(t, t) for t in themes],
                allow_blank=False,
                value=self.app.theme,
                id="theme-select",
            )

    def on_mount(self) -> None:
        # Keep the Select in sync with the app theme. init=True syncs the value
        # immediately, so this also catches a theme set before this lazy widget
        # mounted — no race between mounting and tracking.
        self.watch(self.app, "theme", self._sync_theme)

    def _sync_theme(self, theme: str) -> None:
        self.query_one("#theme-select", textual.widgets.Select).value = theme

    @textual.on(textual.widgets.Select.Changed, "#theme-select")
    def theme_changed(self, event: textual.widgets.Select.Changed) -> None:
        # pylint: disable-next=attribute-defined-outside-init
        self.app.theme = str(event.value)


class Info(textual.containers.Container):
    def compose(self) -> textual.app.ComposeResult:
        with textual.widgets.Collapsible(title="uproot-browser", collapsed=False):
            yield textual.widgets.Static(f"Version: [green]{__version__}[/green]")
        with textual.widgets.Collapsible(title="Packages", collapsed=False):
            for dist in importlib.metadata.distributions():
                yield textual.widgets.Static(
                    f"{dist.metadata['Name']} == [green]{dist.version}[/green]"
                )
