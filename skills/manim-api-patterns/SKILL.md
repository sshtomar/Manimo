---
name: manim-api-patterns
description: "Manim API patterns and best practices for Scene, Mobject, and Animation classes."
---

<skill_content>

<overview>
Manim API patterns encode best practices for using Manim's core classes effectively. Following these patterns ensures code is maintainable, performant, and follows Manim conventions.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Scene Class Structure</name>
  <description>MUST define Scene classes with construct() method. All animation logic goes in construct()</description>
  <rationale>Manim requires Scene classes with construct() method. This is the standard pattern for all Manim animations.</rationale>
  <consequence>Code won't render, violates Manim architecture</consequence>
</requirement>

<requirement priority="high">
  <name>Mobject Creation Before Animation</name>
  <description>MUST create all Mobjects before animating them. Don't create and animate in the same call</description>
  <rationale>Separating creation from animation improves code clarity and allows for better control over timing.</rationale>
  <consequence>Code is harder to read and modify, timing control is limited</consequence>
</requirement>

<requirement priority="high">
  <name>Use Appropriate Animation Methods</name>
  <description>MUST use appropriate animation methods: Write() for text, Create() for shapes, Transform() for morphing, TransformMatchingTex() for equations, etc.</description>
  <rationale>Each animation method is designed for specific use cases. Using the right method produces better results. TransformMatchingTex intelligently matches parts of equations.</rationale>
  <consequence>Animations look wrong or unprofessional, code is harder to understand</consequence>
</requirement>

<requirement priority="high">
  <name>Rate Functions for Mathematical Accuracy</name>
  <description>MUST use linear rate_func when animating mathematical processes (differential equations, time evolution) to preserve accuracy</description>
  <rationale>Default smooth rate function masks mathematical behavior. Linear preserves the actual time evolution of mathematical systems.</rationale>
  <consequence>Mathematical animations lose accuracy, viewers misunderstand the actual behavior</consequence>
</requirement>

<requirement priority="medium">
  <name>Updaters for Dynamic Tracking</name>
  <description>SHOULD use updaters when objects need to dynamically follow other objects (e.g., dots tracking curve endpoints)</description>
  <rationale>Updaters provide real-time updates. Essential for showing how objects relate dynamically.</rationale>
  <consequence>Dynamic relationships aren't shown, animations miss important connections</consequence>
</requirement>

<requirement priority="critical">
  <name>Return Scene Class</name>
  <description>MUST return the Scene class from the cell so it can be rendered</description>
  <rationale>Marimo cells need to return values. Returning the Scene class allows it to be used for rendering.</rationale>
  <consequence>Scene can't be accessed or rendered</consequence>
</requirement>

</mandatory_requirements>

<patterns>

<pattern name="Basic Scene Structure">
  <code>
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # Create objects
        text = Text("Hello, Manim!")
        
        # Animate
        self.play(Write(text))
        self.wait()
        
        # Transform or remove
        self.play(FadeOut(text))
```
  </code>
  <description>Standard pattern: create objects, animate them, optionally transform or remove</description>
</pattern>

<pattern name="Multiple Objects">
  <code>
```python
class MyScene(Scene):
    def construct(self):
        # Create all objects first
        circle = Circle()
        square = Square()
        text = Text("Example")
        
        # Position objects
        square.next_to(circle, RIGHT)
        text.next_to(square, DOWN)
        
        # Animate in sequence or parallel
        self.play(Create(circle), Create(square))
        self.play(Write(text))
```
  </code>
  <description>Create all objects, position them, then animate</description>
</pattern>

<pattern name="Updaters for Dynamic Objects">
  <code>
```python
class UpdaterScene(Scene):
    def construct(self):
        curve = ParametricFunction(lambda t: np.array([t, np.sin(t), 0]), t_range=[0, 2*PI])
        dot = Dot(color=RED)
        
        # Define updater function
        def update_dot(mob, dt):
            mob.move_to(curve.get_end())
        
        # Add updater - dot will follow curve end
        dot.add_updater(update_dot)
        
        self.add(curve, dot)
        self.play(Create(curve), run_time=3)
        
        # Remove updater when done
        dot.remove_updater(update_dot)
```
  </code>
  <description>Use updaters to make objects dynamically follow other objects. Essential for tracking points on evolving curves.</description>
</pattern>

<pattern name="TransformMatchingTex for Equations">
  <code>
```python
class EquationTransform(Scene):
    def construct(self):
        # Use double braces to group parts for matching
        eq1 = MathTex("42 {{ a^2 }} + {{ b^2 }} = {{ c^2 }}")
        eq2 = MathTex("42 {{ a^2 }} = {{ c^2 }} - {{ b^2 }}")
        
        self.add(eq1)
        self.wait()
        # TransformMatchingTex matches parts with same TeX strings
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
```
  </code>
  <description>Use TransformMatchingTex to animate equation transformations. Double braces {{ }} group parts for matching.</description>
</pattern>

<pattern name="Color Gradients for Visual Effects">
  <code>
```python
class GradientScene(Scene):
    def construct(self):
        # Create color gradient
        colors = color_gradient([BLUE, RED], 10)
        
        # Apply to multiple objects
        curves = VGroup()
        for i, color in enumerate(colors):
            curve = ParametricFunction(...)
            curve.set_color(color)
            curves.add(curve)
        
        self.play(Create(curves))
```
  </code>
  <description>Use color_gradient() to create smooth color transitions across multiple objects. Useful for distinguishing similar elements.</description>
</pattern>

<pattern name="Tracing Tails for Motion">
  <code>
```python
class TracingTailScene(Scene):
    def construct(self):
        dot = Dot(color=BLUE)
        
        # Create tracing tail that follows the dot
        tail = TracingTail(dot, stroke_color=BLUE, time_traced=1.0)
        
        self.add(dot, tail)
        self.play(dot.animate.move_to(3*RIGHT), run_time=3)
```
  </code>
  <description>Use TracingTail to create trailing effects that follow moving objects. time_traced controls how long the tail persists.</description>
</pattern>

</patterns>

</skill_content>

