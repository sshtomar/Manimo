"""
Introduction to Linear Algebra — Interactive Marimo Notebook
Row view vs column view, span, linear combinations, and linear dependence
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
        # Introduction to Linear Algebra

        This notebook builds geometric intuition for the most fundamental ideas
        in linear algebra, following the approach of **Gilbert Strang** and
        **3Blue1Brown**:

        1. **Row Picture** — each equation is a line (or plane); the solution is their intersection
        2. **Column Picture** — the solution tells you how to combine column vectors to reach **b**
        3. **Linear Combinations** — scaling and adding vectors
        4. **Span** — the set of all vectors you can reach with linear combinations
        5. **Linear Independence** — when no vector in a set is redundant
        6. **Basis** — a minimal spanning set that reaches every point in the space

        Select a scene below and click **Render** to generate the animation.

        ---
        """
    )
    return


@app.cell
def _():
    import subprocess
    from pathlib import Path

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
            "l": "-ql",
            "m": "-qm",
            "h": "-qh",
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

        quality_dirs = {"l": "480p15", "m": "720p30", "h": "1080p60"}
        video_dir = MEDIA_DIR / "videos" / module_name / quality_dirs.get(quality, "480p15")

        if video_dir.exists():
            videos = list(video_dir.glob("*.mp4"))
            if videos:
                latest = max(videos, key=lambda p: p.stat().st_mtime)
                return latest.read_bytes(), None

        return None, "Video not found after rendering"
    return NOTEBOOK_DIR, MEDIA_DIR, run_manim_scene, subprocess


# ---------------------------------------------------------------------------
# Section 1: Row Picture
# ---------------------------------------------------------------------------

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The Row Picture

        Consider a system of two equations:

        $$x + 2y = 5$$
        $$2x - y = 0$$

        In the **row picture**, each equation describes a **line** in the $(x,y)$ plane.
        The solution is the **point where all lines meet**.

        This is the view you're most familiar with from high-school algebra —
        "solve two equations, find where they cross."
        """
    )
    return


@app.cell
def _(mo, run_manim_scene):
    row_btn = mo.ui.button(label="Render: Row Picture", kind="success")
    row_btn
    return (row_btn,)


@app.cell
def _(mo, row_btn, run_manim_scene):
    row_output = None
    if row_btn.value:
        mo.output.append(mo.md("Rendering animation..."))
        video_data, error = run_manim_scene("intro_linear_algebra", "RowViewLines")
        if error:
            row_output = mo.md(f"**Error:** {error}")
        elif video_data:
            row_output = mo.video(src=video_data, controls=True, rounded=True)
        else:
            row_output = mo.md("Could not find rendered video")
    row_output
    return


# ---------------------------------------------------------------------------
# Section 2: Column Picture
# ---------------------------------------------------------------------------

@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 2. The Column Picture

        Now look at the **same system** from a completely different angle.
        Rewrite $A\mathbf{x} = \mathbf{b}$ as a **linear combination of columns**:

        $$
        x \begin{bmatrix} 1 \\ 2 \end{bmatrix}
        + y \begin{bmatrix} 2 \\ -1 \end{bmatrix}
        = \begin{bmatrix} 5 \\ 0 \end{bmatrix}
        $$

        The question becomes: *"What combination of the column vectors
        reaches the target vector $\mathbf{b}$?"*

        This is **Strang's key insight**: thinking in columns gives you
        geometric intuition that the row picture hides.
        """
    )
    return


@app.cell
def _(mo, run_manim_scene):
    col_btn = mo.ui.button(label="Render: Column Picture", kind="success")
    col_btn
    return (col_btn,)


@app.cell
def _(col_btn, mo, run_manim_scene):
    col_output = None
    if col_btn.value:
        mo.output.append(mo.md("Rendering animation..."))
        video_data, error = run_manim_scene("intro_linear_algebra", "ColumnViewCombination")
        if error:
            col_output = mo.md(f"**Error:** {error}")
        elif video_data:
            col_output = mo.video(src=video_data, controls=True, rounded=True)
        else:
            col_output = mo.md("Could not find rendered video")
    col_output
    return


# ---------------------------------------------------------------------------
# Section 3: Row vs Column side by side
# ---------------------------------------------------------------------------

@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 3. Row Picture vs Column Picture — Side by Side

        Both views describe **the same system** and give **the same answer**.
        But they highlight different geometry:

        | | Row Picture | Column Picture |
        |---|---|---|
        | **Each row/column is...** | a line (or plane, hyperplane) | a vector |
        | **Solution means...** | intersection of lines | right combination of vectors |
        | **Breaks when...** | lines are parallel (no intersection) | columns are dependent (can't reach $\mathbf{b}$) |
        | **Scales to $n$ dimensions** | hard to visualize | still just vector addition |
        """
    )
    return


@app.cell
def _(mo, run_manim_scene):
    side_btn = mo.ui.button(label="Render: Side-by-Side Comparison", kind="success")
    side_btn
    return (side_btn,)


@app.cell
def _(mo, run_manim_scene, side_btn):
    side_output = None
    if side_btn.value:
        mo.output.append(mo.md("Rendering animation..."))
        video_data, error = run_manim_scene("intro_linear_algebra", "RowVsColumnSideBySide")
        if error:
            side_output = mo.md(f"**Error:** {error}")
        elif video_data:
            side_output = mo.video(src=video_data, controls=True, rounded=True)
        else:
            side_output = mo.md("Could not find rendered video")
    side_output
    return


# ---------------------------------------------------------------------------
# Section 4: Linear Combinations
# ---------------------------------------------------------------------------

@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 4. Linear Combinations

        A **linear combination** of vectors $\vec{v}_1$ and $\vec{v}_2$ is any expression:

        $$c_1 \vec{v}_1 + c_2 \vec{v}_2$$

        where $c_1, c_2$ are scalars (real numbers).

        Geometrically: **scale** each vector, then **add** them head-to-tail.
        The result is a new vector that depends on your choice of scalars.

        > This is the single most important operation in linear algebra.
        > Matrix-vector multiplication, projections, change of basis —
        > they're all linear combinations in disguise.
        """
    )
    return


@app.cell
def _(mo, run_manim_scene):
    lc_btn = mo.ui.button(label="Render: Linear Combination", kind="success")
    lc_btn
    return (lc_btn,)


@app.cell
def _(lc_btn, mo, run_manim_scene):
    lc_output = None
    if lc_btn.value:
        mo.output.append(mo.md("Rendering animation..."))
        video_data, error = run_manim_scene("intro_linear_algebra", "LinearCombination2D")
        if error:
            lc_output = mo.md(f"**Error:** {error}")
        elif video_data:
            lc_output = mo.video(src=video_data, controls=True, rounded=True)
        else:
            lc_output = mo.md("Could not find rendered video")
    lc_output
    return


# ---------------------------------------------------------------------------
# Section 5: Span
# ---------------------------------------------------------------------------

@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 5. Span

        The **span** of a set of vectors is the set of **all possible linear
        combinations** you can make with them.

        $$\text{Span}(\vec{v}_1, \vec{v}_2) = \{ c_1 \vec{v}_1 + c_2 \vec{v}_2 \mid c_1, c_2 \in \mathbb{R} \}$$

        - If $\vec{v}_1$ and $\vec{v}_2$ point in **different directions** (independent), their span is **all of $\mathbb{R}^2$** — you can reach any point in the plane.
        - If $\vec{v}_2$ is just a scaled copy of $\vec{v}_1$ (dependent), the span collapses to **a single line** — you're stuck on one direction.

        The animation shows both cases.
        """
    )
    return


@app.cell
def _(mo, run_manim_scene):
    span_btn = mo.ui.button(label="Render: Span of Vectors", kind="success")
    span_btn
    return (span_btn,)


@app.cell
def _(mo, run_manim_scene, span_btn):
    span_output = None
    if span_btn.value:
        mo.output.append(mo.md("Rendering animation..."))
        video_data, error = run_manim_scene("intro_linear_algebra", "Span2D")
        if error:
            span_output = mo.md(f"**Error:** {error}")
        elif video_data:
            span_output = mo.video(src=video_data, controls=True, rounded=True)
        else:
            span_output = mo.md("Could not find rendered video")
    span_output
    return


# ---------------------------------------------------------------------------
# Section 6: Linear Independence
# ---------------------------------------------------------------------------

@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 6. Linear Independence

        Vectors are **linearly independent** if none of them can be written as a
        linear combination of the others. In other words, no vector is "redundant."

        - **Independent**: $\vec{v}_1$ and $\vec{v}_2$ point in genuinely different directions.
          Removing either one *shrinks* what you can reach.
        - **Dependent**: $\vec{v}_2 = 3\vec{v}_1$. The second vector adds no new
          reachable directions — it's redundant.

        Independence matters because it determines whether $A\mathbf{x} = \mathbf{b}$
        has a unique solution, infinitely many, or none at all.
        """
    )
    return


@app.cell
def _(mo, run_manim_scene):
    dep_btn = mo.ui.button(label="Render: Linear Independence", kind="success")
    dep_btn
    return (dep_btn,)


@app.cell
def _(dep_btn, mo, run_manim_scene):
    dep_output = None
    if dep_btn.value:
        mo.output.append(mo.md("Rendering animation..."))
        video_data, error = run_manim_scene("intro_linear_algebra", "LinearDependence")
        if error:
            dep_output = mo.md(f"**Error:** {error}")
        elif video_data:
            dep_output = mo.video(src=video_data, controls=True, rounded=True)
        else:
            dep_output = mo.md("Could not find rendered video")
    dep_output
    return


# ---------------------------------------------------------------------------
# Section 7: Basis
# ---------------------------------------------------------------------------

@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## 7. Basis — Spanning Without Redundancy

        A **basis** for a vector space is a set of vectors that is:
        1. **Linearly independent** — no vector is redundant
        2. **Spanning** — you can reach every vector in the space

        The standard basis for $\mathbb{R}^2$ is $\{\hat{e}_1, \hat{e}_2\}$:

        $$
        \hat{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad
        \hat{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
        $$

        Any vector $(a, b)$ is uniquely $a\hat{e}_1 + b\hat{e}_2$.
        But the standard basis isn't the *only* basis — any two independent
        vectors form a valid basis for $\mathbb{R}^2$.
        """
    )
    return


@app.cell
def _(mo, run_manim_scene):
    basis_btn = mo.ui.button(label="Render: Basis Spans the Space", kind="success")
    basis_btn
    return (basis_btn,)


@app.cell
def _(basis_btn, mo, run_manim_scene):
    basis_output = None
    if basis_btn.value:
        mo.output.append(mo.md("Rendering animation..."))
        video_data, error = run_manim_scene("intro_linear_algebra", "SpanAndBasis")
        if error:
            basis_output = mo.md(f"**Error:** {error}")
        elif video_data:
            basis_output = mo.video(src=video_data, controls=True, rounded=True)
        else:
            basis_output = mo.md("Could not find rendered video")
    basis_output
    return


# ---------------------------------------------------------------------------
# Summary & Scene Reference
# ---------------------------------------------------------------------------

@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## Summary

        | Concept | One-liner |
        |---------|-----------|
        | **Row picture** | Each equation is a geometric constraint (line/plane); solution is their intersection |
        | **Column picture** | Solution = the right linear combination of column vectors to reach **b** |
        | **Linear combination** | Scale vectors and add: $c_1\vec{v}_1 + c_2\vec{v}_2$ |
        | **Span** | All vectors reachable by linear combinations of a set |
        | **Linear independence** | No vector in the set is a combination of the others |
        | **Basis** | A minimal independent set that spans the whole space |

        ### Scene Reference

        | Scene | Description |
        |-------|-------------|
        | `RowViewLines` | Row picture — two lines intersecting |
        | `ColumnViewCombination` | Column picture — combining column vectors |
        | `RowVsColumnSideBySide` | Both views side by side |
        | `LinearCombination2D` | Scaling and adding two vectors |
        | `Span2D` | Span of independent vs dependent vectors |
        | `LinearDependence` | Independent vs dependent side by side |
        | `SpanAndBasis` | Standard basis decomposition of a vector |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ## Mathematical Background

        ### The Two Pictures of $A\mathbf{x} = \mathbf{b}$

        For a $2 \times 2$ system:

        $$
        \begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix}
        \begin{bmatrix} x \\ y \end{bmatrix}
        = \begin{bmatrix} b_1 \\ b_2 \end{bmatrix}
        $$

        **Row picture** — read each *row* as a separate equation:
        $$a_{11}x + a_{12}y = b_1 \quad \text{(a line)}$$
        $$a_{21}x + a_{22}y = b_2 \quad \text{(a line)}$$

        **Column picture** — read each *column* as a vector to combine:
        $$x \begin{bmatrix} a_{11} \\ a_{21} \end{bmatrix} + y \begin{bmatrix} a_{12} \\ a_{22} \end{bmatrix} = \begin{bmatrix} b_1 \\ b_2 \end{bmatrix}$$

        ### When Things Break

        - **Row view**: parallel lines $\Rightarrow$ no intersection $\Rightarrow$ no solution
        - **Column view**: dependent columns $\Rightarrow$ can't reach every $\mathbf{b}$ $\Rightarrow$ no solution (for some $\mathbf{b}$)

        Both views are equivalent — they just emphasize different geometry.
        """
    )
    return


if __name__ == "__main__":
    app.run()
