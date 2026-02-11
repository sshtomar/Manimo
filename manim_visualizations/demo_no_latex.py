"""
Demo visualization without LaTeX dependency
Shows 3b1b principles in action
"""

from manim import (
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
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    np,
    linear,
    smooth,
)

from themed_scene import ThemedScene


class TangentLineDemo(ThemedScene):
    """
    Demonstrate tangent line moving along a curve.
    Shows: geometry first, progressive disclosure, synchronized updates.
    """

    def construct(self):
        t = self.theme

        # =====================================================================
        # PHASE 1: SETUP - Geometry first (no labels yet)
        # =====================================================================
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 10, 2],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True, "include_numbers": False},
        )
        axes.shift(DOWN * 0.5)

        # Show axes
        self.play(Create(axes), run_time=1)
        self.wait(0.5)

        # Function
        func = lambda x: x**2
        derivative = lambda x: 2 * x

        graph = axes.plot(func, x_range=[-2.5, 2.5], color=t.primary, stroke_width=t.curve_stroke_width)

        # Show curve first (geometry before symbols)
        self.play(Create(graph), run_time=2)
        self.wait(1)

        # =====================================================================
        # PHASE 2: INTRODUCE tangent line (visual before formula)
        # =====================================================================
        x_tracker = ValueTracker(1.0)

        # Point on curve
        point = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(), func(x_tracker.get_value())),
            color=t.accent,
            radius=0.12
        ))

        # Tangent line
        def get_tangent():
            x = x_tracker.get_value()
            slope = derivative(x)
            y = func(x)
            ext = 1.5
            start = axes.c2p(x - ext, y - slope * ext)
            end = axes.c2p(x + ext, y + slope * ext)
            return Line(start, end, color=t.secondary, stroke_width=t.curve_stroke_width)

        tangent = always_redraw(get_tangent)

        self.play(FadeIn(point, scale=0.5))
        self.wait(0.3)
        self.play(Create(tangent))
        self.wait(1)

        # =====================================================================
        # PHASE 3: ADD LABELS (symbols after geometry)
        # =====================================================================
        func_label = Text("f(x) = x²", font_size=t.body_size, color=t.primary)
        func_label.to_corner(UP + LEFT).shift(DOWN * 0.3)

        self.play(Write(func_label))

        # Slope display
        slope_display = always_redraw(lambda: VGroup(
            Text(f"x = {x_tracker.get_value():.1f}", font_size=t.label_size, color=t.accent),
            Text(f"slope = {derivative(x_tracker.get_value()):.1f}", font_size=t.label_size, color=t.secondary),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UP + RIGHT))

        self.play(Write(slope_display))
        self.wait(1)

        # =====================================================================
        # PHASE 4: ANIMATE - Show how tangent changes
        # =====================================================================
        self.play(x_tracker.animate.set_value(2.5), run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(x_tracker.animate.set_value(0), run_time=2, rate_func=smooth)
        self.wait(0.5)
        self.play(x_tracker.animate.set_value(-2), run_time=2, rate_func=smooth)
        self.wait(0.5)

        # =====================================================================
        # PHASE 5: KEY INSIGHT
        # =====================================================================
        insight = Text("Tangent line slope = derivative", font_size=t.body_size, color=t.accent)
        insight.to_edge(UP)

        box = SurroundingRectangle(insight, color=t.accent, buff=0.15)
        self.play(Write(insight), Create(box))
        self.wait(2)


class AreaUnderCurveDemo(ThemedScene):
    """
    Demonstrate area under a curve with Riemann sum approximation.
    Progressive: few rectangles -> many rectangles -> smooth area.
    """

    def construct(self):
        t = self.theme

        # =====================================================================
        # PHASE 1: SETUP
        # =====================================================================
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 6, 1],
            x_length=9,
            y_length=4.5,
            axis_config={"include_tip": True, "include_numbers": False},
        )
        axes.shift(DOWN * 0.8)

        self.play(Create(axes), run_time=1)
        self.wait(0.5)

        # Function
        func = lambda x: 0.3 * x**2 + 0.5
        graph = axes.plot(func, x_range=[0.3, 4.5], color=t.primary, stroke_width=t.curve_stroke_width)

        self.play(Create(graph), run_time=1.5)
        self.wait(0.5)

        # Label
        func_text = Text("f(x) = 0.3x² + 0.5", font_size=t.label_size, color=t.primary)
        func_text.next_to(graph.get_end(), RIGHT)
        self.play(Write(func_text))
        self.wait(0.5)

        # =====================================================================
        # PHASE 2: SHOW RIEMANN RECTANGLES - Progressive refinement
        # =====================================================================
        a, b = 1, 4

        # Bound lines
        bound_a = DashedLine(axes.c2p(a, 0), axes.c2p(a, func(a)), color=t.accent, stroke_width=t.axis_stroke_width)
        bound_b = DashedLine(axes.c2p(b, 0), axes.c2p(b, func(b)), color=t.accent, stroke_width=t.axis_stroke_width)

        self.play(Create(bound_a), Create(bound_b))
        self.wait(0.5)

        # Progressive rectangle refinement
        n_values = [4, 8, 16, 32, 64]

        n_label = Text(f"n = {n_values[0]} rectangles", font_size=t.label_size)
        n_label.to_corner(UP + RIGHT)

        rects = axes.get_riemann_rectangles(
            graph, x_range=[a, b], dx=(b - a) / n_values[0],
            color=[t.primary, t.tertiary],
            fill_opacity=t.area_fill_opacity,
            stroke_width=t.fine_stroke_width,
            stroke_color=t.foreground,
        )

        self.play(
            LaggedStartMap(Create, rects, lag_ratio=0.15),
            Write(n_label),
            run_time=2,
        )
        self.wait(1)

        for n in n_values[1:]:
            new_rects = axes.get_riemann_rectangles(
                graph, x_range=[a, b], dx=(b - a) / n,
                color=[t.primary, t.tertiary],
                fill_opacity=t.area_fill_opacity,
                stroke_width=0.5 if n > 16 else t.fine_stroke_width,
                stroke_color=t.foreground,
            )
            new_label = Text(f"n = {n} rectangles", font_size=t.label_size)
            new_label.to_corner(UP + RIGHT)

            self.play(
                Transform(rects, new_rects),
                Transform(n_label, new_label),
                run_time=1.5,
            )
            self.wait(0.5)

        # =====================================================================
        # PHASE 3: SMOOTH AREA
        # =====================================================================
        area = axes.get_area(graph, x_range=[a, b], color=t.tertiary, opacity=0.7)

        self.play(
            Transform(rects, area),
            FadeOut(n_label),
            run_time=1.5,
        )

        # Final text
        result = Text("Area under the curve = integral!", font_size=t.body_size, color=t.accent)
        result.to_edge(UP)
        box = SurroundingRectangle(result, color=t.accent, buff=0.1)
        self.play(Write(result), Create(box))
        self.wait(2)


class CircleAreaDemo(ThemedScene):
    """
    Approximate circle area with inscribed polygons.
    Shows: building suspense, LaggedStart, progressive disclosure.
    """

    def construct(self):
        t = self.theme

        title = Text("Area of a Circle", font_size=t.subtitle_size)
        title.to_edge(UP)
        self.play(Write(title))

        circle = Circle(radius=2, color=t.primary, stroke_width=t.curve_stroke_width)
        self.play(Create(circle))
        self.wait(0.5)

        # Progressive polygon approximation
        n_sides_list = [3, 4, 6, 8, 12, 24, 48]

        from manim import RegularPolygon

        # First polygon
        poly = RegularPolygon(n=3, color=t.accent, fill_opacity=t.shape_fill_opacity)
        poly.scale(2)  # Match circle radius

        n_display = Text(f"n = 3 sides", font_size=t.label_size)
        n_display.to_corner(UP + RIGHT)

        self.play(Create(poly), Write(n_display))
        self.wait(0.5)

        for n in n_sides_list[1:]:
            new_poly = RegularPolygon(n=n, color=t.accent, fill_opacity=t.shape_fill_opacity)
            new_poly.scale(2)

            new_display = Text(f"n = {n} sides", font_size=t.label_size)
            new_display.to_corner(UP + RIGHT)

            self.play(
                Transform(poly, new_poly),
                Transform(n_display, new_display),
                run_time=1,
            )
            self.wait(0.3)

        # Fill the circle
        filled = Circle(radius=2, color=t.tertiary, fill_opacity=t.area_fill_opacity, stroke_width=t.curve_stroke_width)
        self.play(Transform(poly, filled), run_time=1.5)

        # Formula
        formula = Text("A = pi * r²", font_size=t.subtitle_size, color=t.accent)
        formula.to_edge(DOWN)
        box = SurroundingRectangle(formula, color=t.accent, buff=0.15)
        self.play(Write(formula), Create(box))
        self.wait(2)
