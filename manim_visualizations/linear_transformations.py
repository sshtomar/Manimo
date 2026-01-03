"""
Matrix Multiplication and Linear Transformations Visualizations
Inspired by 3Blue1Brown and Gilbert Strang's intuitive approach
"""

from manim import (
    Scene,
    VGroup,
    Vector,
    Matrix,
    NumberPlane,
    Arrow,
    Text,
    MathTex,
    Dot,
    Square,
    LinearTransformationScene,
    ApplyMatrix,
    Write,
    FadeIn,
    FadeOut,
    Create,
    Transform,
    ReplacementTransform,
    Indicate,
    MoveToTarget,
    Wait,
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
    ORIGIN,
    PI,
    TAU,
    np,
    config,
)


class LinearTransformationIntro(LinearTransformationScene):
    """
    Visualize how a 2x2 matrix transforms the entire 2D plane.
    Shows basis vectors i-hat and j-hat being transformed.
    """

    def __init__(self, **kwargs):
        super().__init__(
            show_coordinates=True,
            leave_ghost_vectors=True,
            show_basis_vectors=True,
            **kwargs,
        )

    def construct(self):
        # Title
        title = Text("Linear Transformations", font_size=36)
        title.to_corner(UP + LEFT)
        self.add_foreground_mobject(title)

        # The transformation matrix
        matrix = [[2, 1], [1, 2]]

        # Add some vectors to show how they transform
        v1 = self.add_vector([1, 1], color=YELLOW)
        v2 = self.add_vector([-1, 1], color=ORANGE)

        self.wait(1)

        # Show the matrix
        matrix_tex = MathTex(
            r"\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}", font_size=36
        )
        matrix_tex.to_corner(UP + RIGHT)
        matrix_tex.add_background_rectangle()
        self.play(Write(matrix_tex))

        self.wait(1)

        # Apply the transformation
        self.apply_matrix(matrix)

        self.wait(2)


class BasisVectorTransformation(Scene):
    """
    Show how matrix columns represent where basis vectors land.
    Core insight: columns of matrix = transformed basis vectors.
    """

    def construct(self):
        # Create coordinate plane
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.4},
        )
        self.play(Create(plane))

        # Basis vectors
        i_hat = Arrow(ORIGIN, RIGHT * 2, buff=0, color=GREEN, stroke_width=6)
        j_hat = Arrow(ORIGIN, UP * 2, buff=0, color=RED, stroke_width=6)

        i_label = MathTex(r"\hat{i}", color=GREEN).next_to(i_hat, DOWN)
        j_label = MathTex(r"\hat{j}", color=RED).next_to(j_hat, LEFT)

        self.play(Create(i_hat), Create(j_hat))
        self.play(Write(i_label), Write(j_label))
        self.wait(1)

        # Show the insight
        insight = Text(
            "Matrix columns = Where basis vectors land", font_size=28, color=YELLOW
        )
        insight.to_edge(UP)
        self.play(Write(insight))

        # Matrix
        matrix = [[2, -1], [1, 1]]
        matrix_mob = MathTex(
            r"\begin{bmatrix} 2 & -1 \\ 1 & 1 \end{bmatrix}", font_size=42
        )
        matrix_mob.to_corner(UP + RIGHT)

        col1 = MathTex(r"\begin{bmatrix} 2 \\ 1 \end{bmatrix}", color=GREEN)
        col2 = MathTex(r"\begin{bmatrix} -1 \\ 1 \end{bmatrix}", color=RED)
        col1.next_to(matrix_mob, DOWN, buff=0.5)
        col2.next_to(col1, RIGHT, buff=1)

        self.play(Write(matrix_mob))
        self.wait(1)

        # Transform basis vectors
        new_i = Arrow(ORIGIN, RIGHT * 2 + UP * 1, buff=0, color=GREEN, stroke_width=6)
        new_j = Arrow(
            ORIGIN, LEFT * 1 + UP * 1, buff=0, color=RED, stroke_width=6
        )

        self.play(Transform(i_hat, new_i), FadeOut(i_label))
        self.play(Write(col1))
        self.wait(0.5)

        self.play(Transform(j_hat, new_j), FadeOut(j_label))
        self.play(Write(col2))

        # New labels
        new_i_label = MathTex(r"(2, 1)", color=GREEN, font_size=28).next_to(
            new_i.get_end(), RIGHT
        )
        new_j_label = MathTex(r"(-1, 1)", color=RED, font_size=28).next_to(
            new_j.get_end(), LEFT
        )

        self.play(Write(new_i_label), Write(new_j_label))
        self.wait(2)


class MatrixMultiplicationAsComposition(Scene):
    """
    Visualize matrix multiplication as composition of transformations.
    AB means: first apply B, then apply A.
    """

    def construct(self):
        title = Text("Matrix Multiplication = Composition", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Create plane
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            background_line_style={"stroke_opacity": 0.3},
        )
        plane.shift(LEFT * 3)
        self.play(Create(plane))

        # Vector to transform
        vec = Arrow(
            plane.get_center(),
            plane.get_center() + RIGHT + UP,
            buff=0,
            color=YELLOW,
            stroke_width=5,
        )
        vec_label = MathTex(r"\vec{v}", color=YELLOW).next_to(vec.get_end(), UR, buff=0.1)
        self.play(Create(vec), Write(vec_label))

        # Matrices
        A = MathTex(r"A = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}", font_size=28)
        A_desc = Text("90° rotation", font_size=20, color=BLUE)
        A.to_corner(UR).shift(DOWN * 0.5)
        A_desc.next_to(A, DOWN)

        B = MathTex(r"B = \begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix}", font_size=28)
        B_desc = Text("Stretch x by 2", font_size=20, color=GREEN)
        B.next_to(A_desc, DOWN, buff=0.5)
        B_desc.next_to(B, DOWN)

        self.play(Write(A), Write(A_desc))
        self.play(Write(B), Write(B_desc))
        self.wait(1)

        # First apply B (stretch)
        step1 = Text("Step 1: Apply B", font_size=24, color=GREEN)
        step1.next_to(plane, DOWN, buff=0.5)
        self.play(Write(step1))

        new_vec1 = Arrow(
            plane.get_center(),
            plane.get_center() + RIGHT * 2 + UP,
            buff=0,
            color=YELLOW,
            stroke_width=5,
        )
        self.play(Transform(vec, new_vec1))
        self.wait(1)

        # Then apply A (rotate)
        step2 = Text("Step 2: Apply A", font_size=24, color=BLUE)
        step2.next_to(step1, DOWN)
        self.play(Write(step2))

        new_vec2 = Arrow(
            plane.get_center(),
            plane.get_center() + LEFT + UP * 2,
            buff=0,
            color=YELLOW,
            stroke_width=5,
        )
        self.play(Transform(vec, new_vec2))
        self.wait(1)

        # Show the product
        product = MathTex(
            r"AB = \begin{bmatrix} 0 & -1 \\ 2 & 0 \end{bmatrix}", font_size=28
        )
        product.next_to(B_desc, DOWN, buff=0.5)

        result_text = Text("AB does both at once!", font_size=22, color=ORANGE)
        result_text.next_to(product, DOWN)

        self.play(Write(product), Write(result_text))
        self.wait(2)


class DotProductInterpretation(Scene):
    """
    Show matrix multiplication row-by-column as dot products.
    """

    def construct(self):
        title = Text("Matrix Multiply: Row × Column = Dot Product", font_size=28)
        title.to_edge(UP)
        self.play(Write(title))

        # Two matrices
        A = MathTex(
            r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}", font_size=36
        )
        B = MathTex(
            r"\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}", font_size=36
        )
        equals = MathTex(r"=", font_size=36)
        C = MathTex(r"\begin{bmatrix} ? & ? \\ ? & ? \end{bmatrix}", font_size=36)

        equation = VGroup(A, B, equals, C).arrange(RIGHT, buff=0.3)
        equation.move_to(UP * 1)
        self.play(Write(A), Write(B), Write(equals), Write(C))
        self.wait(1)

        # Highlight first row of A and first column of B
        row_highlight = Text("Row 1 of A", font_size=20, color=BLUE)
        col_highlight = Text("Col 1 of B", font_size=20, color=GREEN)
        row_highlight.next_to(A, LEFT)
        col_highlight.next_to(B, RIGHT)

        self.play(Write(row_highlight), Write(col_highlight))

        # Show the dot product calculation
        calc = MathTex(
            r"C_{11} = (1)(5) + (2)(7) = 5 + 14 = 19", font_size=28, color=YELLOW
        )
        calc.next_to(equation, DOWN, buff=1)
        self.play(Write(calc))
        self.wait(1)

        # Update C
        C_updated = MathTex(
            r"\begin{bmatrix} 19 & ? \\ ? & ? \end{bmatrix}", font_size=36
        )
        C_updated.move_to(C.get_center())
        self.play(Transform(C, C_updated))
        self.wait(1)

        # Continue with other elements
        calc2 = MathTex(
            r"C_{12} = (1)(6) + (2)(8) = 22", font_size=28, color=YELLOW
        )
        calc2.next_to(calc, DOWN)
        self.play(Write(calc2))

        calc3 = MathTex(r"C_{21} = (3)(5) + (4)(7) = 43", font_size=28, color=YELLOW)
        calc3.next_to(calc2, DOWN)
        self.play(Write(calc3))

        calc4 = MathTex(r"C_{22} = (3)(6) + (4)(8) = 50", font_size=28, color=YELLOW)
        calc4.next_to(calc3, DOWN)
        self.play(Write(calc4))

        # Final result
        C_final = MathTex(
            r"\begin{bmatrix} 19 & 22 \\ 43 & 50 \end{bmatrix}", font_size=36
        )
        C_final.move_to(C.get_center())
        self.play(Transform(C, C_final))
        self.wait(2)


class ShearTransformation(LinearTransformationScene):
    """
    Visualize a shear transformation - common and useful example.
    """

    def __init__(self, **kwargs):
        super().__init__(
            show_coordinates=True,
            leave_ghost_vectors=True,
            show_basis_vectors=True,
            **kwargs,
        )

    def construct(self):
        title = Text("Shear Transformation", font_size=32)
        title.to_corner(UP + LEFT)
        self.add_foreground_mobject(title)

        # Shear matrix
        matrix_tex = MathTex(
            r"\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}", font_size=32
        )
        matrix_tex.to_corner(UP + RIGHT)
        matrix_tex.add_background_rectangle()
        self.play(Write(matrix_tex))

        explanation = Text("Shear: j-hat tilts, i-hat stays", font_size=20)
        explanation.next_to(matrix_tex, DOWN)
        explanation.add_background_rectangle()
        self.play(Write(explanation))

        self.wait(1)

        # Apply shear
        shear_matrix = [[1, 1], [0, 1]]
        self.apply_matrix(shear_matrix)

        self.wait(2)


class RotationTransformation(LinearTransformationScene):
    """
    Visualize rotation transformation.
    """

    def __init__(self, **kwargs):
        super().__init__(
            show_coordinates=True,
            leave_ghost_vectors=True,
            show_basis_vectors=True,
            **kwargs,
        )

    def construct(self):
        title = Text("Rotation by 45°", font_size=32)
        title.to_corner(UP + LEFT)
        self.add_foreground_mobject(title)

        angle = PI / 4
        cos_val = np.cos(angle)
        sin_val = np.sin(angle)

        matrix_tex = MathTex(
            r"\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}",
            font_size=28,
        )
        matrix_tex.to_corner(UP + RIGHT)
        matrix_tex.add_background_rectangle()
        self.play(Write(matrix_tex))

        self.wait(1)

        # Apply rotation
        rotation_matrix = [[cos_val, -sin_val], [sin_val, cos_val]]
        self.apply_matrix(rotation_matrix)

        self.wait(2)


# Scene for running all visualizations
class AllTransformations(Scene):
    """
    Quick overview of different transformations.
    """

    def construct(self):
        title = Text("Gallery of Linear Transformations", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        transformations = [
            ("Identity", [[1, 0], [0, 1]]),
            ("Scale (2x)", [[2, 0], [0, 2]]),
            ("Horizontal Stretch", [[2, 0], [0, 1]]),
            ("Shear", [[1, 1], [0, 1]]),
            ("90° Rotation", [[0, -1], [1, 0]]),
            ("Reflection (y-axis)", [[-1, 0], [0, 1]]),
        ]

        for name, matrix in transformations:
            # Create fresh plane each time
            plane = NumberPlane(
                x_range=[-3, 3, 1],
                y_range=[-3, 3, 1],
                background_line_style={"stroke_opacity": 0.5},
            )

            # Unit square
            square = Square(side_length=2, color=YELLOW, fill_opacity=0.3)
            square.move_to(RIGHT + UP)

            # Basis vectors
            i_hat = Arrow(ORIGIN, RIGHT * 2, buff=0, color=GREEN, stroke_width=4)
            j_hat = Arrow(ORIGIN, UP * 2, buff=0, color=RED, stroke_width=4)

            label = Text(name, font_size=28)
            label.to_edge(UP)

            matrix_tex = MathTex(
                rf"\begin{{bmatrix}} {matrix[0][0]} & {matrix[0][1]} \\ {matrix[1][0]} & {matrix[1][1]} \end{{bmatrix}}",
                font_size=32,
            )
            matrix_tex.to_corner(UR)

            group = VGroup(plane, square, i_hat, j_hat)
            self.play(FadeIn(group), Write(label), Write(matrix_tex))
            self.wait(0.5)

            # Apply transformation
            self.play(
                group.animate.apply_matrix(np.array(matrix)), run_time=1.5
            )
            self.wait(1)

            self.play(FadeOut(group), FadeOut(label), FadeOut(matrix_tex))
