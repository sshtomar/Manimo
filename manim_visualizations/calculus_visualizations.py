"""
Calculus Visualizations - Functions, Derivatives, and Integrals
Animated mathematical intuition for calculus concepts

Improved with 3Blue1Brown visualization principles:
- Progressive disclosure (one concept per step)
- Geometry before symbols
- Transformation over replacement
- Consistent color coding
- Strategic pauses and rhythm
- Visual hierarchy through opacity
"""

from manim import (
    VGroup,
    Axes,
    Text,
    MathTex,
    Tex,
    Dot,
    Line,
    DashedLine,
    Arrow,
    Rectangle,
    SurroundingRectangle,
    Create,
    Write,
    FadeIn,
    FadeOut,
    Transform,
    TransformFromCopy,
    TransformMatchingTex,
    ReplacementTransform,
    MoveAlongPath,
    Indicate,
    LaggedStart,
    LaggedStartMap,
    AnimationGroup,
    Succession,
    ValueTracker,
    always_redraw,
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
    linear,
    smooth,
    config,
)

from themed_scene import ThemedScene


class FunctionPlotAnimation(ThemedScene):
    """
    Animate how a function is plotted over time.

    3b1b Principles Applied:
    - Geometry first (axes, then curve, then formula)
    - Progressive disclosure
    - Transformation over replacement (Transform instead of FadeOut/FadeIn)
    - Strategic pauses
    """

    def construct(self):
        t = self.theme

        # =====================================================================
        # PHASE 1: SETUP - Create coordinate system (geometry first)
        # =====================================================================
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 10, 2],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True, "include_numbers": True},
        )
        axes.shift(DOWN * 0.5)
        labels = axes.get_axis_labels(
            x_label=MathTex("x", color=t.accent),
            y_label=MathTex("y")
        )

        # Show axes with staggered animation
        self.play(Create(axes), run_time=1.5)
        self.play(Write(labels))
        self.wait(0.5)  # Short pause after setup

        # =====================================================================
        # PHASE 2: BUILD - Show the function being traced
        # =====================================================================

        # Plot the function with tracing dot (show process, not just result)
        graph = axes.plot(lambda x: x**2, x_range=[-3, 3], color=t.primary)

        # Tracing dot that follows the curve creation
        trace_dot = Dot(color=t.accent, radius=0.12)
        trace_dot.move_to(axes.c2p(-3, 9))

        # Add the dot first, then create curve with dot following
        self.play(FadeIn(trace_dot, scale=0.5))

        # Animate curve creation with dot tracking the endpoint
        trace_dot.add_updater(lambda m: m.move_to(graph.get_end()))
        self.play(Create(graph), run_time=3, rate_func=linear)
        trace_dot.clear_updaters()

        self.wait(1)  # Medium pause - let the curve sink in

        # =====================================================================
        # PHASE 3: EXPLAIN - Now add the formula (symbols after geometry)
        # =====================================================================
        func_label = MathTex(
            r"f(x) = x^2",
            tex_to_color_map={"x": t.accent, "f": t.primary},
            font_size=t.body_size
        )
        func_label.to_corner(UR)

        # Transform dot into the formula (connection between visual and symbolic)
        self.play(
            TransformFromCopy(trace_dot, func_label),
            FadeOut(trace_dot),
            run_time=1.5
        )
        self.wait(1.5)  # Longer pause - important connection made

        # =====================================================================
        # PHASE 4: EXTEND - Transform to another function (not replace!)
        # =====================================================================

        # Use TransformMatchingTex for equation evolution
        new_label = MathTex(
            r"g(x) = \sin(x) + 3",
            tex_to_color_map={"x": t.accent, "g": t.tertiary},
            font_size=t.body_size
        )
        new_label.to_corner(UR)

        new_graph = axes.plot(
            lambda x: np.sin(x) + 3, x_range=[-3, 3], color=t.tertiary
        )

        # Transformation shows the relationship
        self.play(
            Transform(graph, new_graph),
            Transform(func_label, new_label),
            run_time=2,
            rate_func=smooth
        )
        self.wait(2)  # Final pause for comprehension


class TangentLineDerivative(ThemedScene):
    """
    Animate tangent lines moving along a curve to explain derivatives.

    3b1b Principles Applied:
    - Show the visual (tangent line) before the formula
    - Synchronized representations (slope value + tangent line)
    - Progressive disclosure
    - Consistent color coding
    """

    def construct(self):
        t = self.theme

        # =====================================================================
        # PHASE 1: SETUP - Establish the curve (geometry first)
        # =====================================================================
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 10, 2],
            x_length=7,
            y_length=5,
            axis_config={"include_tip": True, "include_numbers": True},
        )
        axes.shift(DOWN * 0.5 + LEFT * 1)
        labels = axes.get_axis_labels(
            x_label=MathTex("x", color=t.accent),
            y_label=MathTex("y")
        )

        self.play(Create(axes), run_time=1)
        self.play(Write(labels))

        # Function definition
        func = lambda x: x**2
        derivative = lambda x: 2 * x

        graph = axes.plot(func, x_range=[-0.5, 3.2], color=t.primary, stroke_width=t.curve_stroke_width)

        # Show the curve first, no label yet (geometry before symbols)
        self.play(Create(graph), run_time=2)
        self.wait(1)  # Let viewers see the curve

        # =====================================================================
        # PHASE 2: INTRODUCE THE TANGENT - Visual before formula
        # =====================================================================
        x_tracker = ValueTracker(1.0)  # Start at x=1 for cleaner numbers

        # Point on curve (prominent, important)
        point = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(), func(x_tracker.get_value())),
            color=t.accent,
            radius=0.12
        ))

        # Tangent line
        def get_tangent_line():
            x = x_tracker.get_value()
            slope = derivative(x)
            y = func(x)
            # Create a line through the point with the derivative as slope
            x_range = 1.5  # How far the line extends
            start = axes.c2p(x - x_range, y - slope * x_range)
            end = axes.c2p(x + x_range, y + slope * x_range)
            return Line(start, end, color=t.secondary, stroke_width=t.curve_stroke_width)

        tangent = always_redraw(get_tangent_line)

        # Show point first, then tangent (progressive disclosure)
        self.play(FadeIn(point, scale=0.5))
        self.wait(0.5)
        self.play(Create(tangent))
        self.wait(1)  # Let the tangent sink in

        # =====================================================================
        # PHASE 3: ADD LABELS - Now explain what we're seeing
        # =====================================================================

        # Function label (lower opacity - context, not focus)
        func_label = MathTex(r"f(x) = x^2", font_size=t.body_size, color=t.primary)
        func_label.next_to(graph, UR, buff=0.2)
        func_label.set_opacity(0.7)  # Context element

        self.play(Write(func_label))

        # Slope display (synchronized with tangent) - this is the focus
        slope_display = always_redraw(lambda: VGroup(
            MathTex(
                rf"x = {x_tracker.get_value():.1f}",
                font_size=t.body_size,
                color=t.accent,
            ),
            MathTex(
                rf"\text{{slope}} = f'(x) = {derivative(x_tracker.get_value()):.1f}",
                font_size=t.body_size,
                color=t.secondary,
            ),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR))

        self.play(Write(slope_display))
        self.wait(1)

        # =====================================================================
        # PHASE 4: ANIMATE - Show how tangent changes along curve
        # =====================================================================

        # Strategic movements with pauses at key points
        movements = [
            (2.0, 3, "Slope increases as x increases"),
            (0.5, 2, "Near zero, slope is small"),
            (0, 1.5, "At x=0, slope is zero (minimum!)"),
            (2.5, 2, "Slope continues to grow"),
        ]

        for target_x, duration, _ in movements:
            self.play(
                x_tracker.animate.set_value(target_x),
                run_time=duration,
                rate_func=smooth
            )
            self.wait(1)  # Pause at each key point

        # =====================================================================
        # PHASE 5: RESOLUTION - State the key insight
        # =====================================================================
        title = Text("Derivative = Slope of Tangent Line", font_size=t.body_size, color=t.accent)
        title.to_edge(UP)

        self.play(Write(title))
        self.wait(2)


class SecantToTangent(ThemedScene):
    """
    Show how secant lines approach tangent as dx -> 0.
    Core idea of the derivative definition.

    3b1b Principles Applied:
    - Building suspense (will it converge?)
    - Progressive disclosure with Transform
    - Strategic pauses at key moments
    - Equation evolution with color coding
    """

    def construct(self):
        t = self.theme

        # =====================================================================
        # PHASE 1: SETUP - Establish the curve and fixed point
        # =====================================================================
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 10, 2],
            x_length=6,
            y_length=5,
            axis_config={"include_tip": True, "include_numbers": True},
        )
        axes.shift(LEFT * 2 + DOWN * 0.5)

        self.play(Create(axes), run_time=1)

        func = lambda x: x**2
        graph = axes.plot(func, x_range=[0.5, 3.2], color=t.primary, stroke_width=t.curve_stroke_width)
        self.play(Create(graph), run_time=1.5)
        self.wait(0.5)

        # Fixed point a
        x0 = 1.5
        point_a = Dot(axes.c2p(x0, func(x0)), color=t.accent, radius=0.1)
        label_a = MathTex("a", font_size=t.label_size, color=t.accent).next_to(point_a, DL, buff=0.1)

        self.play(FadeIn(point_a, scale=0.5), Write(label_a))
        self.wait(1)

        # =====================================================================
        # PHASE 2: INTRODUCE THE CONCEPT - Show formula first time
        # =====================================================================
        formula = MathTex(
            r"\text{Slope} = \frac{f(a+h) - f(a)}{h}",
            font_size=t.body_size,
            tex_to_color_map={"a": t.accent, "h": t.accent2}
        )
        formula.to_corner(UR)
        self.play(Write(formula))
        self.wait(1)

        # =====================================================================
        # PHASE 3: BUILD SUSPENSE - Secant lines approaching tangent
        # =====================================================================
        dx_values = [1.5, 1.0, 0.5, 0.2, 0.05]

        # First secant line
        dx = dx_values[0]
        x1 = x0 + dx
        y0, y1 = func(x0), func(x1)
        slope = (y1 - y0) / dx

        point_b = Dot(axes.c2p(x1, y1), color=t.accent2, radius=0.08)

        # Extended line
        start = axes.c2p(x0 - 0.5, y0 - 0.5 * slope)
        end = axes.c2p(x1 + 0.5, y1 + 0.5 * slope)
        secant_line = Line(start, end, color=t.accent2, stroke_width=t.curve_stroke_width)

        h_display = VGroup(
            MathTex(f"h = {dx}", font_size=t.label_size, color=t.accent2),
            MathTex(f"\\text{{slope}} = {slope:.2f}", font_size=t.label_size, color=t.accent2),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(formula, DOWN, buff=0.5)

        self.play(
            FadeIn(point_b, scale=0.5),
            Create(secant_line),
        )
        self.play(Write(h_display))
        self.wait(1)

        # Iterate through remaining dx values - building suspense
        for dx in dx_values[1:]:
            x1 = x0 + dx
            y1 = func(x1)
            slope = (y1 - y0) / dx

            new_point_b = Dot(axes.c2p(x1, y1), color=t.accent2, radius=0.08)

            start = axes.c2p(x0 - 0.5, y0 - 0.5 * slope)
            end = axes.c2p(x1 + 0.5, y1 + 0.5 * slope)
            new_line = Line(start, end, color=t.accent2, stroke_width=t.curve_stroke_width)

            new_h_display = VGroup(
                MathTex(f"h = {dx}", font_size=t.label_size, color=t.accent2),
                MathTex(f"\\text{{slope}} = {slope:.2f}", font_size=t.label_size, color=t.accent2),
            ).arrange(DOWN, aligned_edge=LEFT).next_to(formula, DOWN, buff=0.5)

            # Transform (not replace!) - shows the progression
            self.play(
                Transform(secant_line, new_line),
                Transform(point_b, new_point_b),
                Transform(h_display, new_h_display),
                run_time=1 if dx > 0.1 else 1.5,  # Slower for small h (suspense!)
            )
            self.wait(0.75)

        # =====================================================================
        # PHASE 4: REVELATION - The limit!
        # =====================================================================
        self.wait(0.5)  # Pause before revelation

        # Change secant to tangent color (it has become the tangent!)
        final_tangent = secant_line.copy().set_color(t.secondary)
        self.play(
            Transform(secant_line, final_tangent),
            point_b.animate.set_opacity(0),  # Second point disappears
            run_time=1
        )

        # The limit formula - the big reveal
        limit_text = MathTex(
            r"\lim_{h \to 0} \frac{f(a+h) - f(a)}{h} = f'(a)",
            font_size=t.body_size,
            tex_to_color_map={"a": t.accent, "h": t.accent2, "f'": t.secondary}
        )
        limit_text.to_edge(DOWN)

        # Highlight box around the result
        box = SurroundingRectangle(limit_text, color=t.accent, buff=0.15)

        self.play(Write(limit_text), run_time=1.5)
        self.play(Create(box))
        self.wait(2)  # Long final pause


class RiemannSumsToIntegral(ThemedScene):
    """
    Animate Riemann sums becoming the definite integral.

    3b1b Principles Applied:
    - Geometry before symbols (show rectangles before integral notation)
    - Building suspense (will the rectangles fill the area?)
    - LaggedStart for rectangle creation
    - Progressive n values with strategic pauses
    """

    def construct(self):
        t = self.theme

        # =====================================================================
        # PHASE 1: SETUP - The curve and bounds
        # =====================================================================
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 8, 2],
            x_length=9,
            y_length=4.5,
            axis_config={"include_tip": True, "include_numbers": True},
        )
        axes.shift(DOWN * 0.8)

        labels = axes.get_axis_labels(
            x_label=MathTex("x", color=t.accent),
            y_label=MathTex("y")
        )

        self.play(Create(axes), run_time=1)
        self.play(Write(labels))

        # Function
        func = lambda x: 0.5 * x**2 - x + 4
        graph = axes.plot(func, x_range=[0.5, 4.5], color=t.primary, stroke_width=t.curve_stroke_width)

        # Show curve
        self.play(Create(graph), run_time=1.5)
        self.wait(0.5)

        # Function label (context, reduced opacity)
        func_label = MathTex(r"f(x)", font_size=t.label_size, color=t.primary)
        func_label.next_to(graph.get_end(), RIGHT)
        func_label.set_opacity(0.7)
        self.play(FadeIn(func_label))

        # =====================================================================
        # PHASE 2: ESTABLISH BOUNDS - Show the area we want
        # =====================================================================
        a, b = 1, 4

        # Bound lines with labels
        bound_a = DashedLine(
            axes.c2p(a, 0), axes.c2p(a, func(a)),
            color=t.accent, stroke_width=t.axis_stroke_width
        )
        bound_b = DashedLine(
            axes.c2p(b, 0), axes.c2p(b, func(b)),
            color=t.accent, stroke_width=t.axis_stroke_width
        )

        label_a = MathTex("a=1", font_size=t.small_size, color=t.accent).next_to(bound_a, DOWN)
        label_b = MathTex("b=4", font_size=t.small_size, color=t.accent).next_to(bound_b, DOWN)

        self.play(
            Create(bound_a), Create(bound_b),
            Write(label_a), Write(label_b),
        )
        self.wait(1)

        # Pose the question
        question = Text("What is the area under the curve?", font_size=t.label_size)
        question.to_edge(UP)
        self.play(Write(question))
        self.wait(1)

        # =====================================================================
        # PHASE 3: BUILD - Show Riemann rectangles with increasing n
        # =====================================================================
        n_values = [4, 8, 16, 32, 64]

        # n display
        n_display = VGroup(
            Text("Rectangles:", font_size=t.small_size),
            MathTex("n = 4", font_size=t.body_size, color=t.accent)
        ).arrange(RIGHT, buff=0.3).to_corner(UR)

        # First set of rectangles - use LaggedStart for rhythm
        rects = axes.get_riemann_rectangles(
            graph,
            x_range=[a, b],
            dx=(b - a) / 4,
            color=[t.primary, t.tertiary],
            fill_opacity=t.area_fill_opacity,
            stroke_width=t.fine_stroke_width,
            stroke_color=t.foreground,
        )

        # Staggered creation of rectangles (3b1b rhythm)
        self.play(
            LaggedStartMap(Create, rects, lag_ratio=0.15),
            Write(n_display),
            run_time=2
        )
        self.wait(1)

        # Transform through increasing n values
        for n in n_values[1:]:
            new_rects = axes.get_riemann_rectangles(
                graph,
                x_range=[a, b],
                dx=(b - a) / n,
                color=[t.primary, t.tertiary],
                fill_opacity=t.area_fill_opacity,
                stroke_width=0.5 if n > 16 else t.fine_stroke_width,
                stroke_color=t.foreground,
            )

            new_n_display = VGroup(
                Text("Rectangles:", font_size=t.small_size),
                MathTex(f"n = {n}", font_size=t.body_size, color=t.accent)
            ).arrange(RIGHT, buff=0.3).to_corner(UR)

            # Longer animation for larger n (building suspense)
            duration = 1.0 if n <= 16 else 1.5

            self.play(
                Transform(rects, new_rects),
                Transform(n_display, new_n_display),
                run_time=duration,
            )
            self.wait(0.75 if n < 64 else 1.5)  # Longer pause at the end

        # =====================================================================
        # PHASE 4: RESOLUTION - The integral
        # =====================================================================

        # Transform rectangles into smooth area
        area = axes.get_area(graph, x_range=[a, b], color=t.tertiary, opacity=0.7)

        self.play(
            Transform(rects, area),
            FadeOut(n_display),
            run_time=1.5
        )
        self.wait(0.5)

        # Now introduce the integral notation (symbol AFTER geometry)
        self.play(FadeOut(question))

        integral = MathTex(
            r"\int_1^4 f(x) \, dx",
            r"=",
            r"\text{Exact Area}",
            font_size=t.body_size,
        )
        integral[0].set_color(t.tertiary)
        integral[2].set_color(t.tertiary)
        integral.to_edge(UP)

        self.play(Write(integral[0]))
        self.wait(0.5)
        self.play(Write(integral[1:]))

        # Final highlight
        box = SurroundingRectangle(integral, color=t.accent, buff=0.1)
        self.play(Create(box))
        self.wait(2)


class DerivativeIntegralRelation(ThemedScene):
    """
    Visualize the Fundamental Theorem of Calculus.

    3b1b Principles Applied:
    - Dual-space synchronized visualization
    - Show geometric relationship first
    - Consistent color coding (f=primary, F=tertiary)
    - Equation evolution
    """

    def construct(self):
        t = self.theme

        # =====================================================================
        # PHASE 1: SETUP - Two synchronized graphs
        # =====================================================================

        # Left axes for f(x) = 2x
        axes_left = Axes(
            x_range=[0, 4, 1],
            y_range=[-1, 8, 2],
            x_length=5,
            y_length=4,
            axis_config={"include_tip": True, "include_numbers": True},
        )
        axes_left.shift(LEFT * 3.5 + DOWN * 0.3)

        # Right axes for F(x) = x^2
        axes_right = Axes(
            x_range=[0, 4, 1],
            y_range=[-1, 10, 2],
            x_length=5,
            y_length=4,
            axis_config={"include_tip": True, "include_numbers": True},
        )
        axes_right.shift(RIGHT * 3.5 + DOWN * 0.3)

        # Create both axes (staggered)
        self.play(Create(axes_left), run_time=1)
        self.play(Create(axes_right), run_time=1)
        self.wait(0.5)

        # =====================================================================
        # PHASE 2: BUILD THE RELATIONSHIP - Synchronized trackers
        # =====================================================================

        # Shared x tracker for synchronization
        x_tracker = ValueTracker(0.5)

        # Left: f(x) = 2x with area that accumulates
        f_graph = axes_left.plot(lambda x: 2 * x, x_range=[0, 3.5], color=t.primary)

        # Area under f that grows
        area = always_redraw(lambda: axes_left.get_area(
            f_graph,
            x_range=[0, x_tracker.get_value()],
            color=t.tertiary,
            opacity=t.area_fill_opacity
        ))

        # Vertical line at x
        f_line = always_redraw(lambda: DashedLine(
            axes_left.c2p(x_tracker.get_value(), 0),
            axes_left.c2p(x_tracker.get_value(), 2 * x_tracker.get_value()),
            color=t.accent
        ))

        # Right: F(x) = x^2, point that tracks accumulated area
        F_graph = axes_right.plot(lambda x: x**2, x_range=[0, 3.2], color=t.tertiary)

        # Point on F that corresponds to the area
        F_point = always_redraw(lambda: Dot(
            axes_right.c2p(x_tracker.get_value(), x_tracker.get_value()**2),
            color=t.tertiary,
            radius=0.12
        ))

        # Vertical line at x on right
        F_line = always_redraw(lambda: DashedLine(
            axes_right.c2p(x_tracker.get_value(), 0),
            axes_right.c2p(x_tracker.get_value(), x_tracker.get_value()**2),
            color=t.accent
        ))

        # Labels (positioned with updaters)
        label_left = MathTex("f(x) = 2x", font_size=t.label_size, color=t.primary)
        label_left.next_to(axes_left, UP)

        label_right = MathTex("F(x) = x^2", font_size=t.label_size, color=t.tertiary)
        label_right.next_to(axes_right, UP)

        # Show left side first
        self.play(Create(f_graph), Write(label_left))
        self.wait(0.5)

        # Show area concept
        self.play(FadeIn(area), Create(f_line))
        self.wait(1)

        # Show right side - the antiderivative
        self.play(Create(F_graph), Write(label_right))
        self.play(FadeIn(F_point), Create(F_line))
        self.wait(1)

        # =====================================================================
        # PHASE 3: ANIMATE THE CONNECTION
        # =====================================================================

        # Area value display (synchronized)
        value_display = always_redraw(lambda: VGroup(
            MathTex(
                rf"x = {x_tracker.get_value():.1f}",
                font_size=t.label_size,
                color=t.accent
            ),
            MathTex(
                rf"\text{{Area}} = {x_tracker.get_value()**2:.2f}",
                font_size=t.label_size,
                color=t.tertiary
            ),
            MathTex(
                rf"F(x) = {x_tracker.get_value()**2:.2f}",
                font_size=t.label_size,
                color=t.tertiary
            ),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR))

        self.play(Write(value_display))
        self.wait(0.5)

        # Animate x changing - show the relationship
        self.play(x_tracker.animate.set_value(2.5), run_time=4, rate_func=smooth)
        self.wait(1)
        self.play(x_tracker.animate.set_value(1.0), run_time=2)
        self.wait(1)
        self.play(x_tracker.animate.set_value(3.0), run_time=2)
        self.wait(1)

        # =====================================================================
        # PHASE 4: STATE THE THEOREM
        # =====================================================================

        # Clear some clutter
        self.play(FadeOut(value_display))

        # The theorem - equation evolution
        theorem1 = MathTex(
            r"\frac{d}{dx}\left[ \int_0^x f(t)\,dt \right] = f(x)",
            font_size=t.body_size,
        )
        theorem1[0][0:5].set_color(t.secondary)  # d/dx
        theorem1[0][6:7].set_color(t.tertiary)  # integral
        theorem1.to_edge(DOWN).shift(LEFT * 2)

        theorem2 = MathTex(
            r"\int f(x)\,dx = F(x) + C",
            font_size=t.body_size,
        )
        theorem2[0][0].set_color(t.tertiary)
        theorem2[0][-4:-2].set_color(t.tertiary)  # F(x)
        theorem2.to_edge(DOWN).shift(RIGHT * 2)

        self.play(Write(theorem1))
        self.wait(1)
        self.play(Write(theorem2))

        # Title
        title = Text("Fundamental Theorem of Calculus", font_size=t.body_size, color=t.accent)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(2)


class AreaAccumulation(ThemedScene):
    """
    Show how the integral F(x) represents accumulated area.

    3b1b Principles Applied:
    - Synchronized formula and visual
    - Progressive disclosure
    - Linear rate function for accurate time representation
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
            axis_config={"include_tip": True, "include_numbers": True},
        )
        axes.shift(DOWN * 0.8)
        labels = axes.get_axis_labels(
            x_label=MathTex("x", color=t.accent),
            y_label=MathTex("f(x)", color=t.primary)
        )

        self.play(Create(axes), Write(labels), run_time=1.5)

        # Function
        func = lambda x: 0.3 * x**2 + 0.5
        antideriv = lambda x: 0.1 * x**3 + 0.5 * x  # Antiderivative

        graph = axes.plot(func, x_range=[0.3, 4.5], color=t.primary, stroke_width=t.curve_stroke_width)
        self.play(Create(graph), run_time=1.5)
        self.wait(1)

        # =====================================================================
        # PHASE 2: SHOW ACCUMULATION CONCEPT
        # =====================================================================
        x_tracker = ValueTracker(0.5)
        x_start = 0.5

        # Area that grows
        area = always_redraw(lambda: axes.get_area(
            graph,
            x_range=[x_start, max(x_tracker.get_value(), x_start + 0.01)],
            color=t.tertiary,
            opacity=0.6,
        ))

        # Moving boundary line
        boundary_line = always_redraw(lambda: DashedLine(
            axes.c2p(x_tracker.get_value(), 0),
            axes.c2p(x_tracker.get_value(), func(x_tracker.get_value())),
            color=t.accent,
            stroke_width=t.axis_stroke_width,
        ))

        # Moving point on curve
        boundary_point = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(), func(x_tracker.get_value())),
            color=t.accent,
            radius=0.1
        ))

        # Synchronized formula display
        area_formula = always_redraw(lambda: MathTex(
            rf"F({x_tracker.get_value():.1f}) = \int_{{{x_start}}}^{{{x_tracker.get_value():.1f}}} f(t)\,dt",
            font_size=t.label_size,
            tex_to_color_map={"F": t.tertiary, "f": t.primary}
        ).to_corner(UR))

        # Numerical value
        area_value = always_redraw(lambda: MathTex(
            rf"= {antideriv(x_tracker.get_value()) - antideriv(x_start):.2f}",
            font_size=t.label_size,
            color=t.tertiary
        ).next_to(area_formula, DOWN, aligned_edge=RIGHT))

        # Show elements progressively
        self.play(FadeIn(area), Create(boundary_line), FadeIn(boundary_point))
        self.wait(0.5)
        self.play(Write(area_formula))
        self.play(Write(area_value))
        self.wait(1)

        # =====================================================================
        # PHASE 3: ANIMATE ACCUMULATION
        # =====================================================================

        # Use linear rate function to show actual area accumulation
        self.play(
            x_tracker.animate.set_value(4.0),
            run_time=6,
            rate_func=linear  # Linear for accurate accumulation visualization
        )
        self.wait(1)

        # =====================================================================
        # PHASE 4: KEY INSIGHT
        # =====================================================================
        insight = Text(
            "The integral accumulates area as x increases",
            font_size=t.label_size,
            color=t.accent
        )
        insight.to_edge(UP)
        self.play(Write(insight))
        self.wait(2)


class PowerRuleDerivative(ThemedScene):
    """
    Visualize the power rule for derivatives.

    3b1b Principles Applied:
    - Dual representation (function + derivative)
    - Equation evolution with TransformMatchingTex
    - Consistent color coding
    - Build to general rule
    """

    def construct(self):
        t = self.theme

        # =====================================================================
        # PHASE 1: SETUP
        # =====================================================================
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2, 8, 2],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True, "include_numbers": True},
        )
        axes.shift(DOWN * 0.3)

        self.play(Create(axes), run_time=1)
        self.wait(0.5)

        # =====================================================================
        # PHASE 2: FIRST EXAMPLE - x^2 and 2x
        # =====================================================================

        # Functions
        func_x2 = axes.plot(lambda x: x**2, x_range=[-2.2, 2.2], color=t.primary)
        deriv_2x = axes.plot(lambda x: 2 * x, x_range=[-2.2, 2.2], color=t.secondary)

        # Labels with consistent coloring
        label_x2 = MathTex(
            r"f(x) = x^2",
            font_size=t.label_size,
            tex_to_color_map={"f": t.primary, "x": t.accent}
        )
        label_x2.to_corner(UL).shift(DOWN * 0.3)

        label_2x = MathTex(
            r"f'(x) = 2x",
            font_size=t.label_size,
            tex_to_color_map={"f'": t.secondary, "x": t.accent}
        )
        label_2x.next_to(label_x2, DOWN, aligned_edge=LEFT)

        # Show function first
        self.play(Create(func_x2), Write(label_x2), run_time=1.5)
        self.wait(1)

        # Then derivative (progressive disclosure)
        self.play(Create(deriv_2x), Write(label_2x), run_time=1.5)
        self.wait(1.5)

        # =====================================================================
        # PHASE 3: TRANSFORM TO x^3 and 3x^2
        # =====================================================================

        func_x3 = axes.plot(lambda x: x**3, x_range=[-1.8, 1.8], color=t.primary)
        deriv_3x2 = axes.plot(lambda x: 3 * x**2, x_range=[-1.6, 1.6], color=t.secondary)

        # New labels - use TransformMatchingTex for smooth equation evolution
        new_label_x3 = MathTex(
            r"f(x) = x^3",
            font_size=t.label_size,
            tex_to_color_map={"f": t.primary, "x": t.accent}
        )
        new_label_x3.to_corner(UL).shift(DOWN * 0.3)

        new_label_3x2 = MathTex(
            r"f'(x) = 3x^2",
            font_size=t.label_size,
            tex_to_color_map={"f'": t.secondary, "x": t.accent}
        )
        new_label_3x2.next_to(new_label_x3, DOWN, aligned_edge=LEFT)

        # Transform everything together (shows relationship)
        self.play(
            Transform(func_x2, func_x3),
            Transform(deriv_2x, deriv_3x2),
            Transform(label_x2, new_label_x3),
            Transform(label_2x, new_label_3x2),
            run_time=2,
        )
        self.wait(1.5)

        # =====================================================================
        # PHASE 4: TRANSFORM TO x^4 and 4x^3
        # =====================================================================

        func_x4 = axes.plot(lambda x: x**4, x_range=[-1.5, 1.5], color=t.primary)
        deriv_4x3 = axes.plot(lambda x: 4 * x**3, x_range=[-1.4, 1.4], color=t.secondary)

        final_label_f = MathTex(
            r"f(x) = x^4",
            font_size=t.label_size,
            tex_to_color_map={"f": t.primary, "x": t.accent}
        )
        final_label_f.to_corner(UL).shift(DOWN * 0.3)

        final_label_fp = MathTex(
            r"f'(x) = 4x^3",
            font_size=t.label_size,
            tex_to_color_map={"f'": t.secondary, "x": t.accent}
        )
        final_label_fp.next_to(final_label_f, DOWN, aligned_edge=LEFT)

        self.play(
            Transform(func_x2, func_x4),
            Transform(deriv_2x, deriv_4x3),
            Transform(label_x2, final_label_f),
            Transform(label_2x, final_label_fp),
            run_time=2,
        )
        self.wait(1.5)

        # =====================================================================
        # PHASE 5: REVEAL THE GENERAL RULE
        # =====================================================================

        # Fade graphs to background
        self.play(
            func_x2.animate.set_opacity(0.3),
            deriv_2x.animate.set_opacity(0.3),
        )

        # The general power rule - the big reveal
        general_rule = MathTex(
            r"\frac{d}{dx}\left[ x^n \right] = n \cdot x^{n-1}",
            font_size=t.title_size,
        )
        general_rule[0][0:4].set_color(t.secondary)  # d/dx
        general_rule[0][5:7].set_color(t.primary)   # x^n
        general_rule[0][9].set_color(t.accent)  # n
        general_rule[0][11:15].set_color(t.secondary)  # x^{n-1}
        general_rule.move_to(DOWN * 2)

        # Highlight box
        box = SurroundingRectangle(general_rule, color=t.accent, buff=0.2)

        self.play(Write(general_rule), run_time=1.5)
        self.play(Create(box))

        # Title
        title = Text("The Power Rule", font_size=t.body_size, color=t.accent)
        title.to_edge(UP)
        self.play(Write(title))

        self.wait(2)
