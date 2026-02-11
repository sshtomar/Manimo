"""
Waves & Fields - Interactive Marimo Notebook
Beautiful visualizations of waves, vector fields, and complex numbers
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
        # Waves, Fields & Complex Numbers

        Interactive visualizations exploring the beautiful mathematics of:

        1. **Trigonometric Waves** - Sine wave generation and interference
        2. **Vector Fields** - Flow and gradient visualizations
        3. **Complex Numbers** - Multiplication as rotation
        4. **Fourier Series** - Building waves from harmonics
        5. **Harmonic Motion** - Pendulums and oscillations

        Select a scene below and click render to generate the animation.
        """
    )
    return


@app.cell
def _():
    import subprocess
    from pathlib import Path

    # Get the directory where this notebook is located
    NOTEBOOK_DIR = Path(__file__).parent if "__file__" in dir() else Path.cwd()
    MEDIA_DIR = NOTEBOOK_DIR / "media"

    def run_manim_scene(module_name: str, scene_name: str, quality: str = "l"):
        """
        Run a Manim scene and return the video bytes for display.

        Args:
            module_name: Name of the Python module (without .py)
            scene_name: Name of the Scene class to render
            quality: Quality level - 'l' (low/480p), 'm' (medium/720p), 'h' (high/1080p)

        Returns:
            Tuple of (video_bytes, error_message). One will be None.
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
                # Return the most recent video as bytes
                latest = max(videos, key=lambda p: p.stat().st_mtime)
                return latest.read_bytes(), None

        return None, "Video not found after rendering"
    return MEDIA_DIR, NOTEBOOK_DIR, run_manim_scene, subprocess


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## Sine Wave Generation

        See how circular motion creates a sine wave. A point rotating on a circle,
        when projected horizontally, traces out the familiar sine curve.
        """
    )
    return


@app.cell
def _(mo):
    scene_options = mo.ui.dropdown(
        options={
            "SineWaveGeneration": "Sine Wave from Circle",
            "WaveInterference": "Wave Interference (Constructive/Destructive)",
            "VectorFieldVisualization": "Vector Field Flow",
            "ComplexMultiplication": "Complex Numbers & Rotation",
            "FourierSeriesSquareWave": "Fourier Series - Square Wave",
            "PendulumMotion": "Pendulum & Simple Harmonic Motion",
        },
        value="SineWaveGeneration",
        label="Select Animation:",
    )
    scene_options
    return (scene_options,)


@app.cell
def _(mo):
    quality_dropdown = mo.ui.dropdown(
        options={
            "l": "Low (480p) - Fast",
            "m": "Medium (720p)",
            "h": "High (1080p) - Slow",
        },
        value="l",
        label="Quality:",
    )
    quality_dropdown
    return (quality_dropdown,)


@app.cell
def _(mo, quality_dropdown, scene_options):
    render_btn = mo.ui.button(
        label=f"Render: {scene_options.value}",
        kind="success",
    )
    render_btn
    return (render_btn,)


@app.cell
def _(mo, quality_dropdown, render_btn, run_manim_scene, scene_options):
    video_output = None
    if render_btn.value:
        mo.output.append(mo.md("Rendering animation... this may take a moment."))
        video_data, error = run_manim_scene(
            "wave_and_field_visualizations",
            scene_options.value,
            quality_dropdown.value
        )
        if error:
            video_output = mo.md(f"**Error:** {error}")
        elif video_data:
            video_output = mo.video(src=video_data, controls=True, rounded=True)
        else:
            video_output = mo.md("Could not find rendered video")
    video_output
    return (video_output,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## Scene Descriptions

        | Scene | What it Shows |
        |-------|--------------|
        | **Sine Wave from Circle** | A rotating point on a circle projects to create a sine wave - the fundamental connection between circular motion and trigonometry |
        | **Wave Interference** | Two waves combine - watch constructive and destructive interference as phase changes |
        | **Vector Field Flow** | Arrows showing how vectors vary across 2D space, with a particle following the flow |
        | **Complex Numbers & Rotation** | Multiplication by *i* rotates by 90 degrees - see why i^2 = -1 makes geometric sense |
        | **Fourier Series** | Build a square wave from sine waves - any periodic function is a sum of harmonics |
        | **Pendulum Motion** | Simple harmonic motion traces out a sine wave over time |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## Mathematical Background

        ### Sine Wave Generation
        A point $(x, y)$ on a unit circle can be written as:
        $$x = \cos(\theta), \quad y = \sin(\theta)$$
        As $\theta$ increases uniformly with time, the $y$-coordinate traces a sine wave.

        ### Wave Interference
        When two waves $y_1 = A\sin(\omega t)$ and $y_2 = A\sin(\omega t + \phi)$ combine:
        - **Constructive** ($\phi = 0$): amplitudes add, wave gets bigger
        - **Destructive** ($\phi = \pi$): amplitudes cancel, wave disappears

        ### Complex Multiplication
        Multiplying by $e^{i\theta}$ rotates a complex number by angle $\theta$:
        $$z \cdot e^{i\theta} = |z| \cdot e^{i(\arg(z) + \theta)}$$
        Since $i = e^{i\pi/2}$, multiplying by $i$ rotates by 90 degrees.

        ### Fourier Series
        Any periodic function can be written as a sum of sines and cosines:
        $$f(x) = \frac{a_0}{2} + \sum_{n=1}^{\infty} \left[ a_n \cos(nx) + b_n \sin(nx) \right]$$
        """
    )
    return


if __name__ == "__main__":
    app.run()
