"""
Base scene class that applies a centralized theme.

Usage:
    from themed_scene import ThemedScene

    class MyScene(ThemedScene):
        # optional: override the default theme
        theme_name = "dark_slate"

        def construct(self):
            # self.theme is available — a Theme dataclass instance
            title = Text("Hello", font_size=self.theme.title_size,
                         color=self.theme.foreground)
            graph = axes.plot(f, color=self.theme.primary)
            ...

Theme resolution (first wins):
    1. ``theme_name`` class variable on the scene
    2. ``MANIMO_THEME`` environment variable
    3. Falls back to "classic"

For scenes that need LinearTransformationScene or ThreeDScene as the base,
use ThemedMixin and apply it via multiple inheritance:

    class MyScene(ThemedMixin, LinearTransformationScene):
        ...
"""

from manim import Scene

from theme import Theme, get_theme


class ThemedMixin:
    """Mixin that adds theme support to any Manim scene base class.

    Call ``self.apply_theme()`` at the start of ``construct()`` or override
    ``setup()`` to call it automatically.
    """

    theme_name: str | None = None

    def apply_theme(self) -> None:
        """Load and apply the theme. Sets ``self.theme`` and background color."""
        self.theme: Theme = get_theme(self.theme_name)
        self.camera.background_color = self.theme.background

    def setup(self) -> None:
        super().setup()
        self.apply_theme()


class ThemedScene(ThemedMixin, Scene):
    """Drop-in replacement for ``Scene`` with automatic theme support.

    ``self.theme`` is available inside ``construct()`` and contains all
    visual tokens (colors, font sizes, stroke widths, opacities).
    """
