#!/usr/bin/env python3
"""
Command-line interface for rendering Manim visualizations.

Usage:
    python render.py <category> <scene_name> [--quality l|m|h]
    python render.py --list  # List all available scenes

Examples:
    python render.py linear BasisVectorTransformation
    python render.py calculus TangentLineDerivative --quality m
    python render.py pythag BhaskaraProof
"""

import subprocess
import sys
from pathlib import Path

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
}


def list_scenes():
    """Print all available scenes."""
    print("\n🎬 Available Manim Visualizations\n")
    print("=" * 50)

    for category, info in SCENES.items():
        print(f"\n📂 {category} ({info['module']}.py)")
        print("-" * 40)
        for scene in info["scenes"]:
            print(f"    • {scene}")

    print("\n" + "=" * 50)
    print("\nUsage: python render.py <category> <scene_name>")
    print("       python render.py linear BasisVectorTransformation")
    print("       python render.py --all linear  # Render all scenes in category")


def render_scene(category: str, scene_name: str, quality: str = "l"):
    """Render a single scene."""
    if category not in SCENES:
        print(f"❌ Unknown category: {category}")
        print(f"   Available: {', '.join(SCENES.keys())}")
        sys.exit(1)

    info = SCENES[category]
    module = info["module"]

    if scene_name not in info["scenes"]:
        print(f"❌ Unknown scene: {scene_name}")
        print(f"   Available in {category}:")
        for s in info["scenes"]:
            print(f"      • {s}")
        sys.exit(1)

    quality_flags = {"l": "-ql", "m": "-qm", "h": "-qh"}
    quality_names = {"l": "480p", "m": "720p", "h": "1080p"}

    print(f"\n🎬 Rendering {scene_name} at {quality_names.get(quality, '480p')}...")
    print(f"   Module: {module}.py\n")

    cmd = [
        "manim",
        quality_flags.get(quality, "-ql"),
        "-p",  # Preview when done
        f"{module}.py",
        scene_name,
    ]

    script_dir = Path(__file__).parent
    result = subprocess.run(cmd, cwd=script_dir)

    if result.returncode == 0:
        print(f"\n✅ Successfully rendered {scene_name}")
    else:
        print(f"\n❌ Failed to render {scene_name}")
        sys.exit(1)


def render_all(category: str, quality: str = "l"):
    """Render all scenes in a category."""
    if category not in SCENES:
        print(f"❌ Unknown category: {category}")
        sys.exit(1)

    info = SCENES[category]
    module = info["module"]

    quality_flags = {"l": "-ql", "m": "-qm", "h": "-qh"}

    print(f"\n🎬 Rendering all scenes in {category}...")

    cmd = [
        "manim",
        quality_flags.get(quality, "-ql"),
        "-a",  # All scenes
        f"{module}.py",
    ]

    script_dir = Path(__file__).parent
    result = subprocess.run(cmd, cwd=script_dir)

    if result.returncode == 0:
        print(f"\n✅ Successfully rendered all {category} scenes")
    else:
        print(f"\n❌ Some scenes failed to render")
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

    # Parse quality flag
    quality = "l"
    if "--quality" in args:
        idx = args.index("--quality")
        if idx + 1 < len(args):
            quality = args[idx + 1]
            args = args[:idx] + args[idx + 2 :]

    if args[0] == "--all":
        if len(args) < 2:
            print("❌ Please specify a category: --all <category>")
            sys.exit(1)
        render_all(args[1], quality)
    elif len(args) >= 2:
        render_scene(args[0], args[1], quality)
    else:
        print("❌ Please specify both category and scene name")
        print("   Usage: python render.py <category> <scene_name>")
        list_scenes()
        sys.exit(1)


if __name__ == "__main__":
    main()
