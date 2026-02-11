#!/usr/bin/env python3
"""
Command-line interface for rendering Manim visualizations.

Usage:
    python render.py <category> <scene_name> [--quality l|m|h] [--theme NAME]
    python render.py --list  # List all available scenes
    python render.py --themes  # List available themes

Examples:
    python render.py linear BasisVectorTransformation
    python render.py calculus TangentLineDerivative --quality m
    python render.py pythag BhaskaraProof --theme light
    python render.py landing DerivativeDemo --theme dark_slate
"""

import os
import subprocess
import sys
from pathlib import Path

from theme import THEMES, DEFAULT_THEME

SCENES = {
    "linear": {
        "module": "linear_transformations",
        "scenes": [
            "LinearTransformationIntro",
            "BasisVectorTransformation",
            "MatrixMultiplicationAsComposition",
            "DotProductInterpretation",
            "ShearTransformation",
            "RotationTransformation",
            "AllTransformations",
        ],
    },
    "calculus": {
        "module": "calculus_visualizations",
        "scenes": [
            "FunctionPlotAnimation",
            "TangentLineDerivative",
            "SecantToTangent",
            "RiemannSumsToIntegral",
            "DerivativeIntegralRelation",
            "AreaAccumulation",
            "PowerRuleDerivative",
        ],
    },
    "pythag": {
        "module": "pythagorean_proofs",
        "scenes": [
            "PythagoreanIntro",
            "BhaskaraProof",
            "RearrangementProof",
            "AreaBasedProof",
            "EuclideanProof",
            "PresidentialProof",
            "AnimatedProofSummary",
        ],
    },
    "proof": {
        "module": "pythagorean_proof",
        "scenes": [
            "PythagoreanProof",
        ],
    },
    "waves": {
        "module": "wave_and_field_visualizations",
        "scenes": [
            "SineWaveGeneration",
            "WaveInterference",
            "VectorFieldVisualization",
            "ComplexMultiplication",
            "FourierSeriesSquareWave",
            "PendulumMotion",
        ],
    },
    "demo": {
        "module": "demo_no_latex",
        "scenes": [
            "TangentLineDemo",
            "AreaUnderCurveDemo",
            "CircleAreaDemo",
        ],
    },
    "landing": {
        "module": "landing_demo",
        "scenes": [
            "DerivativeDemo",
        ],
    },
    "test": {
        "module": "test_scene",
        "scenes": [
            "SimpleTransformTest",
            "PythagoreanShapesTest",
            "DerivativeShapesTest",
        ],
    },
}


def list_scenes():
    """Print all available scenes."""
    print("\nAvailable Manim Visualizations\n")
    print("=" * 50)

    for category, info in SCENES.items():
        print(f"\n  {category} ({info['module']}.py)")
        print("-" * 40)
        for scene in info["scenes"]:
            print(f"    - {scene}")

    print("\n" + "=" * 50)
    print("\nUsage: python render.py <category> <scene_name>")
    print("       python render.py linear BasisVectorTransformation")
    print("       python render.py --all linear  # Render all scenes in category")


def list_themes():
    """Print available themes."""
    print("\nAvailable Themes\n")
    print("=" * 50)
    for name, theme in THEMES.items():
        marker = " (default)" if name == DEFAULT_THEME else ""
        print(f"\n  {name}{marker}")
        print(f"    background: {theme.background}")
        print(f"    primary:    {theme.primary}")
        print(f"    secondary:  {theme.secondary}")
        print(f"    tertiary:   {theme.tertiary}")
        print(f"    accent:     {theme.accent}")
    print("\n" + "=" * 50)
    print("\nUsage: python render.py <category> <scene> --theme <name>")


def render_scene(category: str, scene_name: str, quality: str = "l", theme: str | None = None):
    """Render a single scene."""
    if category not in SCENES:
        print(f"Unknown category: {category}")
        print(f"   Available: {', '.join(SCENES.keys())}")
        sys.exit(1)

    info = SCENES[category]
    module = info["module"]

    if scene_name not in info["scenes"]:
        print(f"Unknown scene: {scene_name}")
        print(f"   Available in {category}:")
        for s in info["scenes"]:
            print(f"      - {s}")
        sys.exit(1)

    quality_flags = {"l": "-ql", "m": "-qm", "h": "-qh"}
    quality_names = {"l": "480p", "m": "720p", "h": "1080p"}

    theme_display = f" [{theme}]" if theme else ""
    print(f"\nRendering {scene_name} at {quality_names.get(quality, '480p')}{theme_display}...")
    print(f"   Module: {module}.py\n")

    env = os.environ.copy()
    if theme:
        env["MANIMO_THEME"] = theme

    cmd = [
        "manim",
        quality_flags.get(quality, "-ql"),
        "-p",  # Preview when done
        f"{module}.py",
        scene_name,
    ]

    script_dir = Path(__file__).parent
    result = subprocess.run(cmd, cwd=script_dir, env=env)

    if result.returncode == 0:
        print(f"\nSuccessfully rendered {scene_name}")
    else:
        print(f"\nFailed to render {scene_name}")
        sys.exit(1)


def render_all(category: str, quality: str = "l", theme: str | None = None):
    """Render all scenes in a category."""
    if category not in SCENES:
        print(f"Unknown category: {category}")
        sys.exit(1)

    info = SCENES[category]
    module = info["module"]

    quality_flags = {"l": "-ql", "m": "-qm", "h": "-qh"}

    theme_display = f" [{theme}]" if theme else ""
    print(f"\nRendering all scenes in {category}{theme_display}...")

    env = os.environ.copy()
    if theme:
        env["MANIMO_THEME"] = theme

    cmd = [
        "manim",
        quality_flags.get(quality, "-ql"),
        "-a",  # All scenes
        f"{module}.py",
    ]

    script_dir = Path(__file__).parent
    result = subprocess.run(cmd, cwd=script_dir, env=env)

    if result.returncode == 0:
        print(f"\nSuccessfully rendered all {category} scenes")
    else:
        print(f"\nSome scenes failed to render")
        sys.exit(1)


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        list_scenes()
        sys.exit(0)

    if args[0] == "--list":
        list_scenes()
        sys.exit(0)

    if args[0] == "--themes":
        list_themes()
        sys.exit(0)

    # Parse quality flag
    quality = "l"
    if "--quality" in args:
        idx = args.index("--quality")
        if idx + 1 < len(args):
            quality = args[idx + 1]
            args = args[:idx] + args[idx + 2:]

    # Parse theme flag
    theme = None
    if "--theme" in args:
        idx = args.index("--theme")
        if idx + 1 < len(args):
            theme = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
            # Validate theme name
            if theme.lower() not in THEMES:
                print(f"Unknown theme: {theme}")
                print(f"   Available: {', '.join(sorted(THEMES))}")
                sys.exit(1)

    if args[0] == "--all":
        if len(args) < 2:
            print("Please specify a category: --all <category>")
            sys.exit(1)
        render_all(args[1], quality, theme)
    elif len(args) >= 2:
        render_scene(args[0], args[1], quality, theme)
    else:
        print("Please specify both category and scene name")
        print("   Usage: python render.py <category> <scene_name>")
        list_scenes()
        sys.exit(1)


if __name__ == "__main__":
    main()
