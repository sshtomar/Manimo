"""
Demo visualization without LaTeX dependency
Shows 3b1b principles in action
"""

from manim import (
    Scene,
    VGroup,
    Axes,
    Text,
    Dot,
    Line,
    DashedLine,
    Circle,
    Square,
    Create,
    Write,
    FadeIn,
    FadeOut,
    Transform,
    LaggedStart,
    LaggedStartMap,
    ValueTracker,
    always_redraw,
    SurroundingRectangle,
    BLUE,
    RED,
    GREEN,
    GREEN_D,
    YELLOW,
    ORANGE,
    WHITE,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    np,
    linear,
    smooth,
)

# Consistent color palette
FUNC_COLOR = BLUE
DERIV_COLOR = RED
X_COLOR = YELLOW
AREA_COLOR = GREEN_D
HIGHLIGHT_COLOR = YELLOW


class TangentLineDemo(Scene):
    """
    Demonstrate tangent line moving along a curve.
    Shows: geometry first, progressive disclosure, synchronized updates.
    """

    def construct(self):
        # =====================================================================
        # PHASE 1: SETUP - Geometry first (no labels yet)
        # =====================================================================
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 10, 2],
            x_length=7,
            y_length=5,
            axis_config={"include_tip": True},
        )
        axes.shift(DOWN * 0.5 + LEFT * 1)

        self.play(Create(axes), run_time=1)
        self.wait(0.5)

        # Function: f(x) = x^2
        func = lambda x: x**2
        derivative = lambda x: 2 * x

        graph = axes.plot(func, x_range=[-0.5, 3.2], color=FUNC_COLOR, stroke_width=3)

        # Show the curve first - let viewers see it
        self.play(Create(graph), run_time=2)
        self.wait(1)  # Strategic pause

        # =====================================================================
        # PHASE 2: INTRODUCE TANGENT - Visual before explanation
        # =====================================================================
        x_tracker = ValueTracker(1.0)

        # Point on curve (prominent)
        point = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(), func(x_tracker.get_value())),
            color=X_COLOR,
            radius=0.12
        ))

        # Tangent line that follows
        def get_tangent_line():
            x = x_tracker.get_value()
            slope = derivative(x)
            y = func(x)
            x_extent = 1.5
            start = axes.c2p(x - x_extent, y - slope * x_extent)
            end = axes.c2p(x + x_extent, y + slope * x_extent)
            return Line(start, end, color=DERIV_COLOR, stroke_width=3)

        tangent = always_redraw(get_tangent_line)

        # Progressive disclosure: point first, then tangent
        self.play(FadeIn(point, scale=0.5))
        self.wait(0.5)
        self.play(Create(tangent))
        self.wait(1)

        # =====================================================================
        # PHASE 3: ADD SYNCHRONIZED DISPLAY
        # =====================================================================
        slope_display = always_redraw(lambda: VGroup(
            Text(f"x = {x_tracker.get_value():.1f}", font_size=24, color=X_COLOR),
            Text(f"slope = {derivative(x_tracker.get_value()):.1f}", font_size=24, color=DERIV_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UP + RIGHT))

        self.play(Write(slope_display))
        self.wait(1)

        # =====================================================================
        # PHASE 4: ANIMATE - Strategic movements with pauses
        # =====================================================================
        movements = [
            (2.0, 2.5),   # Move to x=2
            (0.5, 2),     # Move to x=0.5 (small slope)
            (0.0, 1.5),   # Move to x=0 (slope = 0!)
            (2.5, 2),     # Move back up
        ]

        for target_x, duration in movements:
            self.play(
                x_tracker.animate.set_value(target_x),
                run_time=duration,
                rate_func=smooth
            )
            self.wait(1)  # Pause at each key point

        # =====================================================================
        # PHASE 5: RESOLUTION
        # =====================================================================
        title = Text("Derivative = Slope of Tangent", font_size=28, color=HIGHLIGHT_COLOR)
        title.to_edge(UP)

        box = SurroundingRectangle(title, color=HIGHLIGHT_COLOR, buff=0.15)

        self.play(Write(title))
        self.play(Create(box))
        self.wait(2)


class RiemannSumsDemo(Scene):
    """
    Riemann sums approaching integral.
    Shows: LaggedStart rhythm, building suspense, geometry before symbols.
    """

    def construct(self):
        # =====================================================================
        # PHASE 1: SETUP
        # =====================================================================
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 8, 2],
            x_length=9,
            y_length=4.5,
            axis_config={"include_tip": True},
        )
        axes.shift(DOWN * 0.8)

        self.play(Create(axes), run_time=1)

        # Function
        func = lambda x: 0.5 * x**2 - x + 4
        graph = axes.plot(func, x_range=[0.5, 4.5], color=FUNC_COLOR, stroke_width=3)

        self.play(Create(graph), run_time=1.5)
        self.wait(0.5)

        # =====================================================================
        # PHASE 2: ESTABLISH BOUNDS
        # =====================================================================
        a, b = 1, 4

        bound_a = DashedLine(
            axes.c2p(a, 0), axes.c2p(a, func(a)),
            color=X_COLOR, stroke_width=2
        )
        bound_b = DashedLine(
            axes.c2p(b, 0), axes.c2p(b, func(b)),
            color=X_COLOR, stroke_width=2
        )

        self.play(Create(bound_a), Create(bound_b))
        self.wait(1)

        # Pose the question
        question = Text("What is the area?", font_size=28)
        question.to_edge(UP)
        self.play(Write(question))
        self.wait(1)

        # =====================================================================
        # PHASE 3: BUILD WITH LAGGED START RHYTHM
        # =====================================================================
        n_values = [4, 8, 16, 32]

        # First set - use LaggedStartMap for 3b1b rhythm
        rects = axes.get_riemann_rectangles(
            graph,
            x_range=[a, b],
            dx=(b - a) / 4,
            color=[FUNC_COLOR, AREA_COLOR],
            fill_opacity=0.6,
            stroke_width=1,
            stroke_color=WHITE,
        )

        n_label = Text("n = 4", font_size=28, color=HIGHLIGHT_COLOR).to_corner(UP + RIGHT)

        # Staggered creation (key 3b1b rhythm pattern)
        self.play(
            LaggedStartMap(Create, rects, lag_ratio=0.15),
            Write(n_label),
            run_time=2
        )
        self.wait(1)

        # Transform through increasing n
        for n in n_values[1:]:
            new_rects = axes.get_riemann_rectangles(
                graph,
                x_range=[a, b],
                dx=(b - a) / n,
                color=[FUNC_COLOR, AREA_COLOR],
                fill_opacity=0.6,
                stroke_width=0.5 if n > 16 else 1,
                stroke_color=WHITE,
            )

            new_label = Text(f"n = {n}", font_size=28, color=HIGHLIGHT_COLOR).to_corner(UP + RIGHT)

            # Building suspense - slower for larger n
            duration = 1.0 if n <= 16 else 1.5

            self.play(
                Transform(rects, new_rects),
                Transform(n_label, new_label),
                run_time=duration,
            )
            self.wait(0.75)

        # =====================================================================
        # PHASE 4: RESOLUTION
        # =====================================================================

        # Transform rectangles into smooth area
        area = axes.get_area(graph, x_range=[a, b], color=AREA_COLOR, opacity=0.7)

        self.play(
            Transform(rects, area),
            FadeOut(n_label),
            run_time=1.5
        )
        self.wait(0.5)

        # Final reveal
        self.play(FadeOut(question))

        result = Text("Exact Area (the integral)", font_size=28, color=AREA_COLOR)
        result.to_edge(UP)

        box = SurroundingRectangle(result, color=HIGHLIGHT_COLOR, buff=0.1)

        self.play(Write(result))
        self.play(Create(box))
        self.wait(2)


class DualSpaceDemo(Scene):
    """
    Synchronized dual-space visualization.
    Shows: multiple representations updating together.
    """

    def construct(self):
        # =====================================================================
        # PHASE 1: SETUP - Two graphs side by side
        # =====================================================================

        # Left: f(x) = 2x
        axes_left = Axes(
            x_range=[0, 4, 1],
            y_range=[-1, 8, 2],
            x_length=5,
            y_length=4,
            axis_config={"include_tip": True},
        )
        axes_left.shift(LEFT * 3.5 + DOWN * 0.3)

        # Right: F(x) = x^2
        axes_right = Axes(
            x_range=[0, 4, 1],
            y_range=[-1, 10, 2],
            x_length=5,
            y_length=4,
            axis_config={"include_tip": True},
        )
        axes_right.shift(RIGHT * 3.5 + DOWN * 0.3)

        # Staggered creation
        self.play(Create(axes_left), run_time=1)
        self.play(Create(axes_right), run_time=1)
        self.wait(0.5)

        # =====================================================================
        # PHASE 2: BUILD SYNCHRONIZED RELATIONSHIP
        # =====================================================================

        # Shared tracker
        x_tracker = ValueTracker(0.5)

        # Left: f(x) = 2x with growing area
        f_graph = axes_left.plot(lambda x: 2 * x, x_range=[0, 3.5], color=FUNC_COLOR)

        area = always_redraw(lambda: axes_left.get_area(
            f_graph,
            x_range=[0, x_tracker.get_value()],
            color=AREA_COLOR,
            opacity=0.5
        ))

        f_line = always_redraw(lambda: DashedLine(
            axes_left.c2p(x_tracker.get_value(), 0),
            axes_left.c2p(x_tracker.get_value(), 2 * x_tracker.get_value()),
            color=X_COLOR
        ))

        # Right: F(x) = x^2, point tracking area
        F_graph = axes_right.plot(lambda x: x**2, x_range=[0, 3.2], color=GREEN)

        F_point = always_redraw(lambda: Dot(
            axes_right.c2p(x_tracker.get_value(), x_tracker.get_value()**2),
            color=GREEN,
            radius=0.12
        ))

        F_line = always_redraw(lambda: DashedLine(
            axes_right.c2p(x_tracker.get_value(), 0),
            axes_right.c2p(x_tracker.get_value(), x_tracker.get_value()**2),
            color=X_COLOR
        ))

        # Labels
        label_left = Text("f(x) = 2x", font_size=24, color=FUNC_COLOR)
        label_left.next_to(axes_left, UP)

        label_right = Text("F(x) = x² (area)", font_size=24, color=GREEN)
        label_right.next_to(axes_right, UP)

        # Progressive disclosure
        self.play(Create(f_graph), Write(label_left))
        self.wait(0.5)

        self.play(FadeIn(area), Create(f_line))
        self.wait(1)

        self.play(Create(F_graph), Write(label_right))
        self.play(FadeIn(F_point), Create(F_line))
        self.wait(1)

        # =====================================================================
        # PHASE 3: ANIMATE SYNCHRONIZED UPDATE
        # =====================================================================

        # Value display
        value_display = always_redraw(lambda: VGroup(
            Text(f"x = {x_tracker.get_value():.1f}", font_size=22, color=X_COLOR),
            Text(f"Area = {x_tracker.get_value()**2:.2f}", font_size=22, color=AREA_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UP + RIGHT))

        self.play(Write(value_display))
        self.wait(0.5)

        # Watch both spaces update together
        self.play(x_tracker.animate.set_value(2.5), run_time=4, rate_func=smooth)
        self.wait(1)
        self.play(x_tracker.animate.set_value(1.0), run_time=2)
        self.wait(1)
        self.play(x_tracker.animate.set_value(3.0), run_time=2)
        self.wait(2)
