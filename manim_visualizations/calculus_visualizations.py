"""
Calculus Visualizations - Functions, Derivatives, and Integrals
Animated mathematical intuition for calculus concepts
"""

from manim import (
    Scene,
    VGroup,
    Axes,
    Text,
    MathTex,
    Dot,
    Line,
    DashedLine,
    TangentLine,
    Create,
    Write,
    FadeIn,
    FadeOut,
    Transform,
    ReplacementTransform,
    MoveAlongPath,
    Indicate,
    AnimationGroup,
    Succession,
    ValueTracker,
    always_redraw,
    BLUE,
    RED,
    GREEN,
    YELLOW,
    ORANGE,
    PURPLE,
    WHITE,
    GREY,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    UR,
    UL,
    DR,
    DL,
    ORIGIN,
    PI,
    np,
    rate_functions,
)


class FunctionPlotAnimation(Scene):
    """
    Animate how a function is plotted over time.
    Shows the function being drawn progressively.
    """

    def construct(self):
        # Title
        title = Text("Plotting a Function", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 10, 2],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True, "include_numbers": True},
        )
        axes.shift(DOWN * 0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        self.play(Create(axes), Write(labels))

        # Function: f(x) = x^2
        func_label = MathTex(r"f(x) = x^2", font_size=32, color=BLUE)
        func_label.to_corner(UR)
        self.play(Write(func_label))

        # Plot the function with animation
        graph = axes.plot(lambda x: x**2, x_range=[-3, 3], color=BLUE)
        self.play(Create(graph), run_time=3)

        # Add a moving dot that traces the function
        dot = Dot(color=YELLOW)
        dot.move_to(axes.c2p(-3, 9))

        self.play(FadeIn(dot))
        self.play(MoveAlongPath(dot, graph), run_time=2)
        self.play(FadeOut(dot))

        self.wait(1)

        # Transform to another function
        new_label = MathTex(r"g(x) = \sin(x) + 3", font_size=32, color=GREEN)
        new_label.to_corner(UR)

        new_graph = axes.plot(
            lambda x: np.sin(x) + 3, x_range=[-3, 3], color=GREEN
        )

        self.play(
            Transform(graph, new_graph), Transform(func_label, new_label), run_time=2
        )
        self.wait(2)


class TangentLineDerivative(Scene):
    """
    Animate tangent lines moving along a curve to explain derivatives.
    Shows the relationship between slope and derivative value.
    """

    def construct(self):
        title = Text("Derivative = Slope of Tangent Line", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Create axes
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 10, 2],
            x_length=7,
            y_length=5,
            axis_config={"include_tip": True},
        )
        axes.shift(DOWN * 0.5 + LEFT * 1)
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        self.play(Create(axes), Write(labels))

        # Function
        func = lambda x: x**2
        derivative = lambda x: 2 * x

        graph = axes.plot(func, x_range=[-0.5, 3.2], color=BLUE, stroke_width=3)
        func_label = MathTex(r"f(x) = x^2", font_size=28, color=BLUE)
        func_label.next_to(graph, UR, buff=0.2)

        self.play(Create(graph), Write(func_label))
        self.wait(1)

        # Value tracker for x position
        x_tracker = ValueTracker(0.5)

        # Tangent line and point that update with tracker
        def get_tangent():
            x = x_tracker.get_value()
            return axes.get_secant_slope_group(
                x=x,
                graph=graph,
                dx=0.01,
                secant_line_length=3,
                secant_line_color=RED,
            )

        def get_point():
            x = x_tracker.get_value()
            return Dot(axes.c2p(x, func(x)), color=YELLOW, radius=0.1)

        tangent = always_redraw(get_tangent)
        point = always_redraw(get_point)

        # Derivative value display
        deriv_text = always_redraw(
            lambda: MathTex(
                rf"f'({x_tracker.get_value():.1f}) = {derivative(x_tracker.get_value()):.2f}",
                font_size=28,
                color=RED,
            ).to_corner(UR)
        )

        slope_text = always_redraw(
            lambda: Text(
                f"Slope = {derivative(x_tracker.get_value()):.2f}",
                font_size=24,
                color=YELLOW,
            ).next_to(deriv_text, DOWN)
        )

        self.play(Create(point), Create(tangent))
        self.play(Write(deriv_text), Write(slope_text))
        self.wait(1)

        # Animate the point moving along the curve
        self.play(x_tracker.animate.set_value(2.5), run_time=4, rate_func=rate_functions.smooth)
        self.wait(1)
        self.play(x_tracker.animate.set_value(1), run_time=2)
        self.wait(1)
        self.play(x_tracker.animate.set_value(3), run_time=2)
        self.wait(2)


class SecantToTangent(Scene):
    """
    Show how secant lines approach tangent as dx -> 0.
    Core idea of the derivative definition.
    """

    def construct(self):
        title = Text("Secant Lines → Tangent Line", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Create axes
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 10, 2],
            x_length=6,
            y_length=5,
            axis_config={"include_tip": True},
        )
        axes.shift(LEFT * 2 + DOWN * 0.5)

        self.play(Create(axes))

        # Function
        func = lambda x: x**2
        graph = axes.plot(func, x_range=[0.5, 3.2], color=BLUE, stroke_width=3)
        self.play(Create(graph))

        # Fixed point
        x0 = 1.5
        point_a = Dot(axes.c2p(x0, func(x0)), color=YELLOW, radius=0.08)
        label_a = MathTex("a", font_size=24).next_to(point_a, DOWN)

        self.play(FadeIn(point_a), Write(label_a))

        # Show secant lines with decreasing dx
        dx_values = [1.5, 1.0, 0.5, 0.2, 0.05]

        formula = MathTex(
            r"\text{Slope} = \frac{f(a+h) - f(a)}{h}", font_size=28
        )
        formula.to_corner(UR)
        self.play(Write(formula))

        secant_line = None
        point_b = None
        h_text = None

        for dx in dx_values:
            x1 = x0 + dx
            y0, y1 = func(x0), func(x1)
            slope = (y1 - y0) / dx

            # Create new secant line
            new_point_b = Dot(axes.c2p(x1, y1), color=GREEN, radius=0.08)

            # Line extending beyond points
            start = axes.c2p(x0 - 0.5, y0 - 0.5 * slope)
            end = axes.c2p(x1 + 0.5, y1 + 0.5 * slope)
            new_line = Line(start, end, color=RED, stroke_width=3)

            new_h_text = MathTex(f"h = {dx}", font_size=24, color=ORANGE)
            new_h_text.next_to(formula, DOWN, buff=0.5)

            slope_val = MathTex(f"\\text{{slope}} = {slope:.2f}", font_size=24, color=RED)
            slope_val.next_to(new_h_text, DOWN)

            if secant_line is None:
                self.play(FadeIn(new_point_b), Create(new_line), Write(new_h_text))
                self.play(Write(slope_val))
                secant_line = new_line
                point_b = new_point_b
                h_text = VGroup(new_h_text, slope_val)
            else:
                self.play(
                    Transform(secant_line, new_line),
                    Transform(point_b, new_point_b),
                    Transform(h_text, VGroup(new_h_text, slope_val)),
                    run_time=0.8,
                )

            self.wait(0.5)

        # Final message
        limit_text = MathTex(
            r"\lim_{h \to 0} \frac{f(a+h) - f(a)}{h} = f'(a)",
            font_size=28,
            color=YELLOW,
        )
        limit_text.to_edge(DOWN)
        self.play(Write(limit_text))
        self.wait(2)


class RiemannSumsToIntegral(Scene):
    """
    Animate Riemann sums becoming the definite integral.
    Shows rectangles getting thinner and area becoming exact.
    """

    def construct(self):
        title = Text("Riemann Sums → Definite Integral", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Create axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 8, 2],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": True},
        )
        axes.shift(DOWN * 1)

        self.play(Create(axes))

        # Function
        func = lambda x: 0.5 * x**2 - x + 4
        graph = axes.plot(func, x_range=[0.5, 4.5], color=BLUE, stroke_width=3)
        func_label = MathTex(r"f(x)", font_size=24, color=BLUE)
        func_label.next_to(graph.get_end(), RIGHT)

        self.play(Create(graph), Write(func_label))
        self.wait(1)

        # Integration bounds
        a, b = 1, 4
        bound_a = DashedLine(
            axes.c2p(a, 0), axes.c2p(a, func(a)), color=WHITE, stroke_width=2
        )
        bound_b = DashedLine(
            axes.c2p(b, 0), axes.c2p(b, func(b)), color=WHITE, stroke_width=2
        )
        self.play(Create(bound_a), Create(bound_b))

        # Show increasing number of rectangles
        n_values = [4, 8, 16, 32, 64]

        n_text = None
        riemann_rects = None

        for n in n_values:
            rects = axes.get_riemann_rectangles(
                graph,
                x_range=[a, b],
                dx=(b - a) / n,
                color=[BLUE, GREEN],
                fill_opacity=0.5,
                stroke_width=0.5,
            )

            new_n_text = MathTex(f"n = {n}", font_size=28, color=YELLOW)
            new_n_text.to_corner(UR)

            if riemann_rects is None:
                self.play(Create(rects), Write(new_n_text))
                riemann_rects = rects
                n_text = new_n_text
            else:
                self.play(
                    Transform(riemann_rects, rects),
                    Transform(n_text, new_n_text),
                    run_time=1,
                )

            self.wait(0.5)

        # Show the integral notation
        integral = MathTex(
            r"\int_1^4 f(x) \, dx = \text{Exact Area}",
            font_size=32,
            color=YELLOW,
        )
        integral.to_edge(DOWN)
        self.play(Write(integral))

        # Transform rectangles into area under curve
        area = axes.get_area(graph, x_range=[a, b], color=[BLUE, GREEN], opacity=0.7)
        self.play(Transform(riemann_rects, area), run_time=1.5)
        self.wait(2)


class DerivativeIntegralRelation(Scene):
    """
    Visualize the Fundamental Theorem of Calculus.
    Show that integration and differentiation are inverse operations.
    """

    def construct(self):
        title = Text("Fundamental Theorem of Calculus", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Create two sets of axes side by side
        axes_left = Axes(
            x_range=[0, 4, 1],
            y_range=[-1, 5, 1],
            x_length=5,
            y_length=4,
            axis_config={"include_tip": True},
        )
        axes_left.shift(LEFT * 3.5 + DOWN * 0.5)

        axes_right = Axes(
            x_range=[0, 4, 1],
            y_range=[-2, 10, 2],
            x_length=5,
            y_length=4,
            axis_config={"include_tip": True},
        )
        axes_right.shift(RIGHT * 3.5 + DOWN * 0.5)

        label_left = Text("f(x) = 2x", font_size=24, color=BLUE)
        label_left.next_to(axes_left, UP)

        label_right = Text("F(x) = x² (antiderivative)", font_size=24, color=GREEN)
        label_right.next_to(axes_right, UP)

        self.play(Create(axes_left), Create(axes_right))
        self.play(Write(label_left), Write(label_right))

        # Plot f(x) = 2x
        f_graph = axes_left.plot(lambda x: 2 * x, x_range=[0, 3.5], color=BLUE)
        self.play(Create(f_graph))

        # Plot F(x) = x^2
        F_graph = axes_right.plot(lambda x: x**2, x_range=[0, 3.2], color=GREEN)
        self.play(Create(F_graph))

        self.wait(1)

        # Show the relationship
        relation1 = MathTex(
            r"\frac{d}{dx}[x^2] = 2x", font_size=28, color=YELLOW
        )
        relation1.shift(DOWN * 2.8 + LEFT * 2)

        relation2 = MathTex(
            r"\int 2x \, dx = x^2 + C", font_size=28, color=ORANGE
        )
        relation2.shift(DOWN * 2.8 + RIGHT * 2)

        self.play(Write(relation1), Write(relation2))

        # Arrow showing the inverse relationship
        arrow_top = MathTex(r"\xrightarrow{\text{derivative}}", font_size=24)
        arrow_top.move_to(UP * 1.5)

        arrow_bottom = MathTex(r"\xleftarrow{\text{integral}}", font_size=24)
        arrow_bottom.move_to(UP * 0.8)

        self.play(Write(arrow_top), Write(arrow_bottom))
        self.wait(2)


class AreaAccumulation(Scene):
    """
    Show how the integral F(x) represents accumulated area.
    """

    def construct(self):
        title = Text("Integral as Accumulated Area", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 6, 1],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": True},
        )
        axes.shift(DOWN * 1)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        self.play(Create(axes), Write(labels))

        # Function
        func = lambda x: 0.3 * x**2 + 0.5
        graph = axes.plot(func, x_range=[0.5, 4.5], color=BLUE, stroke_width=3)
        self.play(Create(graph))

        # Value tracker for x
        x_tracker = ValueTracker(0.5)

        # Area that grows with x
        def get_area():
            return axes.get_area(
                graph,
                x_range=[0.5, x_tracker.get_value()],
                color=GREEN,
                opacity=0.5,
            )

        area = always_redraw(get_area)

        # Moving vertical line
        def get_line():
            x = x_tracker.get_value()
            return DashedLine(
                axes.c2p(x, 0),
                axes.c2p(x, func(x)),
                color=YELLOW,
                stroke_width=2,
            )

        line = always_redraw(get_line)

        # Area value display
        def get_area_value():
            x = x_tracker.get_value()
            # Approximate integral value
            area_val = (0.3 / 3 * x**3 + 0.5 * x) - (0.3 / 3 * 0.5**3 + 0.5 * 0.5)
            text = MathTex(
                rf"F({x:.1f}) = \int_{{0.5}}^{{{x:.1f}}} f(t) \, dt \approx {area_val:.2f}",
                font_size=24,
            )
            text.to_corner(UR)
            return text

        area_text = always_redraw(get_area_value)

        self.play(FadeIn(area), Create(line), Write(area_text))

        # Animate x growing
        self.play(x_tracker.animate.set_value(4), run_time=5, rate_func=rate_functions.smooth)
        self.wait(2)


class PowerRuleDerivative(Scene):
    """
    Visualize the power rule for derivatives.
    """

    def construct(self):
        title = Text("Power Rule: d/dx[xⁿ] = nxⁿ⁻¹", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Create axes
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True},
        )
        axes.shift(DOWN * 0.5)

        self.play(Create(axes))

        # Show x^2 and its derivative
        func_x2 = axes.plot(lambda x: x**2, x_range=[-2, 2], color=BLUE)
        deriv_2x = axes.plot(lambda x: 2 * x, x_range=[-2, 2], color=RED)

        label_x2 = MathTex(r"f(x) = x^2", font_size=24, color=BLUE)
        label_x2.to_corner(UL).shift(DOWN * 0.5)

        label_2x = MathTex(r"f'(x) = 2x", font_size=24, color=RED)
        label_2x.next_to(label_x2, DOWN)

        self.play(Create(func_x2), Write(label_x2))
        self.wait(1)
        self.play(Create(deriv_2x), Write(label_2x))
        self.wait(1)

        # Transform to x^3
        func_x3 = axes.plot(lambda x: x**3, x_range=[-1.5, 1.5], color=BLUE)
        deriv_3x2 = axes.plot(lambda x: 3 * x**2, x_range=[-1.5, 1.5], color=RED)

        new_label_x3 = MathTex(r"f(x) = x^3", font_size=24, color=BLUE)
        new_label_x3.to_corner(UL).shift(DOWN * 0.5)

        new_label_3x2 = MathTex(r"f'(x) = 3x^2", font_size=24, color=RED)
        new_label_3x2.next_to(new_label_x3, DOWN)

        self.play(
            Transform(func_x2, func_x3),
            Transform(deriv_2x, deriv_3x2),
            Transform(label_x2, new_label_x3),
            Transform(label_2x, new_label_3x2),
            run_time=2,
        )
        self.wait(2)

        # General rule
        general = MathTex(
            r"\frac{d}{dx}[x^n] = nx^{n-1}", font_size=36, color=YELLOW
        )
        general.to_edge(DOWN)
        self.play(Write(general))
        self.wait(2)
