"""
Visual Proofs of the Pythagorean Theorem
Multiple animated proofs showing a² + b² = c²
"""

from manim import (
    Scene,
    VGroup,
    Polygon,
    Square,
    Line,
    Text,
    MathTex,
    Tex,
    Dot,
    Arrow,
    Brace,
    Create,
    Write,
    FadeIn,
    FadeOut,
    Transform,
    ReplacementTransform,
    Indicate,
    AnimationGroup,
    Rotate,
    Circumscribe,
    BLUE,
    RED,
    GREEN,
    YELLOW,
    ORANGE,
    PURPLE,
    WHITE,
    GREY,
    PINK,
    TEAL,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    PI,
    np,
    config,
)


class PythagoreanIntro(Scene):
    """
    Introduction to the Pythagorean Theorem with a simple right triangle.
    """

    def construct(self):
        title = Text("The Pythagorean Theorem", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Create a right triangle
        a, b = 2, 3
        c = np.sqrt(a**2 + b**2)

        triangle = Polygon(
            ORIGIN,
            RIGHT * a,
            RIGHT * a + UP * b,
            color=WHITE,
            fill_color=BLUE,
            fill_opacity=0.3,
            stroke_width=3,
        )
        triangle.move_to(ORIGIN)

        self.play(Create(triangle))

        # Label the sides
        # Side a (bottom)
        brace_a = Brace(Line(triangle.get_vertices()[0], triangle.get_vertices()[1]), DOWN)
        label_a = MathTex("a", font_size=32, color=GREEN)
        label_a.next_to(brace_a, DOWN)

        # Side b (right)
        brace_b = Brace(Line(triangle.get_vertices()[1], triangle.get_vertices()[2]), RIGHT)
        label_b = MathTex("b", font_size=32, color=RED)
        label_b.next_to(brace_b, RIGHT)

        # Side c (hypotenuse)
        label_c = MathTex("c", font_size=32, color=YELLOW)
        hyp_center = (triangle.get_vertices()[0] + triangle.get_vertices()[2]) / 2
        label_c.move_to(hyp_center + LEFT * 0.4 + UP * 0.2)

        self.play(
            FadeIn(brace_a),
            Write(label_a),
            FadeIn(brace_b),
            Write(label_b),
            Write(label_c),
        )

        # Right angle marker
        right_angle = Square(side_length=0.3, color=WHITE, fill_opacity=0)
        right_angle.move_to(triangle.get_vertices()[1] + LEFT * 0.15 + UP * 0.15)
        self.play(Create(right_angle))

        self.wait(1)

        # The theorem
        theorem = MathTex(r"a^2 + b^2 = c^2", font_size=48, color=YELLOW)
        theorem.to_edge(DOWN)
        self.play(Write(theorem))

        self.wait(2)


class BhaskaraProof(Scene):
    """
    Bhaskara's proof: Dissect the square on the hypotenuse
    into 4 triangles plus a smaller square.
    "Behold!" proof
    """

    def construct(self):
        title = Text("Bhaskara's Proof", font_size=36)
        subtitle = Text('"Behold!"', font_size=28, color=YELLOW)
        title.to_edge(UP)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), Write(subtitle))

        # Triangle dimensions
        a, b = 1.5, 2.0
        c = np.sqrt(a**2 + b**2)

        # Create the large square with side c
        # Position it on the left side
        large_square_center = LEFT * 2.5

        # The four triangles arranged inside the c-square
        # Each triangle has legs a and b
        # They fit around a central square of side (b-a)

        def create_right_triangle(a, b, color):
            return Polygon(
                ORIGIN,
                RIGHT * a,
                RIGHT * a + UP * b,
                color=WHITE,
                fill_color=color,
                fill_opacity=0.7,
                stroke_width=2,
            )

        # Create 4 triangles
        colors = [BLUE, GREEN, ORANGE, PURPLE]
        triangles = VGroup()

        for i, color in enumerate(colors):
            t = create_right_triangle(a, b, color)
            triangles.add(t)

        # Arrange triangles in the Bhaskara configuration
        # Triangle 0: bottom left corner, pointing up-right
        triangles[0].move_to(large_square_center + LEFT * c / 2 + DOWN * c / 2, aligned_edge=LEFT + DOWN)

        # Triangle 1: bottom right, rotated 90° CCW
        triangles[1].rotate(PI / 2, about_point=ORIGIN)
        triangles[1].move_to(large_square_center + RIGHT * c / 2 + DOWN * c / 2, aligned_edge=RIGHT + DOWN)

        # Triangle 2: top right, rotated 180°
        triangles[2].rotate(PI, about_point=ORIGIN)
        triangles[2].move_to(large_square_center + RIGHT * c / 2 + UP * c / 2, aligned_edge=RIGHT + UP)

        # Triangle 3: top left, rotated 270° (or -90°)
        triangles[3].rotate(-PI / 2, about_point=ORIGIN)
        triangles[3].move_to(large_square_center + LEFT * c / 2 + UP * c / 2, aligned_edge=LEFT + UP)

        # Inner square of side |b - a|
        inner_side = abs(b - a)
        inner_square = Square(
            side_length=inner_side,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.7,
            stroke_width=2,
        )
        inner_square.move_to(large_square_center)

        # Outer square (boundary of c-square)
        outer_square = Square(side_length=c, color=WHITE, stroke_width=3)
        outer_square.move_to(large_square_center)

        # Labels
        c_label = MathTex("c", font_size=28)
        c_label.next_to(outer_square, DOWN)

        self.play(Create(outer_square), Write(c_label))
        self.wait(0.5)

        self.play(
            AnimationGroup(*[FadeIn(t) for t in triangles], lag_ratio=0.3),
        )
        self.play(FadeIn(inner_square))
        self.wait(1)

        # Area equation on the right
        equation_title = Text("Area of c² square:", font_size=24)
        equation_title.to_edge(RIGHT).shift(UP * 2)

        area_eq = MathTex(
            r"c^2 = 4 \cdot \frac{1}{2}ab + (b-a)^2", font_size=28
        )
        area_eq.next_to(equation_title, DOWN, buff=0.5)

        self.play(Write(equation_title))
        self.play(Write(area_eq))

        # Simplify
        step1 = MathTex(r"c^2 = 2ab + b^2 - 2ab + a^2", font_size=28)
        step1.next_to(area_eq, DOWN, buff=0.3)

        step2 = MathTex(r"c^2 = a^2 + b^2", font_size=32, color=YELLOW)
        step2.next_to(step1, DOWN, buff=0.3)

        self.play(Write(step1))
        self.wait(0.5)
        self.play(Write(step2))

        self.play(Circumscribe(step2, color=YELLOW))
        self.wait(2)


class RearrangementProof(Scene):
    """
    Classic rearrangement proof:
    Two squares of side (a+b) partitioned differently
    to show a² + b² = c²
    """

    def construct(self):
        title = Text("Rearrangement Proof", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Dimensions
        a, b = 1.2, 1.8
        c = np.sqrt(a**2 + b**2)
        total = a + b

        # Left configuration: (a+b)² square with 4 triangles + a² + b² squares
        left_center = LEFT * 3.5

        # Create the outer square
        left_outer = Square(side_length=total, color=WHITE, stroke_width=2)
        left_outer.move_to(left_center)

        # Create the triangles for left configuration
        def right_triangle(a, b, color):
            return Polygon(
                ORIGIN,
                RIGHT * a,
                UP * b,
                color=WHITE,
                fill_color=color,
                fill_opacity=0.7,
                stroke_width=1.5,
            )

        left_triangles = VGroup()
        tri_colors = [BLUE, GREEN, ORANGE, PURPLE]

        for color in tri_colors:
            left_triangles.add(right_triangle(a, b, color))

        # Position triangles in corners
        # Bottom-left corner: triangle pointing up-right
        left_triangles[0].move_to(
            left_center + LEFT * total / 2 + DOWN * total / 2, aligned_edge=LEFT + DOWN
        )

        # Bottom-right corner: rotated 90° CW
        left_triangles[1].rotate(-PI / 2)
        left_triangles[1].move_to(
            left_center + RIGHT * total / 2 + DOWN * total / 2, aligned_edge=RIGHT + DOWN
        )

        # Top-right corner: rotated 180°
        left_triangles[2].rotate(PI)
        left_triangles[2].move_to(
            left_center + RIGHT * total / 2 + UP * total / 2, aligned_edge=RIGHT + UP
        )

        # Top-left corner: rotated 90° CCW
        left_triangles[3].rotate(PI / 2)
        left_triangles[3].move_to(
            left_center + LEFT * total / 2 + UP * total / 2, aligned_edge=LEFT + UP
        )

        # a² square in top-left area
        a_square = Square(side_length=a, color=RED, fill_color=RED, fill_opacity=0.5)
        a_square.move_to(left_center + LEFT * b / 2 + UP * b / 2)

        # b² square in bottom-right area
        b_square = Square(side_length=b, color=TEAL, fill_color=TEAL, fill_opacity=0.5)
        b_square.move_to(left_center + RIGHT * a / 2 + DOWN * a / 2)

        # Labels for left config
        left_label = Text("Configuration 1", font_size=22)
        left_label.next_to(left_outer, DOWN, buff=0.3)

        a_label = MathTex("a^2", font_size=24, color=RED)
        a_label.move_to(a_square.get_center())

        b_label = MathTex("b^2", font_size=24, color=TEAL)
        b_label.move_to(b_square.get_center())

        # Right configuration: (a+b)² square with 4 triangles + c² square
        right_center = RIGHT * 3.5

        right_outer = Square(side_length=total, color=WHITE, stroke_width=2)
        right_outer.move_to(right_center)

        right_triangles = VGroup()
        for color in tri_colors:
            right_triangles.add(right_triangle(a, b, color))

        # Bhaskara arrangement (tilted c² square in center)
        # This creates a tilted square of side c with triangles in corners

        # The four triangles around a tilted c-square
        # Bottom-left: base along bottom, height going right
        right_triangles[0].move_to(
            right_center + LEFT * total / 2 + DOWN * total / 2, aligned_edge=LEFT + DOWN
        )

        # Bottom-right: base along right side, height going up
        right_triangles[1].rotate(-PI / 2)
        right_triangles[1].move_to(
            right_center + RIGHT * total / 2 + DOWN * total / 2, aligned_edge=RIGHT + DOWN
        )

        # Top-right: upside down
        right_triangles[2].rotate(PI)
        right_triangles[2].move_to(
            right_center + RIGHT * total / 2 + UP * total / 2, aligned_edge=RIGHT + UP
        )

        # Top-left
        right_triangles[3].rotate(PI / 2)
        right_triangles[3].move_to(
            right_center + LEFT * total / 2 + UP * total / 2, aligned_edge=LEFT + UP
        )

        # Wait - for classic rearrangement, we need a different arrangement
        # Let me redo the right side properly
        # In the second configuration, the 4 triangles surround a c² square

        # Actually let me create the c² square (tilted 45°-ish inside)
        # The tilted c-square has vertices at:
        # (a, 0), (a+b, a), (b, a+b), (0, b) relative to bottom-left of outer square

        c_square = Polygon(
            right_center + LEFT * total / 2 + DOWN * total / 2 + RIGHT * a,  # bottom vertex
            right_center + LEFT * total / 2 + DOWN * total / 2 + RIGHT * total + UP * a,  # right vertex
            right_center + LEFT * total / 2 + DOWN * total / 2 + RIGHT * b + UP * total,  # top vertex
            right_center + LEFT * total / 2 + DOWN * total / 2 + UP * b,  # left vertex
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.5,
            stroke_width=2,
        )

        right_label = Text("Configuration 2", font_size=22)
        right_label.next_to(right_outer, DOWN, buff=0.3)

        c_label = MathTex("c^2", font_size=28, color=YELLOW)
        c_label.move_to(right_center)

        # Show left configuration
        self.play(Create(left_outer))
        self.play(*[FadeIn(t) for t in left_triangles])
        self.play(FadeIn(a_square), FadeIn(b_square))
        self.play(Write(a_label), Write(b_label), Write(left_label))
        self.wait(1)

        # Show right configuration
        self.play(Create(right_outer))
        self.play(*[FadeIn(t) for t in right_triangles])
        self.play(FadeIn(c_square))
        self.play(Write(c_label), Write(right_label))
        self.wait(1)

        # The key insight
        equation1 = MathTex(
            r"\text{Same outer square } (a+b)^2", font_size=28
        )
        equation1.to_edge(DOWN).shift(UP * 1.5)

        equation2 = MathTex(
            r"\text{Same 4 triangles}", font_size=28
        )
        equation2.next_to(equation1, DOWN, buff=0.2)

        equation3 = MathTex(
            r"\Rightarrow a^2 + b^2 = c^2", font_size=36, color=YELLOW
        )
        equation3.next_to(equation2, DOWN, buff=0.3)

        self.play(Write(equation1))
        self.play(Write(equation2))
        self.play(Write(equation3))

        self.play(Circumscribe(equation3, color=YELLOW))
        self.wait(2)


class AreaBasedProof(Scene):
    """
    Direct area comparison: Build squares on each side of the triangle.
    """

    def construct(self):
        title = Text("Area-Based Proof", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Triangle dimensions
        a, b = 2.0, 1.5
        c = np.sqrt(a**2 + b**2)

        # Create the right triangle
        triangle = Polygon(
            ORIGIN,
            RIGHT * a,
            RIGHT * a + UP * b,
            color=WHITE,
            fill_color=GREY,
            fill_opacity=0.3,
            stroke_width=3,
        )
        triangle.move_to(LEFT * 1)

        # Get actual vertices after moving
        v0 = triangle.get_vertices()[0]  # origin
        v1 = triangle.get_vertices()[1]  # right
        v2 = triangle.get_vertices()[2]  # top-right

        self.play(Create(triangle))
        self.wait(0.5)

        # Square on side a (bottom)
        a_square = Square(side_length=a, color=GREEN, fill_color=GREEN, fill_opacity=0.5)
        a_square.next_to(Line(v0, v1), DOWN, buff=0)
        a_label = MathTex(r"a^2", font_size=28, color=GREEN)
        a_label.move_to(a_square.get_center())

        # Square on side b (right)
        b_square = Square(side_length=b, color=RED, fill_color=RED, fill_opacity=0.5)
        b_square.next_to(Line(v1, v2), RIGHT, buff=0)
        b_label = MathTex(r"b^2", font_size=28, color=RED)
        b_label.move_to(b_square.get_center())

        # Square on side c (hypotenuse) - needs rotation
        c_square = Square(side_length=c, color=YELLOW, fill_color=YELLOW, fill_opacity=0.5)
        # Calculate rotation angle of hypotenuse
        angle = np.arctan2(b, -a)  # angle from v2 to v0
        c_square.rotate(angle + PI / 2)  # perpendicular to hypotenuse

        # Position it along the hypotenuse (outside the triangle)
        hyp_center = (v0 + v2) / 2
        hyp_direction = (v0 - v2) / np.linalg.norm(v0 - v2)
        perp_direction = np.array([-hyp_direction[1], hyp_direction[0], 0])
        c_square.move_to(hyp_center + perp_direction * c / 2)

        c_label = MathTex(r"c^2", font_size=28, color=YELLOW)
        c_label.move_to(c_square.get_center())

        # Animate adding squares
        self.play(FadeIn(a_square), Write(a_label))
        self.wait(0.5)
        self.play(FadeIn(b_square), Write(b_label))
        self.wait(0.5)
        self.play(FadeIn(c_square), Write(c_label))
        self.wait(1)

        # Show the equation
        equation = MathTex(
            r"\text{Area}(a^2) + \text{Area}(b^2) = \text{Area}(c^2)",
            font_size=28,
        )
        equation.to_edge(DOWN).shift(UP * 0.8)

        final = MathTex(r"a^2 + b^2 = c^2", font_size=40, color=YELLOW)
        final.next_to(equation, DOWN, buff=0.3)

        self.play(Write(equation))
        self.play(Write(final))

        self.play(Circumscribe(final, color=YELLOW))
        self.wait(2)


class EuclideanProof(Scene):
    """
    Euclid's proof using similar triangles and altitude to hypotenuse.
    """

    def construct(self):
        title = Text("Euclid's Proof (Similar Triangles)", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Triangle dimensions
        a, b = 3, 2
        c = np.sqrt(a**2 + b**2)

        # Main triangle ABC: right angle at C
        A = LEFT * 3 + DOWN * 1
        B = RIGHT * 2 + DOWN * 1
        C = LEFT * 3 + UP * 2  # Wait, let me reconsider

        # Actually, standard configuration:
        # Right angle at bottom-left, base along bottom
        base_left = LEFT * 2.5 + DOWN * 0.5
        base_right = base_left + RIGHT * a
        top_right = base_left + RIGHT * a + UP * b

        A = base_left  # left vertex
        B = base_right  # right vertex (bottom)
        C = top_right  # top vertex

        triangle = Polygon(
            A, B, C,
            color=WHITE,
            fill_color=BLUE,
            fill_opacity=0.2,
            stroke_width=3,
        )

        self.play(Create(triangle))

        # Labels
        label_A = MathTex("A", font_size=24).next_to(A, LEFT)
        label_B = MathTex("B", font_size=24).next_to(B, RIGHT)
        label_C = MathTex("C", font_size=24).next_to(C, UP)

        self.play(Write(label_A), Write(label_B), Write(label_C))

        # Draw altitude from B to AC (hypotenuse)
        # The foot of the altitude H is where the perpendicular from B meets AC
        # For a right triangle with right angle at B:
        # Actually, let me reconfigure. Right angle should be at B for standard setup.

        # Let's redo: Right triangle with right angle at B
        # A at left, B at bottom-middle (right angle), C at right

        self.clear()
        self.play(Write(title))

        # Reconfigure
        A = LEFT * 3 + UP * 1.5
        B = ORIGIN + DOWN * 1
        C = RIGHT * 2 + UP * 2

        # Actually, for Euclid's proof, the setup is:
        # Right triangle with right angle at C (vertex opposite hypotenuse)
        # Altitude from C to hypotenuse AB

        # Simpler setup
        A = LEFT * 2 + DOWN * 1
        C = LEFT * 2 + UP * 1.5  # Right angle vertex
        B = RIGHT * 2 + DOWN * 1

        triangle2 = Polygon(
            A, C, B,
            color=WHITE,
            fill_color=BLUE,
            fill_opacity=0.2,
            stroke_width=3,
        )

        self.play(Create(triangle2))

        label_A = MathTex("A", font_size=24).next_to(A, DOWN + LEFT)
        label_B = MathTex("B", font_size=24).next_to(B, DOWN + RIGHT)
        label_C = MathTex("C", font_size=24).next_to(C, UP)

        self.play(Write(label_A), Write(label_B), Write(label_C))

        # Right angle marker at C
        right_angle = Square(side_length=0.25, color=WHITE, fill_opacity=0)
        right_angle.move_to(C + DOWN * 0.125 + RIGHT * 0.125)
        self.play(Create(right_angle))

        # Altitude from C to AB
        # Find foot of altitude H
        AB = B - A
        AC = C - A
        t = np.dot(AC, AB) / np.dot(AB, AB)
        H = A + t * AB

        altitude = Line(C, H, color=YELLOW, stroke_width=3)
        label_H = MathTex("H", font_size=24).next_to(H, DOWN)

        self.play(Create(altitude), Write(label_H))

        # Highlight the three similar triangles
        explanation = VGroup(
            Text("Three similar triangles:", font_size=22),
            MathTex(r"\triangle ACB \sim \triangle AHC \sim \triangle CHB", font_size=24),
        )
        explanation.arrange(DOWN, buff=0.2)
        explanation.to_edge(RIGHT).shift(UP * 0.5)

        self.play(Write(explanation))
        self.wait(1)

        # Show the proportions
        props = VGroup(
            MathTex(r"\frac{AC}{AB} = \frac{AH}{AC}", font_size=24, color=GREEN),
            MathTex(r"\Rightarrow AC^2 = AB \cdot AH", font_size=24, color=GREEN),
            MathTex(r"\frac{BC}{AB} = \frac{BH}{BC}", font_size=24, color=RED),
            MathTex(r"\Rightarrow BC^2 = AB \cdot BH", font_size=24, color=RED),
        )
        props.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        props.to_edge(RIGHT).shift(DOWN * 1.5)

        self.play(Write(props[0]))
        self.play(Write(props[1]))
        self.wait(0.5)
        self.play(Write(props[2]))
        self.play(Write(props[3]))
        self.wait(1)

        # Final step
        final = VGroup(
            MathTex(r"AC^2 + BC^2 = AB(AH + BH) = AB^2", font_size=26),
            MathTex(r"a^2 + b^2 = c^2", font_size=36, color=YELLOW),
        )
        final.arrange(DOWN, buff=0.3)
        final.to_edge(DOWN)

        self.play(Write(final[0]))
        self.play(Write(final[1]))

        self.play(Circumscribe(final[1], color=YELLOW))
        self.wait(2)


class PresidentialProof(Scene):
    """
    James Garfield's trapezoid proof (before he became US President).
    """

    def construct(self):
        title = Text("Garfield's Trapezoid Proof", font_size=32)
        subtitle = Text("(James A. Garfield, 1876)", font_size=20, color=GREY)
        title.to_edge(UP)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), Write(subtitle))

        # Create a trapezoid from two copies of a right triangle and a half-square
        a, b = 1.5, 2.0

        # The trapezoid has:
        # - Base 1: length a+b (bottom)
        # - Base 2: length 0 (top is a point)
        # Actually, Garfield's trapezoid has parallel sides of length a and b

        # Correct construction:
        # Take right triangle with legs a, b
        # Put two of them together with a right isosceles triangle between

        # Vertices of trapezoid (going counterclockwise from bottom-left)
        v0 = ORIGIN  # bottom-left
        v1 = RIGHT * (a + b)  # bottom-right
        v2 = RIGHT * (a + b) + UP * a  # top-right
        v3 = UP * b  # top-left

        trapezoid = Polygon(
            v0, v1, v2, v3,
            color=WHITE,
            stroke_width=2,
        )
        trapezoid.move_to(LEFT * 1)

        # Get moved vertices
        vertices = trapezoid.get_vertices()
        v0, v1, v2, v3 = vertices

        self.play(Create(trapezoid))

        # First right triangle (bottom-left)
        tri1 = Polygon(
            v0, v0 + RIGHT * a, v3,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_width=2,
        )

        # Second right triangle (bottom-right portion)
        # From v0 + RIGHT*a to v1 to v2
        tri2 = Polygon(
            v0 + RIGHT * a, v1, v2,
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.5,
            stroke_width=2,
        )

        # Middle right triangle (on hypotenuse)
        tri3 = Polygon(
            v3, v0 + RIGHT * a, v2,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.5,
            stroke_width=2,
        )

        self.play(FadeIn(tri1), FadeIn(tri2), FadeIn(tri3))

        # Labels
        label_a1 = MathTex("a", font_size=20, color=BLUE)
        label_a1.next_to(Line(v0, v0 + RIGHT * a), DOWN, buff=0.1)

        label_b1 = MathTex("b", font_size=20, color=BLUE)
        label_b1.next_to(Line(v0, v3), LEFT, buff=0.1)

        label_a2 = MathTex("a", font_size=20, color=GREEN)
        label_a2.next_to(Line(v1, v2), RIGHT, buff=0.1)

        label_b2 = MathTex("b", font_size=20, color=GREEN)
        label_b2.next_to(Line(v0 + RIGHT * a, v1), DOWN, buff=0.1)

        label_c1 = MathTex("c", font_size=20, color=YELLOW)
        mid1 = (v3 + v0 + RIGHT * a) / 2
        label_c1.move_to(mid1 + LEFT * 0.2 + UP * 0.1)

        label_c2 = MathTex("c", font_size=20, color=YELLOW)
        mid2 = (v0 + RIGHT * a + v2) / 2
        label_c2.move_to(mid2 + RIGHT * 0.1 + DOWN * 0.1)

        self.play(
            Write(label_a1), Write(label_b1),
            Write(label_a2), Write(label_b2),
            Write(label_c1), Write(label_c2),
        )
        self.wait(1)

        # Area calculations
        area_trap = MathTex(
            r"\text{Trapezoid area} = \frac{1}{2}(a+b)(a+b) = \frac{(a+b)^2}{2}",
            font_size=24,
        )
        area_trap.to_edge(RIGHT).shift(UP * 1)

        area_tris = MathTex(
            r"\text{Triangle areas} = \frac{ab}{2} + \frac{ab}{2} + \frac{c^2}{2}",
            font_size=24,
        )
        area_tris.next_to(area_trap, DOWN, buff=0.5)

        self.play(Write(area_trap))
        self.play(Write(area_tris))
        self.wait(1)

        # Equate
        equation = MathTex(
            r"\frac{(a+b)^2}{2} = ab + \frac{c^2}{2}",
            font_size=28,
        )
        equation.next_to(area_tris, DOWN, buff=0.5)

        step2 = MathTex(
            r"a^2 + 2ab + b^2 = 2ab + c^2",
            font_size=28,
        )
        step2.next_to(equation, DOWN, buff=0.3)

        result = MathTex(r"a^2 + b^2 = c^2", font_size=36, color=YELLOW)
        result.next_to(step2, DOWN, buff=0.3)

        self.play(Write(equation))
        self.play(Write(step2))
        self.play(Write(result))

        self.play(Circumscribe(result, color=YELLOW))
        self.wait(2)


class AnimatedProofSummary(Scene):
    """
    Quick animated summary showing the theorem visually.
    """

    def construct(self):
        title = Text("The Pythagorean Theorem", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Create animated squares on triangle sides
        a, b = 2, 1.5
        c = np.sqrt(a**2 + b**2)

        # Triangle
        A = LEFT * 2 + DOWN * 1
        B = A + RIGHT * a
        C = B + UP * b

        triangle = Polygon(A, B, C, color=WHITE, stroke_width=3)
        self.play(Create(triangle))

        # Squares on each side with animation
        square_a = Square(side_length=a, color=GREEN, fill_color=GREEN, fill_opacity=0.6)
        square_a.next_to(Line(A, B), DOWN, buff=0)

        square_b = Square(side_length=b, color=RED, fill_color=RED, fill_opacity=0.6)
        square_b.next_to(Line(B, C), RIGHT, buff=0)

        # c-square needs rotation
        angle = np.arctan2(C[1] - A[1], C[0] - A[0])
        square_c = Square(side_length=c, color=YELLOW, fill_color=YELLOW, fill_opacity=0.6)
        square_c.rotate(angle)
        # Position perpendicular to hypotenuse
        hyp_mid = (A + C) / 2
        perp = np.array([-(C[1] - A[1]), C[0] - A[0], 0])
        perp = perp / np.linalg.norm(perp)
        square_c.move_to(hyp_mid + perp * c / 2)

        # Animate squares growing from sides
        self.play(FadeIn(square_a, scale=0.5))
        self.play(FadeIn(square_b, scale=0.5))
        self.play(FadeIn(square_c, scale=0.5))

        # Labels
        a_label = MathTex(f"a^2 = {a**2:.1f}", font_size=24, color=WHITE)
        a_label.move_to(square_a.get_center())

        b_label = MathTex(f"b^2 = {b**2:.2f}", font_size=24, color=WHITE)
        b_label.move_to(square_b.get_center())

        c_label = MathTex(f"c^2 = {c**2:.2f}", font_size=24, color=WHITE)
        c_label.move_to(square_c.get_center())

        self.play(Write(a_label), Write(b_label), Write(c_label))

        # The equation
        equation = MathTex(
            f"{a**2:.1f} + {b**2:.2f} = {c**2:.2f}",
            font_size=32,
        )
        equation.to_edge(DOWN).shift(UP * 0.5)

        final = MathTex(r"a^2 + b^2 = c^2", font_size=48, color=YELLOW)
        final.next_to(equation, DOWN, buff=0.3)

        self.play(Write(equation))
        self.play(Write(final))

        self.play(Indicate(square_a), Indicate(square_b))
        self.wait(0.5)
        self.play(Indicate(square_c))

        self.wait(2)
