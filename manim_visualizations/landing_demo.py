"""
Landing Page Demo - Derivative of x² Visualization
A polished, concise animation for the Manimo landing page.
No LaTeX dependency - uses Text instead of MathTex.
"""

from manim import (
    Scene,
    VGroup,
    Axes,
    Text,
    Dot,
    Line,
    Create,
    Write,
    FadeIn,
    FadeOut,
    ValueTracker,
    always_redraw,
    BLUE,
    RED,
    YELLOW,
    WHITE,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    config,
    linear,
)

# Colors
FUNC_COLOR = BLUE
TANGENT_COLOR = "#F59E0B"  # Amber to match the UI
POINT_COLOR = "#F59E0B"


class DerivativeDemo(Scene):
    """
    Clean, focused animation showing the derivative of x².
    Designed for the landing page hero section.
    """

    def construct(self):
        # Dark background matching the landing page
        self.camera.background_color = "#0f172a"  # slate-900

        # Create axes (no numbers to avoid LaTeX)
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-0.5, 5, 1],
            x_length=8,
            y_length=5,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "color": "#475569",  # slate-600
            },
        )
        axes.shift(DOWN * 0.3)

        # Axis labels using Text
        x_label = Text("x", font_size=24, color="#94a3b8")
        x_label.next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = Text("y", font_size=24, color="#94a3b8")
        y_label.next_to(axes.y_axis.get_end(), UP, buff=0.2)

        # Function and derivative
        func = lambda x: x**2
        derivative = lambda x: 2 * x

        # Plot the parabola
        graph = axes.plot(
            func,
            x_range=[-2.2, 2.2],
            color=FUNC_COLOR,
            stroke_width=3,
        )

        # Function label
        func_label = Text("f(x) = x²", font_size=28, color=FUNC_COLOR)
        func_label.to_corner(UP + RIGHT).shift(DOWN * 0.5 + LEFT * 0.5)

        # Derivative label (will appear later)
        deriv_label = Text("f'(x) = 2x", font_size=28, color=TANGENT_COLOR)
        deriv_label.next_to(func_label, DOWN, aligned_edge=LEFT, buff=0.3)

        # Animate axes and graph
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1)
        self.play(Create(graph), run_time=1.5)
        self.play(Write(func_label), run_time=0.8)
        self.wait(0.5)

        # Value tracker for x position
        x_tracker = ValueTracker(-2.0)

        # Point on curve
        point = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(), func(x_tracker.get_value())),
            color=POINT_COLOR,
            radius=0.12,
        ))

        # Tangent line
        def get_tangent_line():
            x = x_tracker.get_value()
            slope = derivative(x)
            y = func(x)
            x_range = 1.2
            start = axes.c2p(x - x_range, y - slope * x_range)
            end = axes.c2p(x + x_range, y + slope * x_range)
            return Line(start, end, color=TANGENT_COLOR, stroke_width=3)

        tangent = always_redraw(get_tangent_line)

        # Slope display using Text
        def get_slope_display():
            x_val = x_tracker.get_value()
            slope_val = derivative(x_val)

            x_text = Text(f"x = {x_val:.1f}", font_size=24, color="#e2e8f0")
            slope_text = Text(f"slope = {slope_val:.1f}", font_size=24, color=TANGENT_COLOR)

            group = VGroup(x_text, slope_text)
            group.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            group.to_corner(UP + RIGHT).shift(DOWN * 1.8 + LEFT * 0.5)
            return group

        slope_box = always_redraw(get_slope_display)

        # Show point and tangent
        self.play(FadeIn(point, scale=0.5), run_time=0.5)
        self.play(Create(tangent), run_time=0.8)
        self.play(Write(slope_box), run_time=0.5)
        self.wait(0.3)

        # Animate the point moving along the curve
        self.play(
            x_tracker.animate.set_value(2.0),
            run_time=4,
            rate_func=linear,
        )
        self.wait(0.5)

        # Show derivative formula
        self.play(Write(deriv_label), run_time=0.8)
        self.wait(0.3)

        # One more sweep back
        self.play(
            x_tracker.animate.set_value(-1.5),
            run_time=2.5,
            rate_func=linear,
        )
        self.wait(0.5)

        # Final pause
        self.play(
            x_tracker.animate.set_value(1.0),
            run_time=1.5,
            rate_func=linear,
        )
        self.wait(1)


if __name__ == "__main__":
    # Render with: manim -pql landing_demo.py DerivativeDemo
    # Or for higher quality: manim -pqh landing_demo.py DerivativeDemo
    pass
