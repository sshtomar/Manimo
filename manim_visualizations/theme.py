"""
Centralized theme system for Manim visualizations.

Provides semantic color roles, font sizes, stroke widths, and fill opacities
so that visual styling is defined once and applied consistently across all scenes.

Usage:
    from theme import THEMES, get_theme

    theme = get_theme()           # reads MANIMO_THEME env var, defaults to "classic"
    theme = get_theme("light")    # explicit theme name

Themes can also be selected at render time:
    python render.py calculus FunctionPlotAnimation --theme dark_slate
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Theme:
    """All visual tokens for a Manim scene.

    Colors are hex strings (e.g. "#58C4DD") accepted by all Manim color params.
    """

    name: str

    # --- scene colors ---
    background: str
    foreground: str          # primary text, axis lines
    muted: str               # grid lines, secondary text

    # --- semantic math colors ---
    primary: str             # main entity (functions, key shapes)
    secondary: str           # contrasting entity (derivatives, second concept)
    tertiary: str            # third entity (integrals, additional)
    accent: str              # highlights, emphasis, key results
    accent2: str             # alternative accent

    # --- font sizes ---
    title_size: int = 44
    subtitle_size: int = 36
    body_size: int = 28
    label_size: int = 24
    small_size: int = 20

    # --- stroke widths ---
    axis_stroke_width: float = 2.0
    curve_stroke_width: float = 3.0
    heavy_stroke_width: float = 5.0
    fine_stroke_width: float = 1.0

    # --- fill opacities ---
    shape_fill_opacity: float = 0.3
    area_fill_opacity: float = 0.5
    subtle_fill_opacity: float = 0.15

    # --- extra palette (domain-specific overrides) ---
    extras: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Preset themes
# ---------------------------------------------------------------------------

CLASSIC = Theme(
    name="classic",
    # Manim CE default dark background with 3b1b-inspired palette
    background="#000000",
    foreground="#FFFFFF",
    muted="#888888",
    primary="#58C4DD",      # BLUE
    secondary="#FC6255",    # RED
    tertiary="#83C167",     # GREEN
    accent="#FFFF00",       # YELLOW
    accent2="#FF862F",      # ORANGE
)

DARK_SLATE = Theme(
    name="dark_slate",
    # Tailwind slate palette — polished dark UI feel
    background="#0f172a",   # slate-900
    foreground="#e2e8f0",   # slate-200
    muted="#475569",        # slate-600
    primary="#3b82f6",      # blue-500
    secondary="#ef4444",    # red-500
    tertiary="#22c55e",     # green-500
    accent="#f59e0b",       # amber-500
    accent2="#a855f7",      # purple-500
    extras={
        "axis_color": "#475569",
        "label_color": "#94a3b8",   # slate-400
    },
)

LIGHT = Theme(
    name="light",
    # Light background for presentations and print
    background="#FFFFFF",
    foreground="#1e293b",   # slate-800
    muted="#94a3b8",        # slate-400
    primary="#2563eb",      # blue-600
    secondary="#dc2626",    # red-600
    tertiary="#16a34a",     # green-600
    accent="#d97706",       # amber-600
    accent2="#7c3aed",      # violet-600
)

WARM = Theme(
    name="warm",
    # Warm, inviting deep-purple tone
    background="#1a0a2e",
    foreground="#fef3c7",   # amber-100
    muted="#78716c",        # stone-500
    primary="#f59e0b",      # amber-500
    secondary="#ec4899",    # pink-500
    tertiary="#06b6d4",     # cyan-500
    accent="#f97316",       # orange-500
    accent2="#a78bfa",      # violet-400
)

# ---------------------------------------------------------------------------
# Educator themes
# ---------------------------------------------------------------------------

CHALKBOARD = Theme(
    name="chalkboard",
    # Classroom chalkboard with chalk-pastel colors
    background="#2a3a2a",
    foreground="#e8e0d0",   # warm chalk white
    muted="#6b7b6b",        # dusty chalk
    primary="#7eb8da",      # blue chalk
    secondary="#e8a0a0",    # pink chalk
    tertiary="#d4c878",     # yellow chalk
    accent="#e8b060",       # orange chalk
    accent2="#78c8a0",      # mint chalk
    title_size=46,
    subtitle_size=38,
    body_size=30,
    label_size=26,
    small_size=22,
    axis_stroke_width=2.5,
    curve_stroke_width=4.0,
    heavy_stroke_width=6.0,
    fine_stroke_width=1.5,
    shape_fill_opacity=0.2,
    area_fill_opacity=0.35,
    subtle_fill_opacity=0.1,
)

WHITEBOARD = Theme(
    name="whiteboard",
    # Clean marker-on-whiteboard, high-saturation dry-erase colors
    background="#f8f6f0",
    foreground="#1a1a2e",   # near-black
    muted="#b0aaa0",        # light gray
    primary="#1a73e8",      # blue marker
    secondary="#d93025",    # red marker
    tertiary="#188038",     # green marker
    accent="#e8710a",       # orange marker
    accent2="#8430ce",      # purple marker
    curve_stroke_width=3.5,
    heavy_stroke_width=5.5,
)

HIGH_CONTRAST = Theme(
    name="high_contrast",
    # WCAG AA+, color-blind safe (blue/orange primary pair)
    background="#000000",
    foreground="#ffffff",
    muted="#999999",
    primary="#4da6ff",      # bright blue
    secondary="#ff9933",    # bright orange (not red — CB-safe)
    tertiary="#33cccc",     # cyan
    accent="#ffdd00",       # yellow
    accent2="#ff66cc",      # magenta
    title_size=48,
    subtitle_size=40,
    body_size=32,
    label_size=28,
    small_size=24,
    axis_stroke_width=2.5,
    curve_stroke_width=4.0,
    heavy_stroke_width=7.0,
    fine_stroke_width=1.5,
)

LECTURE_HALL = Theme(
    name="lecture_hall",
    # Projector-optimized, high saturation, extra-large text
    background="#0a0e1a",
    foreground="#f5f0e0",   # bright cream
    muted="#4a5568",        # steel blue
    primary="#38bdf8",      # vivid sky blue
    secondary="#fb7185",    # coral
    tertiary="#a3e635",     # lime (more visible on projectors than green)
    accent="#fbbf24",       # gold
    accent2="#c4b5fd",      # lavender
    title_size=50,
    subtitle_size=42,
    body_size=34,
    label_size=30,
    small_size=26,
    axis_stroke_width=2.5,
    curve_stroke_width=4.5,
    heavy_stroke_width=7.0,
    fine_stroke_width=1.5,
)

PASTEL = Theme(
    name="pastel",
    # Soft Catppuccin Mocha-inspired, low fatigue for long sessions
    background="#1e1e2e",
    foreground="#cdd6f4",   # lavender white
    muted="#585b70",        # overlay
    primary="#89b4fa",      # blue
    secondary="#fab387",    # peach
    tertiary="#a6e3a1",     # green
    accent="#cba6f7",       # mauve
    accent2="#f5c2e7",      # pink
    shape_fill_opacity=0.35,
)

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

THEMES: dict[str, Theme] = {
    "classic": CLASSIC,
    "dark_slate": DARK_SLATE,
    "light": LIGHT,
    "warm": WARM,
    "chalkboard": CHALKBOARD,
    "whiteboard": WHITEBOARD,
    "high_contrast": HIGH_CONTRAST,
    "lecture_hall": LECTURE_HALL,
    "pastel": PASTEL,
}

DEFAULT_THEME = "classic"


def get_theme(name: str | None = None) -> Theme:
    """Return a theme by name.

    Resolution order:
        1. Explicit ``name`` argument
        2. ``MANIMO_THEME`` environment variable
        3. Falls back to ``DEFAULT_THEME``

    Raises ``KeyError`` if the name doesn't match a registered theme.
    """
    resolved = name or os.environ.get("MANIMO_THEME") or DEFAULT_THEME
    resolved = resolved.lower().strip()
    if resolved not in THEMES:
        available = ", ".join(sorted(THEMES))
        raise KeyError(
            f"Unknown theme {resolved!r}. Available themes: {available}"
        )
    return THEMES[resolved]
