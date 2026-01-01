---
name: mathematical-visualization
description: "Best practices for visualizing mathematical concepts clearly and accurately."
---

<skill_content>

<overview>
Mathematical visualization requires accuracy, clarity, and appropriate representation. This skill ensures mathematical concepts are visualized correctly and understandably.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Mathematical Accuracy</name>
  <description>MUST ensure all mathematical representations are accurate. Scales, proportions, and relationships must be correct</description>
  <rationale>Inaccurate visualizations teach wrong concepts. Mathematical accuracy is non-negotiable for educational content.</rationale>
  <consequence>Viewers learn incorrect mathematics, animation misleads rather than teaches</consequence>
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
  <rationale>Mathematical processes have inherent time evolution. Smoothing functions mask this behavior. Animation runtime should match the actual time scale of the mathematical system.</rationale>
  <consequence>Viewers misunderstand how the system actually evolves, mathematical accuracy is lost</consequence>
  <example>When animating a Lorenz attractor, use linear rate_func and runtime matching the integration time to show actual evolution</example>
</requirement>

</mandatory_requirements>

<patterns>

<pattern name="Graphing Functions">
  <code>
```python
class FunctionGraph(Scene):
    def construct(self):
        # Create axes with proper labels
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # Create function graph
        graph = axes.plot(lambda x: x**2, color=BLUE)
        graph_label = MathTex("y = x^2").next_to(graph, UR)
        
        # Animate
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(graph), Write(graph_label))
```
  </code>
  <description>Always include axes, labels, and function labels for clarity</description>
</pattern>

<pattern name="Geometric Constructions">
  <code>
```python
class GeometryScene(Scene):
    def construct(self):
        # Create geometric objects with proper relationships
        triangle = Polygon(
            [0, 0, 0],
            [2, 0, 0],
            [1, 1.73, 0],
            color=BLUE
        )
        
        # Label vertices
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
        
        # Define differential equation
        def lorenz_system(t, state):
            x, y, z = state
            return [10*(y-x), x*(28-z)-y, x*y-8/3*z]
        
        # Solve numerically
        solution = solve_ivp(lorenz_system, [0, 30], [10, 10, 10], 
                            dense_output=True)
        points = solution.sol(np.linspace(0, 30, 1000)).T
        
        # Create curve with linear rate function for accuracy
        curve = VMobject()
        curve.set_points_as_corners(points)
        curve.set_color(BLUE)
        
        # Animate with linear rate_func to preserve time evolution
        self.play(Create(curve), rate_func=linear, run_time=30)
```
  </code>
  <description>When visualizing differential equations, use linear rate_func and match runtime to actual time to preserve mathematical accuracy</description>
</pattern>

<pattern name="Multiple Initial Conditions">
  <code>
```python
class MultipleTrajectories(Scene):
    def construct(self):
        # Multiple initial conditions
        initial_states = [[10, 10, 10 + i*0.001] for i in range(10)]
        colors = color_gradient([BLUE, TEAL], len(initial_states))
        
        curves = VGroup()
        dots = VGroup()
        
        for state, color in zip(initial_states, colors):
            # Solve for each initial condition
            solution = solve_ode(state, ...)
            curve = VMobject()
            curve.set_points_as_corners(solution)
            curve.set_color(color)
            curves.add(curve)
            
            # Dot to track endpoint
            dot = Dot(color=color, radius=0.08)
            dots.add(dot)
        
        # Updater to track endpoints
        def update_dots(mobs):
            for dot, curve in zip(mobs, curves):
                dot.move_to(curve.get_end())
        
        dots.add_updater(update_dots)
        
        self.play(Create(curves), rate_func=linear, run_time=30)
        self.add(dots)
```
  </code>
  <description>Use color gradients and updaters to visualize multiple trajectories with tracking dots. Essential for showing chaos and divergence.</description>
</pattern>

</patterns>

</skill_content>

