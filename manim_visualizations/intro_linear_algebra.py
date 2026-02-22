"""
Introduction to Linear Algebra — Row View vs Column View, Span, and Linear Combinations
Inspired by 3Blue1Brown and Gilbert Strang's geometric intuition approach

Scenes:
    RowViewLines          – Ax = b as intersection of lines (row picture)
    ColumnViewCombination – Ax = b as a linear combination of columns (column picture)
    RowVsColumnSideBySide – Both views together for direct comparison
    LinearCombination2D   – What a linear combination looks like geometrically
    Span2D                – Span of two vectors in 2D (line vs plane)
    LinearDependence      – Dependent vs independent vectors
    SpanAndBasis          – How basis vectors span all of R^2
"""

from manim import (
    VGroup,
    Arrow,
    Line,
    Dot,
    Text,
    MathTex,
    Tex,
    NumberPlane,
    Axes,
    Create,
    Write,
    FadeIn,
    FadeOut,
    Transform,
    ReplacementTransform,
    GrowArrow,
    Indicate,
    MoveToTarget,
    AnimationGroup,
    SurroundingRectangle,
    DashedLine,
    Rectangle,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    PI,
    np,
    config,
    ValueTracker,
    always_redraw,
    Polygon,
    rate_functions,
)

from themed_scene import ThemedScene


# ---------------------------------------------------------------------------
# Scene 1: Row View — each equation is a line, solution is the intersection
# ---------------------------------------------------------------------------

class RowViewLines(ThemedScene):
    """
    The ROW picture of Ax = b.

    System:  x + 2y = 5
             2x -  y = 0

    Each equation is a line in the (x, y) plane.
    The solution (1, 2) is where they cross.
    """

    def construct(self):
        t = self.theme

        # Title
        title = Text("Row Picture", font_size=t.title_size, color=t.foreground)
        title.to_edge(UP)
        self.play(Write(title))

        # Axes
        axes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 4, 1],
            x_length=8,
            y_length=5,
            axis_config={
                "color": t.muted,
                "stroke_width": t.axis_stroke_width,
                "include_numbers": True,
            },
        ).shift(DOWN * 0.3)
        x_label = axes.get_x_axis_label("x", direction=RIGHT)
        y_label = axes.get_y_axis_label("y", direction=UP)
        self.play(Create(axes), Write(x_label), Write(y_label))

        # Equation 1: x + 2y = 5  =>  y = (5 - x) / 2
        line1 = axes.plot(lambda x: (5 - x) / 2, x_range=[-0.5, 5.5], color=t.primary)
        eq1 = MathTex(r"x + 2y = 5", font_size=t.body_size, color=t.primary)
        eq1.next_to(axes.c2p(5, 0.2), RIGHT, buff=0.2)
        self.play(Create(line1), Write(eq1))
        self.wait(0.5)

        # Equation 2: 2x - y = 0  =>  y = 2x
        line2 = axes.plot(lambda x: 2 * x, x_range=[-0.5, 2.5], color=t.secondary)
        eq2 = MathTex(r"2x - y = 0", font_size=t.body_size, color=t.secondary)
        eq2.next_to(axes.c2p(2.5, 5), LEFT, buff=0.2).shift(DOWN * 0.3)
        self.play(Create(line2), Write(eq2))
        self.wait(0.5)

        # Intersection point (1, 2)
        dot = Dot(axes.c2p(1, 2), color=t.accent, radius=0.12)
        sol_label = MathTex(r"(1, 2)", font_size=t.body_size, color=t.accent)
        sol_label.next_to(dot, UP + RIGHT, buff=0.15)
        self.play(FadeIn(dot, scale=2), Write(sol_label))

        # Explanation
        note = Text(
            "Each row is a line — solution is their intersection",
            font_size=t.label_size,
            color=t.foreground,
        )
        note.to_edge(DOWN)
        self.play(Write(note))
        self.wait(2)


# ---------------------------------------------------------------------------
# Scene 2: Column View — solution as a linear combination of column vectors
# ---------------------------------------------------------------------------

class ColumnViewCombination(ThemedScene):
    """
    The COLUMN picture of Ax = b.

    System:  x [1, 2] + y [-2, 1]  = [5, 0]
                 ^col1      ^col2      ^b

    (Actual solution is different system for nice geometry:
     x [1, 2] + y [2, -1] = [5, 0]  =>  x=1, y=2)

    Shows column vectors being scaled and added to reach b.
    """

    def construct(self):
        t = self.theme

        title = Text("Column Picture", font_size=t.title_size, color=t.foreground)
        title.to_edge(UP)
        self.play(Write(title))

        # Plane
        plane = NumberPlane(
            x_range=[-2, 7, 1],
            y_range=[-2, 5, 1],
            x_length=9,
            y_length=7,
            background_line_style={"stroke_opacity": 0.2, "stroke_color": t.muted},
            axis_config={"color": t.muted, "stroke_width": t.axis_stroke_width},
        ).shift(DOWN * 0.3)
        self.play(Create(plane), run_time=0.8)

        # Column vectors (unscaled)
        col1_vec = Arrow(
            plane.c2p(0, 0), plane.c2p(1, 2), buff=0,
            color=t.primary, stroke_width=t.heavy_stroke_width,
        )
        col1_label = MathTex(
            r"\begin{bmatrix} 1 \\ 2 \end{bmatrix}",
            font_size=t.label_size, color=t.primary,
        ).next_to(col1_vec.get_end(), LEFT, buff=0.15)

        col2_vec = Arrow(
            plane.c2p(0, 0), plane.c2p(2, -1), buff=0,
            color=t.secondary, stroke_width=t.heavy_stroke_width,
        )
        col2_label = MathTex(
            r"\begin{bmatrix} 2 \\ -1 \end{bmatrix}",
            font_size=t.label_size, color=t.secondary,
        ).next_to(col2_vec.get_end(), DOWN + RIGHT, buff=0.15)

        self.play(GrowArrow(col1_vec), Write(col1_label))
        self.play(GrowArrow(col2_vec), Write(col2_label))
        self.wait(0.5)

        # Show the equation
        equation = MathTex(
            r"x", r"\begin{bmatrix} 1 \\ 2 \end{bmatrix}",
            r"+ \; y", r"\begin{bmatrix} 2 \\ -1 \end{bmatrix}",
            r"=", r"\begin{bmatrix} 5 \\ 0 \end{bmatrix}",
            font_size=t.body_size,
        )
        equation[0].set_color(t.primary)
        equation[1].set_color(t.primary)
        equation[2].set_color(t.secondary)
        equation[3].set_color(t.secondary)
        equation[5].set_color(t.accent)
        equation.to_corner(UP + RIGHT).shift(DOWN * 0.6)
        equation.add_background_rectangle(opacity=0.8)
        self.play(Write(equation))
        self.wait(1)

        # Scale col1 by x=1 (stays same), scale col2 by y=2
        self.play(FadeOut(col1_label), FadeOut(col2_label))

        # x=1 * col1
        x_label = MathTex(r"1 \cdot", font_size=t.body_size, color=t.primary)
        x_label.next_to(col1_vec.get_center(), LEFT, buff=0.3)
        self.play(Write(x_label))

        # y=2 * col2  => (4, -2)
        scaled_col2 = Arrow(
            plane.c2p(0, 0), plane.c2p(4, -2), buff=0,
            color=t.secondary, stroke_width=t.heavy_stroke_width,
        )
        y_label = MathTex(r"2 \cdot", font_size=t.body_size, color=t.secondary)
        y_label.next_to(scaled_col2.get_center(), DOWN + RIGHT, buff=0.15)
        self.play(Transform(col2_vec, scaled_col2), Write(y_label))
        self.wait(0.5)

        # Move scaled col2 to tip of col1 (head-to-tail addition)
        shifted_col2 = Arrow(
            plane.c2p(1, 2), plane.c2p(5, 0), buff=0,
            color=t.secondary, stroke_width=t.heavy_stroke_width,
        )
        self.play(
            Transform(col2_vec, shifted_col2),
            FadeOut(x_label), FadeOut(y_label),
        )
        self.wait(0.3)

        # Result vector b = (5, 0)
        b_vec = Arrow(
            plane.c2p(0, 0), plane.c2p(5, 0), buff=0,
            color=t.accent, stroke_width=t.heavy_stroke_width,
        )
        b_label = MathTex(
            r"\vec{b} = \begin{bmatrix} 5 \\ 0 \end{bmatrix}",
            font_size=t.body_size, color=t.accent,
        )
        b_label.next_to(b_vec.get_center(), DOWN, buff=0.2)

        self.play(GrowArrow(b_vec), Write(b_label))

        note = Text(
            "Combine column vectors to reach b",
            font_size=t.label_size, color=t.foreground,
        )
        note.to_edge(DOWN)
        self.play(Write(note))
        self.wait(2)


# ---------------------------------------------------------------------------
# Scene 3: Side-by-side comparison of Row vs Column view
# ---------------------------------------------------------------------------

class RowVsColumnSideBySide(ThemedScene):
    """
    Split screen: left shows the row picture, right shows the column picture,
    for the same 2x2 system.
    """

    def construct(self):
        t = self.theme

        title = Text(
            "Row Picture vs Column Picture",
            font_size=t.title_size, color=t.foreground,
        )
        title.to_edge(UP)
        self.play(Write(title))

        # The system
        system = MathTex(
            r"x + 2y = 5", r"\\" r"2x - y = 0",
            font_size=t.body_size,
        )
        system.next_to(title, DOWN, buff=0.3)
        self.play(Write(system))
        self.wait(0.5)

        # ---- LEFT: Row picture ----
        row_label = Text("Row Picture", font_size=t.label_size, color=t.primary)
        row_label.move_to(LEFT * 3.5 + UP * 1.2)

        axes_l = Axes(
            x_range=[-0.5, 4, 1], y_range=[-0.5, 3.5, 1],
            x_length=4, y_length=3.5,
            axis_config={"color": t.muted, "stroke_width": t.fine_stroke_width},
        ).move_to(LEFT * 3.5 + DOWN * 1)

        line1 = axes_l.plot(lambda x: (5 - x) / 2, x_range=[0, 4], color=t.primary)
        line2 = axes_l.plot(lambda x: 2 * x, x_range=[0, 2], color=t.secondary)
        dot_l = Dot(axes_l.c2p(1, 2), color=t.accent, radius=0.1)

        self.play(Write(row_label), Create(axes_l))
        self.play(Create(line1), Create(line2))
        self.play(FadeIn(dot_l, scale=2))

        each_row_note = Text(
            "Each row = a line",
            font_size=t.small_size, color=t.muted,
        ).next_to(axes_l, DOWN, buff=0.2)
        self.play(Write(each_row_note))

        # ---- RIGHT: Column picture ----
        col_label = Text("Column Picture", font_size=t.label_size, color=t.secondary)
        col_label.move_to(RIGHT * 3.5 + UP * 1.2)

        axes_r = Axes(
            x_range=[-1, 6, 1], y_range=[-2.5, 3, 1],
            x_length=4, y_length=3.5,
            axis_config={"color": t.muted, "stroke_width": t.fine_stroke_width},
        ).move_to(RIGHT * 3.5 + DOWN * 1)

        c1 = Arrow(
            axes_r.c2p(0, 0), axes_r.c2p(1, 2), buff=0,
            color=t.primary, stroke_width=t.curve_stroke_width,
        )
        c2_shifted = Arrow(
            axes_r.c2p(1, 2), axes_r.c2p(5, 0), buff=0,
            color=t.secondary, stroke_width=t.curve_stroke_width,
        )
        b_vec = Arrow(
            axes_r.c2p(0, 0), axes_r.c2p(5, 0), buff=0,
            color=t.accent, stroke_width=t.curve_stroke_width,
        )

        self.play(Write(col_label), Create(axes_r))
        self.play(GrowArrow(c1), GrowArrow(c2_shifted))
        self.play(GrowArrow(b_vec))

        each_col_note = Text(
            "Each column = a vector",
            font_size=t.small_size, color=t.muted,
        ).next_to(axes_r, DOWN, buff=0.2)
        self.play(Write(each_col_note))

        # Divider
        divider = DashedLine(
            UP * 1.5, DOWN * 3.5,
            color=t.muted, stroke_width=t.fine_stroke_width,
        )
        self.play(Create(divider))

        # Same answer
        answer = MathTex(
            r"x = 1, \; y = 2",
            font_size=t.body_size, color=t.accent,
        )
        answer.to_edge(DOWN)
        self.play(Write(answer))
        self.wait(2)


# ---------------------------------------------------------------------------
# Scene 4: Linear Combination in 2D
# ---------------------------------------------------------------------------

class LinearCombination2D(ThemedScene):
    """
    Show c1 * v1 + c2 * v2 as scalars sweep, building geometric intuition
    for what 'linear combination' means.
    """

    def construct(self):
        t = self.theme

        title = Text("Linear Combination", font_size=t.title_size, color=t.foreground)
        title.to_edge(UP)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.15, "stroke_color": t.muted},
            axis_config={"color": t.muted, "stroke_width": t.axis_stroke_width},
        )
        self.play(Create(plane), run_time=0.6)

        # Define two vectors
        v1_coords = np.array([2, 1, 0])
        v2_coords = np.array([1, 2, 0])

        v1 = Arrow(ORIGIN, v1_coords, buff=0, color=t.primary, stroke_width=t.heavy_stroke_width)
        v2 = Arrow(ORIGIN, v2_coords, buff=0, color=t.secondary, stroke_width=t.heavy_stroke_width)

        v1_label = MathTex(r"\vec{v}_1", font_size=t.body_size, color=t.primary)
        v1_label.next_to(v1.get_end(), DOWN + RIGHT, buff=0.1)
        v2_label = MathTex(r"\vec{v}_2", font_size=t.body_size, color=t.secondary)
        v2_label.next_to(v2.get_end(), UP + LEFT, buff=0.1)

        self.play(GrowArrow(v1), Write(v1_label))
        self.play(GrowArrow(v2), Write(v2_label))
        self.wait(0.5)

        # Formula
        formula = MathTex(
            r"c_1", r"\vec{v}_1", r"+ \; c_2", r"\vec{v}_2",
            font_size=t.subtitle_size,
        )
        formula[0].set_color(t.primary)
        formula[1].set_color(t.primary)
        formula[2].set_color(t.secondary)
        formula[3].set_color(t.secondary)
        formula.to_corner(UP + RIGHT).shift(DOWN * 0.5)
        formula.add_background_rectangle(opacity=0.8)
        self.play(Write(formula))
        self.wait(0.5)

        # Animate a specific combination: 1.5 * v1 + 1 * v2 = (4, 3.5)
        c1, c2 = 1.5, 1.0
        scaled_v1 = Arrow(
            ORIGIN, c1 * v1_coords, buff=0,
            color=t.primary, stroke_width=t.curve_stroke_width,
        )
        scaled_v1_label = MathTex(
            r"1.5 \, \vec{v}_1", font_size=t.label_size, color=t.primary,
        ).next_to(scaled_v1.get_center(), DOWN, buff=0.15)

        self.play(
            Transform(v1, scaled_v1),
            FadeOut(v1_label),
            Write(scaled_v1_label),
        )
        self.wait(0.3)

        # Shift v2 to tip of scaled v1
        start = c1 * v1_coords
        end = start + c2 * v2_coords
        shifted_v2 = Arrow(
            start, end, buff=0,
            color=t.secondary, stroke_width=t.curve_stroke_width,
        )
        shifted_label = MathTex(
            r"1 \, \vec{v}_2", font_size=t.label_size, color=t.secondary,
        ).next_to(shifted_v2.get_center(), LEFT, buff=0.15)

        self.play(
            Transform(v2, shifted_v2),
            FadeOut(v2_label),
            Write(shifted_label),
        )
        self.wait(0.3)

        # Result
        result = Arrow(
            ORIGIN, end, buff=0,
            color=t.accent, stroke_width=t.heavy_stroke_width,
        )
        result_label = MathTex(
            r"c_1 \vec{v}_1 + c_2 \vec{v}_2",
            font_size=t.body_size, color=t.accent,
        ).next_to(result.get_end(), RIGHT, buff=0.15)

        self.play(GrowArrow(result), Write(result_label))

        note = Text(
            "Scale and add — that's a linear combination",
            font_size=t.label_size, color=t.foreground,
        )
        note.to_edge(DOWN)
        self.play(Write(note))
        self.wait(2)


# ---------------------------------------------------------------------------
# Scene 5: Span of two vectors
# ---------------------------------------------------------------------------

class Span2D(ThemedScene):
    """
    Demonstrate span:
    1) Two INDEPENDENT vectors -> span = all of R^2 (the full plane lights up)
    2) Two DEPENDENT vectors   -> span = just a line
    """

    def construct(self):
        t = self.theme

        title = Text("Span of Vectors", font_size=t.title_size, color=t.foreground)
        title.to_edge(UP)
        self.play(Write(title))

        # --- Part 1: Independent vectors span R^2 ---
        part1_label = Text(
            "Independent vectors", font_size=t.body_size, color=t.primary,
        )
        part1_label.next_to(title, DOWN, buff=0.3)
        self.play(Write(part1_label))

        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.15, "stroke_color": t.muted},
            axis_config={"color": t.muted, "stroke_width": t.axis_stroke_width},
        ).shift(DOWN * 0.5)
        self.play(Create(plane), run_time=0.6)

        v1 = Arrow(ORIGIN + DOWN * 0.5, plane.c2p(2, 1), buff=0, color=t.primary,
                    stroke_width=t.heavy_stroke_width)
        v2 = Arrow(ORIGIN + DOWN * 0.5, plane.c2p(-1, 1.5), buff=0, color=t.secondary,
                    stroke_width=t.heavy_stroke_width)

        v1_label = MathTex(r"\vec{v}_1", color=t.primary, font_size=t.body_size)
        v1_label.next_to(v1.get_end(), RIGHT, buff=0.1)
        v2_label = MathTex(r"\vec{v}_2", color=t.secondary, font_size=t.body_size)
        v2_label.next_to(v2.get_end(), LEFT, buff=0.1)

        self.play(GrowArrow(v1), GrowArrow(v2), Write(v1_label), Write(v2_label))
        self.wait(0.5)

        # Show sample combinations spreading across the plane
        dots = VGroup()
        for c1 in np.linspace(-1.5, 1.5, 7):
            for c2 in np.linspace(-1.5, 1.5, 7):
                pt = c1 * np.array([2, 1, 0]) + c2 * np.array([-1, 1.5, 0])
                pt += np.array([0, -0.5, 0])  # shift to match plane center
                dots.add(Dot(pt, color=t.accent, radius=0.05, fill_opacity=0.6))

        self.play(FadeIn(dots, lag_ratio=0.02), run_time=1.5)

        span_note = MathTex(
            r"\text{Span}(\vec{v}_1, \vec{v}_2) = \mathbb{R}^2",
            font_size=t.body_size, color=t.accent,
        )
        span_note.to_edge(DOWN)
        self.play(Write(span_note))
        self.wait(1.5)

        # Clear for part 2
        self.play(
            FadeOut(dots), FadeOut(v1), FadeOut(v2),
            FadeOut(v1_label), FadeOut(v2_label),
            FadeOut(span_note), FadeOut(part1_label),
        )

        # --- Part 2: Dependent vectors span only a line ---
        part2_label = Text(
            "Dependent vectors", font_size=t.body_size, color=t.secondary,
        )
        part2_label.next_to(title, DOWN, buff=0.3)
        self.play(Write(part2_label))

        w1 = Arrow(ORIGIN + DOWN * 0.5, plane.c2p(2, 1), buff=0, color=t.primary,
                    stroke_width=t.heavy_stroke_width)
        w2 = Arrow(ORIGIN + DOWN * 0.5, plane.c2p(4, 2), buff=0, color=t.secondary,
                    stroke_width=t.heavy_stroke_width)

        w1_label = MathTex(r"\vec{w}_1", color=t.primary, font_size=t.body_size)
        w1_label.next_to(w1.get_end(), UP + LEFT, buff=0.1)
        w2_label = MathTex(
            r"\vec{w}_2 = 2\vec{w}_1", color=t.secondary, font_size=t.label_size,
        )
        w2_label.next_to(w2.get_end(), DOWN + RIGHT, buff=0.1)

        self.play(GrowArrow(w1), GrowArrow(w2), Write(w1_label), Write(w2_label))
        self.wait(0.5)

        # The span is just a line through the direction (2, 1)
        span_line = Line(
            plane.c2p(-4, -2), plane.c2p(4, 2),
            color=t.accent, stroke_width=t.curve_stroke_width,
        )
        self.play(Create(span_line))

        span_note2 = MathTex(
            r"\text{Span}(\vec{w}_1, \vec{w}_2) = \text{a line}",
            font_size=t.body_size, color=t.accent,
        )
        span_note2.to_edge(DOWN)
        self.play(Write(span_note2))
        self.wait(2)


# ---------------------------------------------------------------------------
# Scene 6: Linear Dependence
# ---------------------------------------------------------------------------

class LinearDependence(ThemedScene):
    """
    Contrast linearly independent vs dependent sets of vectors.
    Show that dependence means one vector is 'redundant' — it lives
    in the span of the others.
    """

    def construct(self):
        t = self.theme

        title = Text("Linear Independence", font_size=t.title_size, color=t.foreground)
        title.to_edge(UP)
        self.play(Write(title))

        # --- LEFT: Independent ---
        left_label = Text("Independent", font_size=t.body_size, color=t.tertiary)
        left_label.move_to(LEFT * 3.5 + UP * 1.8)
        self.play(Write(left_label))

        axes_l = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=4, y_length=4,
            axis_config={"color": t.muted, "stroke_width": t.fine_stroke_width},
        ).move_to(LEFT * 3.5 + DOWN * 0.5)
        self.play(Create(axes_l))

        a1 = Arrow(
            axes_l.c2p(0, 0), axes_l.c2p(2, 1), buff=0,
            color=t.primary, stroke_width=t.heavy_stroke_width,
        )
        a2 = Arrow(
            axes_l.c2p(0, 0), axes_l.c2p(-1, 2), buff=0,
            color=t.secondary, stroke_width=t.heavy_stroke_width,
        )
        self.play(GrowArrow(a1), GrowArrow(a2))

        indep_note = Text(
            "Neither is a multiple\nof the other",
            font_size=t.small_size, color=t.muted,
        )
        indep_note.next_to(axes_l, DOWN, buff=0.3)
        self.play(Write(indep_note))

        # --- RIGHT: Dependent ---
        right_label = Text("Dependent", font_size=t.body_size, color=t.accent2)
        right_label.move_to(RIGHT * 3.5 + UP * 1.8)
        self.play(Write(right_label))

        axes_r = Axes(
            x_range=[-3, 5, 1], y_range=[-3, 3, 1],
            x_length=4, y_length=4,
            axis_config={"color": t.muted, "stroke_width": t.fine_stroke_width},
        ).move_to(RIGHT * 3.5 + DOWN * 0.5)
        self.play(Create(axes_r))

        b1 = Arrow(
            axes_r.c2p(0, 0), axes_r.c2p(1, 1), buff=0,
            color=t.primary, stroke_width=t.heavy_stroke_width,
        )
        b2 = Arrow(
            axes_r.c2p(0, 0), axes_r.c2p(3, 3), buff=0,
            color=t.secondary, stroke_width=t.heavy_stroke_width,
        )
        self.play(GrowArrow(b1), GrowArrow(b2))

        dep_note = MathTex(
            r"\vec{b}_2 = 3 \, \vec{b}_1",
            font_size=t.body_size, color=t.accent,
        )
        dep_note.next_to(axes_r, DOWN, buff=0.3)
        self.play(Write(dep_note))

        # Highlight the redundancy
        box = SurroundingRectangle(dep_note, color=t.accent, buff=0.15)
        redundant = Text(
            "One vector is redundant!",
            font_size=t.label_size, color=t.accent,
        )
        redundant.to_edge(DOWN)
        self.play(Create(box), Write(redundant))

        # Divider
        divider = DashedLine(
            UP * 2, DOWN * 3.5,
            color=t.muted, stroke_width=t.fine_stroke_width,
        )
        self.play(Create(divider))
        self.wait(2)


# ---------------------------------------------------------------------------
# Scene 7: Basis vectors span all of R^2
# ---------------------------------------------------------------------------

class SpanAndBasis(ThemedScene):
    """
    Show that the standard basis {e1, e2} spans all of R^2.
    Any vector (a, b) = a*e1 + b*e2.
    Then show a non-standard basis doing the same.
    """

    def construct(self):
        t = self.theme

        title = Text("Basis Spans the Space", font_size=t.title_size, color=t.foreground)
        title.to_edge(UP)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-4, 5, 1], y_range=[-3, 4, 1],
            background_line_style={"stroke_opacity": 0.15, "stroke_color": t.muted},
            axis_config={"color": t.muted, "stroke_width": t.axis_stroke_width},
        ).shift(DOWN * 0.3)
        self.play(Create(plane), run_time=0.6)

        # Standard basis
        e1 = Arrow(ORIGIN, RIGHT, buff=0, color=t.primary, stroke_width=t.heavy_stroke_width)
        e2 = Arrow(ORIGIN, UP, buff=0, color=t.secondary, stroke_width=t.heavy_stroke_width)
        e1_l = MathTex(r"\hat{e}_1", font_size=t.body_size, color=t.primary)
        e1_l.next_to(e1.get_end(), DOWN, buff=0.1)
        e2_l = MathTex(r"\hat{e}_2", font_size=t.body_size, color=t.secondary)
        e2_l.next_to(e2.get_end(), LEFT, buff=0.1)

        self.play(GrowArrow(e1), GrowArrow(e2), Write(e1_l), Write(e2_l))
        self.wait(0.5)

        # Target vector (3, 2)
        target_coords = np.array([3, 2, 0])
        target = Arrow(
            ORIGIN, target_coords, buff=0,
            color=t.accent, stroke_width=t.heavy_stroke_width,
        )
        target_label = MathTex(
            r"\begin{bmatrix} 3 \\ 2 \end{bmatrix}",
            font_size=t.body_size, color=t.accent,
        ).next_to(target.get_end(), RIGHT, buff=0.15)
        self.play(GrowArrow(target), Write(target_label))
        self.wait(0.3)

        # Decompose: 3 * e1
        scaled_e1 = Arrow(
            ORIGIN, RIGHT * 3, buff=0,
            color=t.primary, stroke_width=t.curve_stroke_width,
        )
        se1_label = MathTex(r"3\hat{e}_1", font_size=t.label_size, color=t.primary)
        se1_label.next_to(scaled_e1.get_center(), DOWN, buff=0.15)

        self.play(Transform(e1, scaled_e1), FadeOut(e1_l), Write(se1_label))

        # 2 * e2 shifted
        shifted_e2 = Arrow(
            RIGHT * 3, RIGHT * 3 + UP * 2, buff=0,
            color=t.secondary, stroke_width=t.curve_stroke_width,
        )
        se2_label = MathTex(r"2\hat{e}_2", font_size=t.label_size, color=t.secondary)
        se2_label.next_to(shifted_e2.get_center(), RIGHT, buff=0.15)

        self.play(Transform(e2, shifted_e2), FadeOut(e2_l), Write(se2_label))

        # Equation
        decomp = MathTex(
            r"\begin{bmatrix} 3 \\ 2 \end{bmatrix} = 3\hat{e}_1 + 2\hat{e}_2",
            font_size=t.body_size, color=t.foreground,
        )
        decomp.to_edge(DOWN)
        self.play(Write(decomp))

        subtitle = Text(
            "Every vector = a unique combination of basis vectors",
            font_size=t.label_size, color=t.accent,
        )
        subtitle.next_to(decomp, UP, buff=0.2)
        self.play(Write(subtitle))
        self.wait(2)
