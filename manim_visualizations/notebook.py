"""
Manim Visualizations - Interactive Marimo Notebook
Run visualizations for Linear Algebra, Calculus, and Pythagorean Theorem
"""

import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # 🎬 Manim Mathematical Visualizations

        This notebook provides an interactive interface to render beautiful mathematical animations
        using Manim (Mathematical Animation Engine), inspired by 3Blue1Brown's visual style.

        ## Categories

        1. **Linear Transformations** - Matrix multiplication, basis vectors, transformations
        2. **Calculus** - Functions, derivatives, integrals, Riemann sums
        3. **Pythagorean Theorem** - Multiple visual proofs
        """
    )
    return


@app.cell
def _():
    import subprocess
    import os
    from pathlib import Path

    # Get the directory where this notebook is located
    NOTEBOOK_DIR = Path(__file__).parent if "__file__" in dir() else Path.cwd()
    MEDIA_DIR = NOTEBOOK_DIR / "media"

    def run_manim_scene(module_name: str, scene_name: str, quality: str = "l"):
        """
        Run a Manim scene and return the path to the generated video.

        Args:
            module_name: Name of the Python module (without .py)
            scene_name: Name of the Scene class to render
            quality: Quality level - 'l' (low/480p), 'm' (medium/720p), 'h' (high/1080p)
        """
        quality_flags = {
            "l": "-ql",  # 480p, 15fps
            "m": "-qm",  # 720p, 30fps
            "h": "-qh",  # 1080p, 60fps
        }

        cmd = [
            "uv", "run", "manim",
            quality_flags.get(quality, "-ql"),
            f"{module_name}.py",
            scene_name,
        ]

        result = subprocess.run(
            cmd,
            cwd=str(NOTEBOOK_DIR),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return None, f"Error: {result.stderr}"

        # Find the generated video
        quality_dirs = {"l": "480p15", "m": "720p30", "h": "1080p60"}
        video_dir = MEDIA_DIR / "videos" / module_name / quality_dirs.get(quality, "480p15")

        if video_dir.exists():
            videos = list(video_dir.glob("*.mp4"))
            if videos:
                # Return the most recent video
                latest = max(videos, key=lambda p: p.stat().st_mtime)
                return str(latest), None

        return None, "Video not found after rendering"

    return MEDIA_DIR, NOTEBOOK_DIR, Path, os, run_manim_scene, subprocess


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 🔷 1. Linear Transformations

        Visualize how matrices transform 2D space, following the intuition from
        3Blue1Brown's "Essence of Linear Algebra" series.
        """
    )
    return


@app.cell
def _(mo):
    linear_scenes = mo.ui.dropdown(
        options={
            "LinearTransformationIntro": "Introduction to Linear Transformations",
            "BasisVectorTransformation": "Basis Vectors & Matrix Columns",
            "MatrixMultiplicationAsComposition": "Matrix Multiplication as Composition",
            "DotProductInterpretation": "Dot Product Interpretation",
            "ShearTransformation": "Shear Transformation",
            "RotationTransformation": "45° Rotation",
            "AllTransformations": "Gallery of Transformations",
        },
        value="LinearTransformationIntro",
        label="Select Scene:",
    )
    linear_scenes
    return (linear_scenes,)


@app.cell
def _(linear_scenes, mo):
    linear_render_btn = mo.ui.button(
        label=f"🎬 Render: {linear_scenes.value}",
        kind="success",
    )
    linear_render_btn
    return (linear_render_btn,)


@app.cell
def _(linear_render_btn, linear_scenes, mo, run_manim_scene):
    linear_output = None
    if linear_render_btn.value:
        mo.output.append(mo.md("⏳ Rendering animation... this may take a moment."))
        video_path, error = run_manim_scene("linear_transformations", linear_scenes.value)
        if error:
            linear_output = mo.md(f"❌ {error}")
        elif video_path:
            linear_output = mo.video(src=video_path)
        else:
            linear_output = mo.md("❌ Could not find rendered video")
    linear_output
    return (linear_output,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 📈 2. Calculus Visualizations

        See derivatives come alive as tangent lines, watch functions get plotted,
        and observe Riemann sums converge to definite integrals.
        """
    )
    return


@app.cell
def _(mo):
    calculus_scenes = mo.ui.dropdown(
        options={
            "FunctionPlotAnimation": "Animated Function Plotting",
            "TangentLineDerivative": "Tangent Lines & Derivatives",
            "SecantToTangent": "Secant Lines → Tangent (Limit Definition)",
            "RiemannSumsToIntegral": "Riemann Sums → Integral",
            "DerivativeIntegralRelation": "Fundamental Theorem of Calculus",
            "AreaAccumulation": "Integral as Accumulated Area",
            "PowerRuleDerivative": "Power Rule Visualization",
        },
        value="TangentLineDerivative",
        label="Select Scene:",
    )
    calculus_scenes
    return (calculus_scenes,)


@app.cell
def _(calculus_scenes, mo):
    calculus_render_btn = mo.ui.button(
        label=f"🎬 Render: {calculus_scenes.value}",
        kind="success",
    )
    calculus_render_btn
    return (calculus_render_btn,)


@app.cell
def _(calculus_render_btn, calculus_scenes, mo, run_manim_scene):
    calculus_output = None
    if calculus_render_btn.value:
        mo.output.append(mo.md("⏳ Rendering animation... this may take a moment."))
        video_path, error = run_manim_scene("calculus_visualizations", calculus_scenes.value)
        if error:
            calculus_output = mo.md(f"❌ {error}")
        elif video_path:
            calculus_output = mo.video(src=video_path)
        else:
            calculus_output = mo.md("❌ Could not find rendered video")
    calculus_output
    return (calculus_output,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 🔷 3. Pythagorean Theorem Visual Proofs

        Classic "proofs without words" - watch the ancient theorem come to life
        through geometric rearrangements and area comparisons.
        """
    )
    return


@app.cell
def _(mo):
    pythag_scenes = mo.ui.dropdown(
        options={
            "PythagoreanIntro": "Introduction to the Theorem",
            "BhaskaraProof": "Bhaskara's 'Behold!' Proof",
            "RearrangementProof": "Classic Rearrangement Proof",
            "AreaBasedProof": "Area-Based Proof",
            "EuclideanProof": "Euclid's Similar Triangles Proof",
            "PresidentialProof": "Garfield's Trapezoid Proof",
            "AnimatedProofSummary": "Animated Summary",
        },
        value="BhaskaraProof",
        label="Select Scene:",
    )
    pythag_scenes
    return (pythag_scenes,)


@app.cell
def _(mo, pythag_scenes):
    pythag_render_btn = mo.ui.button(
        label=f"🎬 Render: {pythag_scenes.value}",
        kind="success",
    )
    pythag_render_btn
    return (pythag_render_btn,)


@app.cell
def _(mo, pythag_render_btn, pythag_scenes, run_manim_scene):
    pythag_output = None
    if pythag_render_btn.value:
        mo.output.append(mo.md("⏳ Rendering animation... this may take a moment."))
        video_path, error = run_manim_scene("pythagorean_proofs", pythag_scenes.value)
        if error:
            pythag_output = mo.md(f"❌ {error}")
        elif video_path:
            pythag_output = mo.video(src=video_path)
        else:
            pythag_output = mo.md("❌ Could not find rendered video")
    pythag_output
    return (pythag_output,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## ⚙️ Batch Rendering

        Render multiple scenes at once for a specific category.
        """
    )
    return


@app.cell
def _(mo):
    batch_category = mo.ui.dropdown(
        options={
            "linear_transformations": "Linear Transformations",
            "calculus_visualizations": "Calculus",
            "pythagorean_proofs": "Pythagorean Theorem",
        },
        value="linear_transformations",
        label="Category:",
    )

    quality_select = mo.ui.dropdown(
        options={
            "l": "Low (480p) - Fast",
            "m": "Medium (720p)",
            "h": "High (1080p) - Slow",
        },
        value="l",
        label="Quality:",
    )

    mo.hstack([batch_category, quality_select])
    return batch_category, quality_select


@app.cell
def _(batch_category, mo, quality_select):
    batch_render_btn = mo.ui.button(
        label=f"🎬 Render All {batch_category.value.replace('_', ' ').title()} Scenes ({quality_select.value})",
        kind="warn",
    )
    batch_render_btn
    return (batch_render_btn,)


@app.cell
def _(NOTEBOOK_DIR, batch_category, batch_render_btn, mo, quality_select, subprocess):
    batch_output = None
    if batch_render_btn.value:
        module = batch_category.value
        quality = quality_select.value
        quality_flags = {"l": "-ql", "m": "-qm", "h": "-qh"}

        mo.output.append(mo.md(f"⏳ Rendering all scenes in `{module}`... this may take several minutes."))

        cmd = [
            "uv", "run", "manim",
            quality_flags.get(quality, "-ql"),
            "-a",  # Render all scenes
            f"{module}.py",
        ]

        result = subprocess.run(
            cmd,
            cwd=str(NOTEBOOK_DIR),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            batch_output = mo.md(f"❌ Error:\n```\n{result.stderr}\n```")
        else:
            batch_output = mo.md(f"✅ All scenes rendered!\n\nOutput:\n```\n{result.stdout[-2000:]}\n```")

    batch_output
    return (batch_output,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 📖 Scene Descriptions

        ### Linear Transformations
        | Scene | Description |
        |-------|-------------|
        | `LinearTransformationIntro` | Watch the entire 2D plane transform under a matrix |
        | `BasisVectorTransformation` | See how matrix columns represent transformed basis vectors |
        | `MatrixMultiplicationAsComposition` | Matrix AB = first apply B, then A |
        | `DotProductInterpretation` | Row × Column = Dot Product |
        | `ShearTransformation` | Classic shear example |
        | `RotationTransformation` | 45° rotation matrix in action |
        | `AllTransformations` | Gallery of common transformations |

        ### Calculus
        | Scene | Description |
        |-------|-------------|
        | `FunctionPlotAnimation` | Watch f(x) = x² get drawn |
        | `TangentLineDerivative` | Moving tangent line shows derivative |
        | `SecantToTangent` | Limit definition of derivative |
        | `RiemannSumsToIntegral` | Rectangles → exact area |
        | `DerivativeIntegralRelation` | Fundamental Theorem of Calculus |
        | `AreaAccumulation` | Integral as accumulated area |
        | `PowerRuleDerivative` | Power rule visualization |

        ### Pythagorean Theorem
        | Scene | Description |
        |-------|-------------|
        | `PythagoreanIntro` | Basic theorem introduction |
        | `BhaskaraProof` | Bhaskara's "Behold!" dissection proof |
        | `RearrangementProof` | Two (a+b)² squares, same triangles |
        | `AreaBasedProof` | Squares on each side |
        | `EuclideanProof` | Similar triangles proof |
        | `PresidentialProof` | Garfield's trapezoid proof |
        | `AnimatedProofSummary` | Quick visual summary |
        """
    )
    return


if __name__ == "__main__":
    app.run()
