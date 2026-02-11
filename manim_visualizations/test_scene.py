"""
Simple test scene without LaTeX dependencies.
Uses only shapes and basic text to verify rendering pipeline.
"""

from manim import (
    VGroup,
    Square,
    Circle,
    Triangle,
    Arrow,
    Line,
    Polygon,
    Text,
    NumberPlane,
    Create,
    FadeIn,
    FadeOut,
    Transform,
    Rotate,
    Indicate,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    PI,
    np,
)

from themed_scene import ThemedScene


class SimpleTransformTest(ThemedScene):
    """Test linear transformation without LaTeX."""

    def construct(self):
        t = self.theme

        # Title using plain Text (no LaTeX needed)
        title = Text("Linear Transformation Demo", font_size=t.subtitle_size)
        title.to_edge(UP)
        self.play(Create(title))

        # Create a grid
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.4},
        )
        self.play(Create(plane), run_time=1.5)

        # Basis vectors as arrows
        i_hat = Arrow(ORIGIN, RIGHT * 2, buff=0, color=t.tertiary, stroke_width=t.heavy_stroke_width)
        j_hat = Arrow(ORIGIN, UP * 2, buff=0, color=t.secondary, stroke_width=t.heavy_stroke_width)

        i_label = Text("i", font_size=t.body_size, color=t.tertiary).next_to(i_hat, DOWN)
        j_label = Text("j", font_size=t.body_size, color=t.secondary).next_to(j_hat, LEFT)

        self.play(Create(i_hat), Create(j_hat))
        self.play(FadeIn(i_label), FadeIn(j_label))
        self.wait(0.5)

        # A unit square to show transformation
        square = Square(side_length=2, color=t.accent, fill_opacity=t.shape_fill_opacity)
        square.move_to(RIGHT + UP)
        self.play(FadeIn(square))
        self.wait(0.5)

        # Apply a shear transformation
        shear_matrix = np.array([[1, 0.5], [0, 1]])

        group = VGroup(plane, i_hat, j_hat, square)
        self.play(
            group.animate.apply_matrix(shear_matrix),
            FadeOut(i_label),
            FadeOut(j_label),
            run_time=2,
        )

        # New label
        result = Text("Shear Transform Applied!", font_size=t.body_size, color=t.accent)
        result.to_edge(DOWN)
        self.play(FadeIn(result))
        self.wait(1)


class PythagoreanShapesTest(ThemedScene):
    """Test Pythagorean visualization with shapes only."""

    def construct(self):
        t = self.theme

        title = Text("Pythagorean Theorem", font_size=t.title_size)
        self.play(Create(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))

        # Create right triangle
        a, b = 2, 1.5
        c = np.sqrt(a**2 + b**2)

        # Triangle vertices
        A = LEFT * 2 + DOWN * 1
        B = A + RIGHT * a
        C = B + UP * b

        triangle = Polygon(
            A, B, C,
            color=t.foreground,
            fill_color=t.primary,
            fill_opacity=t.shape_fill_opacity,
            stroke_width=t.curve_stroke_width,
        )
        self.play(Create(triangle))

        # Right angle marker
        right_marker = Square(side_length=0.25, color=t.foreground)
        right_marker.move_to(B + LEFT * 0.125 + UP * 0.125)
        self.play(Create(right_marker))

        # Square on side a (bottom)
        square_a = Square(side_length=a, color=t.tertiary, fill_color=t.tertiary, fill_opacity=t.area_fill_opacity)
        square_a.next_to(Line(A, B), DOWN, buff=0)
        label_a = Text("a²", font_size=t.label_size, color=t.foreground)
        label_a.move_to(square_a.get_center())

        self.play(FadeIn(square_a), FadeIn(label_a))

        # Square on side b (right)
        square_b = Square(side_length=b, color=t.secondary, fill_color=t.secondary, fill_opacity=t.area_fill_opacity)
        square_b.next_to(Line(B, C), RIGHT, buff=0)
        label_b = Text("b²", font_size=t.label_size, color=t.foreground)
        label_b.move_to(square_b.get_center())

        self.play(FadeIn(square_b), FadeIn(label_b))

        # Square on hypotenuse
        angle = np.arctan2(C[1] - A[1], C[0] - A[0])
        square_c = Square(side_length=c, color=t.accent, fill_color=t.accent, fill_opacity=t.area_fill_opacity)
        square_c.rotate(angle)
        hyp_mid = (A + C) / 2
        perp = np.array([-(C[1] - A[1]), C[0] - A[0], 0])
        perp = perp / np.linalg.norm(perp)
        square_c.move_to(hyp_mid + perp * c / 2)
        label_c = Text("c²", font_size=t.label_size, color=t.foreground)
        label_c.move_to(square_c.get_center())

        self.play(FadeIn(square_c), FadeIn(label_c))

        # Highlight
        self.play(Indicate(square_a), Indicate(square_b))
        self.wait(0.3)
        self.play(Indicate(square_c))

        # Result text
        result = Text("a² + b² = c²", font_size=t.subtitle_size, color=t.accent)
        result.to_edge(DOWN)
        self.play(FadeIn(result))
        self.wait(1)


class DerivativeShapesTest(ThemedScene):
    """Test derivative visualization with shapes."""

    def construct(self):
        t = self.theme

        title = Text("Tangent Line = Derivative", font_size=t.body_size + 4)
        title.to_edge(UP)
        self.play(Create(title))

        # Create axes manually with lines
        x_axis = Arrow(LEFT * 5, RIGHT * 5, buff=0, color=t.foreground, stroke_width=t.axis_stroke_width)
        y_axis = Arrow(DOWN * 3, UP * 3, buff=0, color=t.foreground, stroke_width=t.axis_stroke_width)

        self.play(Create(x_axis), Create(y_axis))

        # Plot points for x^2 curve (approximated with line segments)
        x_vals = np.linspace(-2, 2, 50)
        y_vals = x_vals**2

        # Scale for display
        points = [np.array([x * 1.5, y * 0.5, 0]) for x, y in zip(x_vals, y_vals)]

        # Create curve from line segments
        curve_lines = VGroup()
        for i in range(len(points) - 1):
            line = Line(points[i], points[i + 1], color=t.primary, stroke_width=t.curve_stroke_width)
            curve_lines.add(line)

        self.play(Create(curve_lines), run_time=2)

        # Add a point on the curve
        x_point = 1.0
        y_point = x_point**2
        point = Circle(radius=0.1, color=t.accent, fill_opacity=1)
        point.move_to(np.array([x_point * 1.5, y_point * 0.5, 0]))

        self.play(FadeIn(point))

        # Tangent line at x=1 (derivative = 2x = 2)
        slope = 2 * x_point
        # Line through (1.5, 0.5) with slope 2 * (0.5/1.5) = 2/3 in display coords
        display_slope = slope * (0.5 / 1.5)

        tangent_start = np.array([0, 0.5 - 1.5 * display_slope, 0])
        tangent_end = np.array([3, 0.5 + 1.5 * display_slope, 0])
        tangent = Line(tangent_start, tangent_end, color=t.secondary, stroke_width=t.curve_stroke_width)

        self.play(Create(tangent))

        # Label
        slope_text = Text("Slope = 2 (derivative at x=1)", font_size=t.label_size, color=t.secondary)
        slope_text.to_edge(DOWN)
        self.play(FadeIn(slope_text))

        self.wait(1)
