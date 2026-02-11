"""
Wave and Field Visualizations - Trigonometry, Vector Fields, and Complex Numbers
Beautiful mathematical animations inspired by 3Blue1Brown

No LaTeX dependency - uses Text instead of MathTex for compatibility.

3Blue1Brown Principles Applied:
- Progressive disclosure (one concept per step)
- Geometry before symbols
- Transformation over replacement
- Consistent color coding
- Strategic pauses and rhythm
"""

from manim import (
    Scene,
    VGroup,
    Axes,
    NumberPlane,
    Text,
    Dot,
    Line,
    DashedLine,
    Arrow,
    Circle,
    Arc,
    Create,
    Write,
    FadeIn,
    FadeOut,
    Transform,
    ReplacementTransform,
    GrowArrow,
    LaggedStart,
    LaggedStartMap,
    ValueTracker,
    always_redraw,
    SurroundingRectangle,
    TracedPath,
    BLUE,
    BLUE_D,
    RED,
    GREEN,
    GREEN_D,
    YELLOW,
    ORANGE,
    PURPLE,
    TEAL,
    PINK,
    WHITE,
    GREY,
    GREY_B,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    UR,
    UL,
    DR,
    ORIGIN,
    PI,
    TAU,
    np,
    linear,
    smooth,
)

# =============================================================================
# CONSISTENT COLOR PALETTE
# =============================================================================
WAVE_COLOR = BLUE
WAVE2_COLOR = RED
SUM_COLOR = GREEN
AMPLITUDE_COLOR = YELLOW
VECTOR_COLOR = TEAL
COMPLEX_COLOR = ORANGE
REAL_COLOR = BLUE
IMAG_COLOR = GREEN
HIGHLIGHT_COLOR = YELLOW


class SineWaveGeneration(Scene):
    """
    Show how sine wave is generated from circular motion.
    The projection of a point on a circle traces out the familiar sine curve.
    """

    def construct(self):
        # =====================================================================
        # PHASE 1: SETUP - Create the circle and axes
        # =====================================================================

        # Left side: Unit circle
        circle = Circle(radius=1.5, color=GREY_B)
        circle.shift(LEFT * 3.5)
        circle_center = circle.get_center()

        # Right side: Axes for the wave
        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-2, 2, 1],
            x_length=7,
            y_length=3,
            axis_config={"include_tip": True, "include_numbers": False},
        )
        axes.shift(RIGHT * 1.5)

        # Title
        title = Text("Sine Wave from Circular Motion", font_size=32)
        title.to_edge(UP)

        self.play(Create(circle), Create(axes), Write(title), run_time=1.5)
        self.wait(0.5)

        # =====================================================================
        # PHASE 2: BUILD - Show the rotating point on circle
        # =====================================================================

        theta = ValueTracker(0)

        # Point on the circle
        rotating_dot = always_redraw(lambda: Dot(
            circle_center + 1.5 * np.array([
                np.cos(theta.get_value()),
                np.sin(theta.get_value()),
                0
            ]),
            color=WAVE_COLOR,
            radius=0.1
        ))

        # Radius line from center to point
        radius_line = always_redraw(lambda: Line(
            circle_center,
            circle_center + 1.5 * np.array([
                np.cos(theta.get_value()),
                np.sin(theta.get_value()),
                0
            ]),
            color=WAVE_COLOR,
            stroke_width=3
        ))

        # Horizontal dashed line showing projection
        h_line = always_redraw(lambda: DashedLine(
            circle_center + 1.5 * np.array([
                np.cos(theta.get_value()),
                np.sin(theta.get_value()),
                0
            ]),
            axes.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=AMPLITUDE_COLOR,
            stroke_width=2,
            dash_length=0.1
        ))

        # Point on the sine curve
        trace_dot = always_redraw(lambda: Dot(
            axes.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=WAVE_COLOR,
            radius=0.08
        ))

        self.play(FadeIn(rotating_dot), FadeIn(radius_line))
        self.wait(0.5)
        self.play(FadeIn(h_line), FadeIn(trace_dot))
        self.wait(0.5)

        # =====================================================================
        # PHASE 3: ANIMATE - Trace the sine wave using TracedPath
        # =====================================================================

        # Use TracedPath for smooth tracing
        trace = TracedPath(
            trace_dot.get_center,
            stroke_color=WAVE_COLOR,
            stroke_width=3,
            dissipating_time=None
        )
        self.add(trace)

        # Animate two full rotations
        self.play(
            theta.animate.set_value(2 * PI),
            run_time=4,
            rate_func=linear
        )
        self.wait(0.5)

        self.play(
            theta.animate.set_value(4 * PI),
            run_time=4,
            rate_func=linear
        )

        # =====================================================================
        # PHASE 4: EXPLAIN - Add the formula
        # =====================================================================

        formula = Text("y = sin(theta)", font_size=32, color=WAVE_COLOR)
        formula.to_corner(UR)

        self.play(Write(formula))
        self.wait(2)


class WaveInterference(Scene):
    """
    Two waves combining - constructive and destructive interference.
    Shows superposition principle visually.
    """

    def construct(self):
        # =====================================================================
        # PHASE 1: SETUP - Create three sets of axes stacked vertically
        # =====================================================================

        # Top axes - Wave 1
        axes1 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            y_length=1.8,
            axis_config={"include_tip": False, "include_numbers": False},
        )
        axes1.shift(UP * 2.2)

        # Middle axes - Wave 2
        axes2 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            y_length=1.8,
            axis_config={"include_tip": False, "include_numbers": False},
        )

        # Bottom axes - Sum
        axes3 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=2.2,
            axis_config={"include_tip": False, "include_numbers": False},
        )
        axes3.shift(DOWN * 2.4)

        # Labels
        label1 = Text("Wave 1", font_size=24, color=WAVE_COLOR).next_to(axes1, LEFT)
        label2 = Text("Wave 2", font_size=24, color=WAVE2_COLOR).next_to(axes2, LEFT)
        label3 = Text("Sum", font_size=24, color=SUM_COLOR).next_to(axes3, LEFT)

        self.play(
            LaggedStart(
                Create(axes1),
                Create(axes2),
                Create(axes3),
                lag_ratio=0.3
            ),
            run_time=2
        )
        self.play(Write(label1), Write(label2), Write(label3))
        self.wait(0.5)

        # =====================================================================
        # PHASE 2: BUILD - Show Wave 1
        # =====================================================================

        wave1 = axes1.plot(
            lambda x: np.sin(x),
            color=WAVE_COLOR,
            stroke_width=3
        )

        self.play(Create(wave1), run_time=2)
        self.wait(0.5)

        # =====================================================================
        # PHASE 3: SHOW Wave 2 with adjustable phase
        # =====================================================================

        phase = ValueTracker(0)

        wave2 = always_redraw(lambda: axes2.plot(
            lambda x: np.sin(x + phase.get_value()),
            color=WAVE2_COLOR,
            stroke_width=3
        ))

        sum_wave = always_redraw(lambda: axes3.plot(
            lambda x: np.sin(x) + np.sin(x + phase.get_value()),
            color=SUM_COLOR,
            stroke_width=3
        ))

        self.play(Create(wave2))
        self.play(Create(sum_wave))
        self.wait(1)

        # =====================================================================
        # PHASE 4: DEMONSTRATE - Constructive and destructive interference
        # =====================================================================

        phase_label = always_redraw(lambda: Text(
            f"phase = {phase.get_value() / PI:.1f} pi",
            font_size=28
        ).to_corner(UR))

        self.play(FadeIn(phase_label))

        # Constructive interference
        constructive_text = Text("Constructive Interference", font_size=28, color=SUM_COLOR)
        constructive_text.to_edge(DOWN)
        self.play(Write(constructive_text))
        self.wait(1)

        # Shift to destructive (phase = pi)
        self.play(FadeOut(constructive_text))
        self.play(phase.animate.set_value(PI), run_time=3, rate_func=smooth)

        destructive_text = Text("Destructive Interference", font_size=28, color=GREY)
        destructive_text.to_edge(DOWN)
        self.play(Write(destructive_text))
        self.wait(1)

        # Animate through different phases
        self.play(FadeOut(destructive_text))
        self.play(phase.animate.set_value(2 * PI), run_time=4, rate_func=linear)
        self.wait(1)


class VectorFieldVisualization(Scene):
    """
    Visualize a 2D vector field with animated arrows.
    Shows how vectors vary across space - rotational field.
    """

    def construct(self):
        # =====================================================================
        # PHASE 1: SETUP - Create coordinate plane
        # =====================================================================

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            }
        )

        self.play(Create(plane), run_time=1.5)
        self.wait(0.5)

        # =====================================================================
        # PHASE 2: BUILD - Create vector field arrows
        # =====================================================================

        title = Text("Rotational Vector Field", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # This field creates circular flow (rotation): F(x,y) = (-y, x)
        def field_func(x, y):
            return np.array([-y * 0.3, x * 0.3, 0])

        # Create arrows at grid points
        arrows = VGroup()
        for x in np.arange(-3.5, 4, 1):
            for y in np.arange(-2.5, 3, 1):
                if abs(x) < 0.3 and abs(y) < 0.3:
                    continue

                start = np.array([x, y, 0])
                direction = field_func(x, y)
                length = np.linalg.norm(direction)

                if length > 0.1:
                    # Normalize and scale
                    norm_dir = direction / length * min(length, 0.7)
                    arrow = Line(
                        start,
                        start + norm_dir,
                        color=VECTOR_COLOR,
                        stroke_width=3
                    )
                    # Add a small dot at the tip
                    tip = Dot(start + norm_dir, radius=0.05, color=VECTOR_COLOR)
                    arrows.add(VGroup(arrow, tip))

        self.play(
            LaggedStartMap(FadeIn, arrows, lag_ratio=0.02),
            run_time=3
        )
        self.wait(1)

        # =====================================================================
        # PHASE 3: DEMONSTRATE - Show a particle following the flow
        # =====================================================================

        explain = Text("Particles follow the field", font_size=24, color=YELLOW)
        explain.to_edge(DOWN)
        self.play(Write(explain))

        # Animate a dot following the field (circular path)
        t_tracker = ValueTracker(0)

        particle = always_redraw(lambda: Dot(
            np.array([
                2 * np.cos(t_tracker.get_value()),
                2 * np.sin(t_tracker.get_value()),
                0
            ]),
            color=YELLOW,
            radius=0.15
        ))

        # Create traced path for particle trail
        path_trace = TracedPath(
            particle.get_center,
            stroke_color=YELLOW,
            stroke_width=2,
            stroke_opacity=0.7
        )

        self.play(FadeIn(particle, scale=0.5))
        self.add(path_trace)

        self.play(
            t_tracker.animate.set_value(2 * PI),
            run_time=4,
            rate_func=linear
        )
        self.wait(1)

        # =====================================================================
        # PHASE 4: TRANSFORM - Show radial outward field
        # =====================================================================

        new_title = Text("Radial Vector Field", font_size=32)
        new_title.to_edge(UP)

        # Radial outward field: F(x,y) = (x, y)
        def radial_field(x, y):
            r = np.sqrt(x**2 + y**2)
            if r < 0.1:
                return np.array([0, 0, 0])
            return np.array([x * 0.2, y * 0.2, 0])

        new_arrows = VGroup()
        for x in np.arange(-3.5, 4, 1):
            for y in np.arange(-2.5, 3, 1):
                if abs(x) < 0.3 and abs(y) < 0.3:
                    continue

                start = np.array([x, y, 0])
                direction = radial_field(x, y)
                length = np.linalg.norm(direction)

                if length > 0.1:
                    norm_dir = direction / length * min(length, 0.7)
                    arrow = Line(
                        start,
                        start + norm_dir,
                        color=ORANGE,
                        stroke_width=3
                    )
                    tip = Dot(start + norm_dir, radius=0.05, color=ORANGE)
                    new_arrows.add(VGroup(arrow, tip))

        self.play(
            FadeOut(particle),
            FadeOut(path_trace),
            FadeOut(explain),
            Transform(title, new_title),
            Transform(arrows, new_arrows),
            run_time=2
        )
        self.wait(2)


class ComplexMultiplication(Scene):
    """
    Visualize multiplication of complex numbers as rotation and scaling.
    Shows why i * i = -1 makes geometric sense.
    """

    def construct(self):
        # =====================================================================
        # PHASE 1: SETUP - Create complex plane
        # =====================================================================

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            }
        )

        # Labels for axes
        real_label = Text("Real", font_size=20, color=REAL_COLOR)
        real_label.next_to(plane.get_x_axis().get_end(), DOWN)
        imag_label = Text("Imaginary", font_size=20, color=IMAG_COLOR)
        imag_label.next_to(plane.get_y_axis().get_end(), RIGHT)

        self.play(Create(plane), run_time=1.5)
        self.play(Write(real_label), Write(imag_label))
        self.wait(0.5)

        # =====================================================================
        # PHASE 2: BUILD - Show a complex number as a point/vector
        # =====================================================================

        title = Text("z = 2 + i", font_size=36)
        title.to_corner(UL)

        # Complex number z = 2 + i -> point at (2, 1)
        z_point = np.array([2, 1, 0])
        z_line = Line(ORIGIN, z_point, color=COMPLEX_COLOR, stroke_width=4)
        z_dot = Dot(z_point, color=COMPLEX_COLOR, radius=0.12)
        z_label = Text("z", color=COMPLEX_COLOR, font_size=28)
        z_label.next_to(z_dot, UR, buff=0.1)

        self.play(Write(title))
        self.play(Create(z_line))
        self.play(FadeIn(z_dot), Write(z_label))
        self.wait(1)

        # =====================================================================
        # PHASE 3: DEMONSTRATE - Multiply by i (rotation by 90 degrees)
        # =====================================================================

        multiply_text = Text("Multiply by i = 90 deg rotation", font_size=28)
        multiply_text.to_corner(UR)
        self.play(Write(multiply_text))
        self.wait(0.5)

        # i * (2 + i) = -1 + 2i
        iz_point = np.array([-1, 2, 0])

        # Show the rotation with an arc
        angle_arc = Arc(
            radius=0.8,
            start_angle=np.arctan2(1, 2),
            angle=PI / 2,
            color=YELLOW
        )

        self.play(Create(angle_arc))

        # Animate the rotation
        iz_line = Line(ORIGIN, iz_point, color=GREEN, stroke_width=4)
        iz_dot = Dot(iz_point, color=GREEN, radius=0.12)
        iz_label = Text("iz = -1 + 2i", color=GREEN, font_size=24)
        iz_label.next_to(iz_dot, UL, buff=0.1)

        self.play(Create(iz_line), FadeIn(iz_dot), Write(iz_label), run_time=2)
        self.wait(1)

        # =====================================================================
        # PHASE 4: EXTEND - Show i^2 = -1 geometrically
        # =====================================================================

        self.play(
            FadeOut(angle_arc),
            FadeOut(z_line),
            FadeOut(z_dot),
            FadeOut(z_label),
            FadeOut(iz_line),
            FadeOut(iz_dot),
            FadeOut(iz_label),
            FadeOut(multiply_text),
            FadeOut(title),
        )

        # New demonstration: start with 1, multiply by i twice
        new_title = Text("Why does i^2 = -1?", font_size=36)
        new_title.to_corner(UL)
        self.play(Write(new_title))

        # Start at 1
        one_point = np.array([1, 0, 0])
        one_line = Line(ORIGIN, one_point, color=BLUE, stroke_width=4)
        one_dot = Dot(one_point, color=BLUE, radius=0.12)
        one_label = Text("1", color=BLUE, font_size=28)
        one_label.next_to(one_point, DR, buff=0.1)

        self.play(Create(one_line), FadeIn(one_dot), Write(one_label))
        self.wait(0.5)

        # First multiplication by i: 1 -> i
        step1 = Text("x i", font_size=24, color=YELLOW).next_to(new_title, DOWN)
        self.play(Write(step1))

        i_point = np.array([0, 1, 0])
        arc1 = Arc(radius=0.5, start_angle=0, angle=PI / 2, color=YELLOW)
        self.play(Create(arc1))

        i_line = Line(ORIGIN, i_point, color=GREEN, stroke_width=4)
        i_dot = Dot(i_point, color=GREEN, radius=0.12)
        i_label = Text("i", color=GREEN, font_size=28)
        i_label.next_to(i_point, UR, buff=0.1)

        self.play(
            ReplacementTransform(one_line, i_line),
            ReplacementTransform(one_dot, i_dot),
            ReplacementTransform(one_label, i_label),
            run_time=1.5
        )
        self.wait(0.5)

        # Second multiplication by i: i -> -1
        step2 = Text("x i again", font_size=24, color=YELLOW).next_to(step1, DOWN)
        self.play(Write(step2))

        neg_one_point = np.array([-1, 0, 0])
        arc2 = Arc(radius=0.5, start_angle=PI / 2, angle=PI / 2, color=YELLOW)
        self.play(Create(arc2))

        neg_one_line = Line(ORIGIN, neg_one_point, color=RED, stroke_width=4)
        neg_one_dot = Dot(neg_one_point, color=RED, radius=0.12)
        neg_one_label = Text("-1", color=RED, font_size=28)
        neg_one_label.next_to(neg_one_point, UL, buff=0.1)

        self.play(
            ReplacementTransform(i_line, neg_one_line),
            ReplacementTransform(i_dot, neg_one_dot),
            ReplacementTransform(i_label, neg_one_label),
            run_time=1.5
        )

        # Final result
        final_result = Text("Two 90 deg rotations = 180 deg = multiply by -1", font_size=28, color=YELLOW)
        final_result.to_edge(DOWN)

        box = SurroundingRectangle(final_result, color=YELLOW, buff=0.15)

        self.play(Write(final_result), Create(box))
        self.wait(2)


class FourierSeriesSquareWave(Scene):
    """
    Build a square wave from sine waves - the Fourier series.
    Shows how any periodic function can be built from sinusoids.
    """

    def construct(self):
        # =====================================================================
        # PHASE 1: SETUP - Create axes
        # =====================================================================

        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-2, 2, 1],
            x_length=11,
            y_length=4,
            axis_config={"include_tip": True, "include_numbers": False},
        )
        axes.shift(DOWN * 0.5)

        title = Text("Building a Square Wave from Sine Waves", font_size=28)
        title.to_edge(UP)

        self.play(Create(axes), Write(title), run_time=1.5)
        self.wait(0.5)

        # =====================================================================
        # PHASE 2: BUILD - Show the target square wave
        # =====================================================================

        def square_wave(x):
            x_mod = x % (2 * PI)
            return 1 if x_mod < PI else -1

        square = axes.plot(
            square_wave,
            x_range=[0.01, 4 * PI - 0.01],
            color=GREY,
            stroke_width=2,
            use_smoothing=False,
            discontinuities=[PI, 2 * PI, 3 * PI],
        )

        target_label = Text("Target: Square Wave", font_size=20, color=GREY)
        target_label.to_corner(UR)

        self.play(Create(square), Write(target_label))
        self.wait(1)

        # =====================================================================
        # PHASE 3: DEMONSTRATE - Add harmonics one by one
        # =====================================================================

        def fourier_approx(x, n_terms):
            result = 0
            for k in range(n_terms):
                n = 2 * k + 1  # 1, 3, 5, 7, ...
                result += (4 / PI) * (1 / n) * np.sin(n * x)
            return result

        colors = [BLUE, GREEN, ORANGE, PURPLE, TEAL, PINK]

        # Start with n=1 (fundamental)
        current_approx = axes.plot(
            lambda x: fourier_approx(x, 1),
            color=colors[0],
            stroke_width=3
        )

        term_label = Text("n=1: sin(x)", font_size=24)
        term_label.next_to(axes, DOWN, buff=0.3)

        self.play(Create(current_approx), Write(term_label))
        self.wait(1)

        # Add more terms progressively
        terms_info = [
            (2, "n=1,3: + sin(3x)/3"),
            (3, "n=1,3,5: + sin(5x)/5"),
            (4, "n=1,3,5,7: + sin(7x)/7"),
            (5, "+ sin(9x)/9"),
            (8, "+ more harmonics..."),
            (15, "15 terms total"),
        ]

        for n_terms, label_text in terms_info:
            new_approx = axes.plot(
                lambda x, n=n_terms: fourier_approx(x, n),
                color=colors[min(n_terms - 1, len(colors) - 1)],
                stroke_width=3
            )

            new_label = Text(label_text, font_size=24)
            new_label.next_to(axes, DOWN, buff=0.3)

            self.play(
                Transform(current_approx, new_approx),
                Transform(term_label, new_label),
                run_time=1.5
            )
            self.wait(0.5)

        # =====================================================================
        # PHASE 4: RESOLUTION - Final insight
        # =====================================================================

        final_text = Text("Any periodic function = sum of sines!", font_size=28, color=HIGHLIGHT_COLOR)
        final_text.next_to(axes, DOWN, buff=0.5)

        self.play(Transform(term_label, final_text))
        self.wait(2)


class PendulumMotion(Scene):
    """
    Simple harmonic motion of a pendulum showing sine wave connection.
    """

    def construct(self):
        # =====================================================================
        # PHASE 1: SETUP - Create pendulum and graph
        # =====================================================================

        pivot = UP * 2.5 + LEFT * 4
        length = 2.5

        pivot_dot = Dot(pivot, color=WHITE, radius=0.08)

        # Graph on the right
        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=3,
            axis_config={"include_tip": True, "include_numbers": False},
        )
        axes.shift(RIGHT * 2)

        title = Text("Pendulum Motion = Sine Wave", font_size=28)
        title.to_edge(UP)

        x_label = Text("time", font_size=20).next_to(axes.x_axis.get_end(), DOWN)
        y_label = Text("angle", font_size=20).next_to(axes.y_axis.get_end(), LEFT)

        self.play(
            FadeIn(pivot_dot),
            Create(axes),
            Write(title),
            Write(x_label),
            Write(y_label),
            run_time=1.5
        )

        # =====================================================================
        # PHASE 2: BUILD - Create pendulum with angle tracker
        # =====================================================================

        t = ValueTracker(0)
        amplitude = 0.8
        omega = 1.5

        def get_angle():
            return amplitude * np.sin(omega * t.get_value())

        # Pendulum bob
        bob = always_redraw(lambda: Dot(
            pivot + length * np.array([
                np.sin(get_angle()),
                -np.cos(get_angle()),
                0
            ]),
            color=BLUE,
            radius=0.2
        ))

        # Pendulum rod
        rod = always_redraw(lambda: Line(
            pivot,
            pivot + length * np.array([
                np.sin(get_angle()),
                -np.cos(get_angle()),
                0
            ]),
            color=WHITE,
            stroke_width=3
        ))

        # Dashed vertical reference
        vertical_ref = DashedLine(pivot, pivot + DOWN * length, color=GREY, stroke_width=1)

        # Angle arc
        angle_arc = always_redraw(lambda: Arc(
            radius=0.5,
            start_angle=-PI / 2,
            angle=get_angle(),
            arc_center=pivot,
            color=YELLOW
        ) if abs(get_angle()) > 0.05 else VGroup())

        self.play(
            Create(vertical_ref),
            FadeIn(rod),
            FadeIn(bob),
            FadeIn(angle_arc),
        )
        self.wait(0.5)

        # =====================================================================
        # PHASE 3: ANIMATE - Swing pendulum and trace angle over time
        # =====================================================================

        # Point on the graph that traces the sine wave
        trace_point = always_redraw(lambda: Dot(
            axes.c2p(
                min(t.get_value(), 4 * PI),
                amplitude * np.sin(omega * t.get_value())
            ),
            color=YELLOW,
            radius=0.08
        ))

        # Use TracedPath for the wave
        trace = TracedPath(
            trace_point.get_center,
            stroke_color=BLUE,
            stroke_width=3,
            dissipating_time=None
        )

        self.add(trace)
        self.play(FadeIn(trace_point))

        # Animate the pendulum swinging
        self.play(
            t.animate.set_value(4 * PI),
            run_time=8,
            rate_func=linear
        )

        # =====================================================================
        # PHASE 4: EXPLAIN - Add formula
        # =====================================================================

        formula = Text("angle(t) = A * sin(w*t)", font_size=24, color=HIGHLIGHT_COLOR)
        formula.to_corner(DR)

        self.play(Write(formula))
        self.wait(2)
