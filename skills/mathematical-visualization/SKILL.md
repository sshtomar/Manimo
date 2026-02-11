---
name: mathematical-visualization
description: "Best practices for visualizing mathematical concepts clearly and accurately, with multi-representation techniques from 3Blue1Brown."
---

<skill_content>

<overview>
Mathematical visualization requires accuracy, clarity, and appropriate representation. This skill ensures mathematical concepts are visualized correctly and understandably, incorporating multi-representation techniques that show the same concept from multiple synchronized perspectives.

Core principle: Mathematical relationships should be VISIBLE, not just stated.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Mathematical Accuracy</name>
  <description>MUST ensure all mathematical representations are accurate. Scales, proportions, and relationships must be correct</description>
  <rationale>Inaccurate visualizations teach wrong concepts. Mathematical accuracy is non-negotiable for educational content.</rationale>
  <consequence>Viewers learn incorrect mathematics, animation misleads rather than teaches</consequence>
</requirement>

<requirement priority="critical">
  <name>Consistent Color Coding</name>
  <description>MUST use consistent colors for the same mathematical entity across all representations</description>
  <rationale>Color creates instant recognition. If x is BLUE in one place, it must be BLUE everywhere.</rationale>
  <consequence>Viewers can't track connections between representations</consequence>
  <standard_palette>
    - Variables: x=BLUE, y=YELLOW, z=GREEN
    - Inputs/first operands: BLUE family
    - Outputs/results: contrasting colors
    - Use t2c={"x": BLUE} in MathTex
  </standard_palette>
</requirement>

<requirement priority="high">
  <name>Clear Labels and Annotations</name>
  <description>MUST label all axes, points, and important elements. Use MathTex for mathematical notation</description>
  <rationale>Unlabeled visualizations are meaningless. Viewers need context to understand what they're seeing.</rationale>
  <consequence>Viewers can't interpret the visualization, educational value is lost</consequence>
</requirement>

<requirement priority="high">
  <name>Appropriate Coordinate Systems</name>
  <description>MUST use appropriate coordinate systems (Axes, NumberLine, ComplexPlane) for the mathematical concept</description>
  <rationale>Different concepts require different coordinate systems. Using the right system makes concepts clearer.</rationale>
  <consequence>Concepts are harder to understand, visualization is less effective</consequence>
</requirement>

<requirement priority="critical">
  <name>Scale and Proportions</name>
  <description>MUST maintain correct scale relationships. Don't distort mathematical relationships for visual appeal</description>
  <rationale>Distorted scales mislead viewers. Mathematical relationships must be preserved accurately.</rationale>
  <consequence>Viewers misunderstand mathematical relationships, learn incorrect concepts</consequence>
</requirement>

<requirement priority="critical">
  <name>Preserve Mathematical Time Evolution</name>
  <description>MUST use linear rate_func and match animation runtime to actual time when visualizing differential equations or time-dependent processes</description>
  <rationale>Mathematical processes have inherent time evolution. Smoothing functions mask this behavior.</rationale>
  <consequence>Viewers misunderstand how the system actually evolves, mathematical accuracy is lost</consequence>
</requirement>

</mandatory_requirements>

<multi_representation_patterns>

<pattern name="Dual-Space Visualization">
  <description>Show related mathematical spaces side by side, updating synchronously</description>
  <code>
```python
class DualSpaceScene(Scene):
    def construct(self):
        # Two coordinate systems for related spaces
        root_plane = ComplexPlane(x_range=[-3, 3], y_range=[-3, 3])
        root_plane.shift(LEFT * 3.5)
        root_label = Text("Root Space", font_size=24).next_to(root_plane, UP)

        coef_plane = ComplexPlane(x_range=[-3, 3], y_range=[-3, 3])
        coef_plane.shift(RIGHT * 3.5)
        coef_label = Text("Coefficient Space", font_size=24).next_to(coef_plane, UP)

        # Synchronized dots
        root_tracker = ValueTracker(1)

        root_dot = always_redraw(lambda: Dot(
            root_plane.n2p(root_tracker.get_value()),
            color=YELLOW
        ))

        coef_dot = always_redraw(lambda: Dot(
            coef_plane.n2p(-root_tracker.get_value()),  # coefficient = -root
            color=RED
        ))

        self.add(root_plane, coef_plane, root_label, coef_label)
        self.add(root_dot, coef_dot)

        # Move root, coefficient follows
        self.play(root_tracker.animate.set_value(2), run_time=2)
```
  </code>
  <use_when>Showing mappings: roots to coefficients, time to frequency, input to output</use_when>
</pattern>

<pattern name="Formula + Graph + Numerical Synchronized">
  <description>Show algebraic, geometric, and numerical representations together</description>
  <code>
```python
class TripleRepresentation(Scene):
    def construct(self):
        # Shared parameter
        x_tracker = ValueTracker(1)

        # Algebraic (formula)
        formula = always_redraw(lambda: MathTex(
            f"f({x_tracker.get_value():.1f}) = {x_tracker.get_value()**2:.2f}",
            color=BLUE
        ).to_corner(UL))

        # Geometric (graph)
        axes = Axes(x_range=[-3, 3], y_range=[0, 9])
        graph = axes.plot(lambda x: x**2, color=BLUE)
        point = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(), x_tracker.get_value()**2),
            color=YELLOW
        ))

        # Numerical (bar or value display)
        bar = always_redraw(lambda: Rectangle(
            height=x_tracker.get_value()**2 / 3,
            width=0.5,
            fill_opacity=0.7,
            color=BLUE
        ).next_to(axes, RIGHT, buff=1).align_to(axes, DOWN))

        self.add(formula, axes, graph, point, bar)
        self.play(x_tracker.animate.set_value(2.5), run_time=3)
```
  </code>
  <use_when>Teaching function concepts - viewers see all three representations update together</use_when>
</pattern>

<pattern name="Before/After Side by Side">
  <description>Show transformation by displaying before and after states simultaneously</description>
  <code>
```python
class TransformationComparison(Scene):
    def construct(self):
        # Original on left
        left_plane = NumberPlane(x_range=[-2, 2], y_range=[-2, 2])
        left_plane.scale(0.4).shift(LEFT * 3)
        left_label = Text("Before", font_size=20).next_to(left_plane, UP)

        # Transformed on right
        right_plane = NumberPlane(x_range=[-2, 2], y_range=[-2, 2])
        right_plane.scale(0.4).shift(RIGHT * 3)
        right_label = Text("After", font_size=20).next_to(right_plane, UP)

        # Same vector in both
        left_vec = Arrow(left_plane.c2p(0, 0), left_plane.c2p(1, 1), color=YELLOW)
        right_vec = Arrow(right_plane.c2p(0, 0), right_plane.c2p(2, 1), color=YELLOW)

        # Show both, animate only the right
        self.add(left_plane, left_label, left_vec)
        self.play(Create(right_plane), Write(right_label))
        self.play(TransformFromCopy(left_vec, right_vec))
```
  </code>
  <use_when>Showing effects of transformations, operations, or changes</use_when>
</pattern>

<pattern name="Discrete to Continuous Transition">
  <description>Show how discrete representations approach continuous limits</description>
  <code>
```python
class DiscreteToContrinuous(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 4], y_range=[0, 5])
        graph = axes.plot(lambda x: x**2 / 4, color=BLUE)

        # Start with few rectangles
        n_tracker = ValueTracker(4)

        rects = always_redraw(lambda: axes.get_riemann_rectangles(
            graph,
            x_range=[0, 4],
            dx=4 / n_tracker.get_value(),
            fill_opacity=0.5
        ))

        n_label = always_redraw(lambda: MathTex(
            f"n = {int(n_tracker.get_value())}"
        ).to_corner(UR))

        self.add(axes, graph, rects, n_label)

        # Increase n progressively
        for n in [8, 16, 32, 64]:
            self.play(n_tracker.animate.set_value(n), run_time=1)
            self.wait(0.5)

        # Final: show area (the limit)
        area = axes.get_area(graph, x_range=[0, 4], color=BLUE, opacity=0.7)
        self.play(Transform(rects, area))
```
  </code>
  <use_when>Teaching limits, integrals, or convergence concepts</use_when>
</pattern>

</multi_representation_patterns>

<standard_patterns>

<pattern name="Graphing Functions">
  <code>
```python
class FunctionGraph(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        # Create function graph with consistent color
        graph = axes.plot(lambda x: x**2, color=BLUE)
        graph_label = MathTex("y = x^2", color=BLUE).next_to(graph, UR)

        self.play(Create(axes), Write(axes_labels))
        self.play(Create(graph), Write(graph_label))
```
  </code>
  <description>Always include axes, labels, and function labels. Color the equation to match the curve.</description>
</pattern>

<pattern name="Geometric Constructions">
  <code>
```python
class GeometryScene(Scene):
    def construct(self):
        triangle = Polygon(
            [0, 0, 0], [2, 0, 0], [1, 1.73, 0],
            color=BLUE
        )

        # Label vertices with consistent positioning
        labels = VGroup(
            MathTex("A").next_to(triangle.get_vertices()[0], DOWN),
            MathTex("B").next_to(triangle.get_vertices()[1], DOWN),
            MathTex("C").next_to(triangle.get_vertices()[2], UP),
        )

        self.play(Create(triangle), Write(labels))
```
  </code>
  <description>Label all important points and maintain geometric accuracy</description>
</pattern>

<pattern name="Differential Equation Visualization">
  <code>
```python
class DiffEqScene(Scene):
    def construct(self):
        from scipy.integrate import solve_ivp

        def system(t, state):
            x, y, z = state
            return [10*(y-x), x*(28-z)-y, x*y-8/3*z]

        solution = solve_ivp(system, [0, 30], [10, 10, 10], dense_output=True)
        points = solution.sol(np.linspace(0, 30, 1000)).T

        curve = VMobject()
        curve.set_points_as_corners(points)
        curve.set_color(BLUE)

        # CRITICAL: Use linear rate_func to preserve time evolution
        self.play(Create(curve), rate_func=linear, run_time=30)
```
  </code>
  <description>When visualizing differential equations, use linear rate_func and match runtime to preserve accuracy</description>
</pattern>

<pattern name="Multiple Trajectories with Color Gradient">
  <code>
```python
class MultipleTrajectories(Scene):
    def construct(self):
        # Slightly different initial conditions
        initial_states = [[10, 10, 10 + i*0.001] for i in range(10)]
        colors = color_gradient([BLUE, TEAL], len(initial_states))

        curves = VGroup()
        for state, color in zip(initial_states, colors):
            solution = solve_ode(state, ...)
            curve = VMobject()
            curve.set_points_as_corners(solution)
            curve.set_color(color)
            curves.add(curve)

        # Animate all together with linear rate_func
        self.play(Create(curves), rate_func=linear, run_time=30)
```
  </code>
  <description>Use color gradients to distinguish similar trajectories. Essential for showing chaos/divergence.</description>
</pattern>

</standard_patterns>

<visual_hierarchy>

<principle name="Opacity for Focus">
  <description>Use opacity to establish what's important vs. contextual</description>
  <implementation>
    - Primary focus: opacity=1.0
    - Supporting context: opacity=0.2-0.5
    - Background reference: opacity=0.1
  </implementation>
  <code>
```python
# Focus on one curve while showing others as context
for i, curve in enumerate(curves):
    if i == focus_index:
        curve.set_stroke(opacity=1.0, width=3)
    else:
        curve.set_stroke(opacity=0.3, width=1)
```
  </code>
</principle>

<principle name="Size for Importance">
  <description>Larger elements are more important</description>
  <implementation>
    - Key points: larger dots (radius=0.15)
    - Reference points: smaller dots (radius=0.05)
    - Important labels: larger font (font_size=36)
    - Annotations: smaller font (font_size=20)
  </implementation>
</principle>

<principle name="Position for Relationship">
  <description>Related elements should be spatially close</description>
  <implementation>
    - Labels next to their referents
    - Equations near their graphs
    - Legends near their data
  </implementation>
</principle>

</visual_hierarchy>

<thinking_process>
For every mathematical visualization:
1. What is the core mathematical relationship to show?
2. What representation makes this relationship VISIBLE?
3. Would multiple synchronized representations help?
4. What's the correct coordinate system?
5. What needs to be labeled for clarity?
6. What's the visual hierarchy (focus vs. context)?
7. Is color coding consistent across all elements?
8. Is the mathematical time evolution preserved (if applicable)?
</thinking_process>

</skill_content>
