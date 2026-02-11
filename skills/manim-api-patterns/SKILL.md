---
name: manim-api-patterns
description: "Manim API patterns and best practices for Scene, Mobject, and Animation classes, with 3Blue1Brown animation rhythm techniques."
---

<skill_content>

<overview>
Manim API patterns encode best practices for using Manim's core classes effectively. This skill covers both fundamental Manim usage and advanced animation timing/rhythm techniques derived from 3Blue1Brown's production code.

Key insight: The API is a tool for pedagogy. Every technical choice should serve the educational goal.
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

<requirement priority="critical">
  <name>Use Transformation Animations</name>
  <description>MUST prefer Transform, TransformMatchingTex, TransformFromCopy over FadeOut/FadeIn for related objects</description>
  <rationale>Transformations show relationships. Viewers track how things change. FadeOut/FadeIn breaks mental models.</rationale>
  <consequence>Viewers lose track of relationships, animations feel disjointed</consequence>
</requirement>

<requirement priority="high">
  <name>Use Appropriate Animation Methods</name>
  <description>MUST use appropriate animation methods: Write() for text, Create() for shapes, Transform() for morphing, TransformMatchingTex() for equations</description>
  <rationale>Each animation method is designed for specific use cases. Using the right method produces better results.</rationale>
  <consequence>Animations look wrong or unprofessional, code is harder to understand</consequence>
</requirement>

<requirement priority="high">
  <name>Rate Functions for Mathematical Accuracy</name>
  <description>MUST use linear rate_func when animating mathematical processes (differential equations, time evolution)</description>
  <rationale>Default smooth rate function masks mathematical behavior. Linear preserves the actual time evolution.</rationale>
  <consequence>Mathematical animations lose accuracy, viewers misunderstand the actual behavior</consequence>
</requirement>

<requirement priority="critical">
  <name>Animation Rhythm with LaggedStart</name>
  <description>MUST use LaggedStart/LaggedStartMap for collections of objects instead of animating all simultaneously</description>
  <rationale>Staggered animations create visual rhythm and guide attention through collections.</rationale>
  <consequence>Animations feel chaotic, viewers can't track individual elements</consequence>
</requirement>

<requirement priority="high">
  <name>Updaters for Dynamic Relationships</name>
  <description>SHOULD use updaters when objects need to dynamically follow other objects</description>
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

<animation_rhythm_patterns>

<pattern name="LaggedStartMap for Collections">
  <code>
```python
# GOOD: Staggered animation creates rhythm
self.play(LaggedStartMap(FadeIn, objects, lag_ratio=0.1))
self.play(LaggedStartMap(Create, curves, lag_ratio=0.05))

# BAD: Everything at once is chaotic
self.play(*[FadeIn(obj) for obj in objects])  # Avoid this
```
  </code>
  <description>Always use LaggedStartMap for collections. The lag_ratio controls timing:
    - 0.01-0.1: Dense information, many similar objects
    - 0.3-0.5: Sequential steps with dependencies
    - 0.7: Strong separation between steps
  </description>
</pattern>

<pattern name="Strategic Pauses">
  <code>
```python
# After surprising result - long pause
self.play(Write(surprising_equation))
self.wait(2)  # Let it sink in

# After completing a step - medium pause
self.play(Transform(eq1, eq2))
self.wait(1)

# Between mechanical steps - short pause
self.play(Indicate(term1))
self.wait(0.25)
self.play(Indicate(term2))
```
  </code>
  <description>Pauses are pedagogical tools. Duration signals importance.</description>
</pattern>

<pattern name="Run Time Scaling">
  <code>
```python
# Complex transformations need more time
self.play(Transform(complex_obj, target), run_time=2)

# Simple movements can be quick
self.play(obj.animate.shift(RIGHT), run_time=0.5)

# Emphasize important reveals
self.play(Write(key_formula), run_time=1.5)

# Mathematical evolution matches real time
self.play(Create(trajectory), rate_func=linear, run_time=30)
```
  </code>
  <description>Match run_time to importance and complexity. Important = slower.</description>
</pattern>

</animation_rhythm_patterns>

<transformation_patterns>

<pattern name="TransformMatchingTex for Equations">
  <code>
```python
# Use double braces to mark parts for matching
eq1 = MathTex(r"{{ e^x }} = {{ 1 }} + {{ x }} + {{ \frac{x^2}{2!} }}")
eq2 = MathTex(r"{{ e^{-x^2} }} = {{ 1 }} - {{ x^2 }} + {{ \frac{x^4}{2!} }}")

self.add(eq1)
self.wait()
# Parts with matching TeX strings animate to each other
self.play(TransformMatchingTex(eq1, eq2))
```
  </code>
  <description>TransformMatchingTex creates smooth equation evolution. Parts transform based on matching TeX strings.</description>
</pattern>

<pattern name="TransformFromCopy for Derivations">
  <code>
```python
# Show how one thing derives from another
original = MathTex("a^2 + b^2")
derived = MathTex("c^2")

self.add(original)
self.wait()
# Original stays, copy transforms to derived
self.play(TransformFromCopy(original, derived.next_to(original, DOWN)))
```
  </code>
  <description>TransformFromCopy shows derivation while keeping the source visible.</description>
</pattern>

<pattern name="MoveToTarget for Complex Rearrangement">
  <code>
```python
# Setup the target state
obj.generate_target()
obj.target.shift(RIGHT * 2)
obj.target.scale(0.5)
obj.target.set_color(RED)

# Animate to target
self.play(MoveToTarget(obj))
```
  </code>
  <description>MoveToTarget allows complex multi-property animations in a single call.</description>
</pattern>

</transformation_patterns>

<updater_patterns>

<pattern name="always_redraw for Live Updates">
  <code>
```python
# Object that redraws every frame based on tracker
x_tracker = ValueTracker(0)

point = always_redraw(lambda: Dot(
    axes.c2p(x_tracker.get_value(), func(x_tracker.get_value())),
    color=YELLOW
))

label = always_redraw(lambda: MathTex(
    f"x = {x_tracker.get_value():.2f}"
).next_to(point, UP))

self.add(point, label)
self.play(x_tracker.animate.set_value(3), run_time=3)
```
  </code>
  <description>always_redraw recreates the object each frame. Use for objects with complex dependencies.</description>
</pattern>

<pattern name="add_updater for Relationships">
  <code>
```python
# Label follows moving object
label.add_updater(lambda m: m.next_to(dot, UP))

# Curve endpoint tracking
dot.add_updater(lambda m: m.move_to(curve.get_end()))

# Remove when done
dot.clear_updaters()
```
  </code>
  <description>add_updater maintains relationships during animation. Essential for labels and tracking.</description>
</pattern>

<pattern name="TracedPath for Motion History">
  <code>
```python
dot = Dot(color=BLUE)
path = TracedPath(dot.get_center, stroke_color=BLUE, stroke_width=2)

self.add(path, dot)  # path must be added before dot moves
self.play(dot.animate.move_to(3 * RIGHT + 2 * UP), run_time=2)
```
  </code>
  <description>TracedPath shows where objects have been. Essential for trajectories.</description>
</pattern>

</updater_patterns>

<frame_control_patterns>

<pattern name="Zooming and Panning">
  <code>
```python
# Access the frame (camera)
frame = self.camera.frame

# Zoom in on detail
self.play(frame.animate.scale(0.5).move_to(detail_point), run_time=2)

# Pan to new focus
self.play(frame.animate.move_to(new_focus), run_time=1)

# Zoom out to see context
self.play(frame.animate.scale(2).move_to(ORIGIN), run_time=2)
```
  </code>
  <description>Frame control directs viewer attention. Zoom for detail, pan for navigation.</description>
</pattern>

<pattern name="3D Perspective Changes">
  <code>
```python
# For ThreeDScene
frame = self.camera.frame

# Rotate to see from different angle
self.play(frame.animate.reorient(theta=30, phi=70), run_time=2)

# Combine with movement
self.play(
    frame.animate.reorient(theta=45, phi=60).move_to(focus_point),
    run_time=2
)
```
  </code>
  <description>In 3D scenes, use reorient to reveal structure from different viewpoints.</description>
</pattern>

</frame_control_patterns>

<color_patterns>

<pattern name="Consistent Color Coding">
  <code>
```python
# Define colors for mathematical roles
X_COLOR = BLUE
Y_COLOR = YELLOW
RESULT_COLOR = GREEN

# Apply in MathTex with t2c
equation = MathTex(
    r"f(x) = x^2",
    tex_to_color_map={"x": X_COLOR, "f": RESULT_COLOR}
)

# Apply to geometric objects
x_line = Line(ORIGIN, RIGHT * 2, color=X_COLOR)
y_line = Line(ORIGIN, UP * 2, color=Y_COLOR)
```
  </code>
  <description>Same mathematical entity = same color everywhere. Define colors once, use consistently.</description>
</pattern>

<pattern name="Color Gradients for Sequences">
  <code>
```python
# Create gradient across collection
colors = color_gradient([BLUE, TEAL, GREEN], len(objects))

for obj, color in zip(objects, colors):
    obj.set_color(color)
```
  </code>
  <description>Use gradients for similar objects to show progression or distinguish individuals.</description>
</pattern>

<pattern name="Opacity for Visual Hierarchy">
  <code>
```python
# Focus: full opacity
main_object.set_opacity(1.0)

# Context: reduced opacity
for supporting in context_objects:
    supporting.set_opacity(0.3)

# Gradual reveal
self.play(object.animate.set_opacity(1.0), run_time=0.5)
```
  </code>
  <description>Opacity establishes importance. High opacity = focus, low opacity = context.</description>
</pattern>

</color_patterns>

<defensive_patterns>

<pattern name="Scene Organization into Methods">
  <code>
```python
class QuantumTunneling(ThreeDScene):
    def construct(self):
        self.intro_foundation()
        self.show_wave_function()
        self.demonstrate_barrier()
        self.show_tunneling()
        self.conclusion()

    def intro_foundation(self):
        """Foundation concepts"""
        title = Text("Wave-Particle Duality")
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

    def show_wave_function(self):
        """Wave function visualization"""
        pass
```
  </code>
  <description>Break complex animations into named methods for clarity. Each method handles one concept or scene segment.</description>
</pattern>

<pattern name="Reusable Components">
  <code>
```python
def create_labeled_equation(tex_string, label_text, color=BLUE):
    """Create equation with label below"""
    equation = MathTex(tex_string).set_color(color)
    label = Text(label_text, font_size=24).next_to(equation, DOWN)
    return VGroup(equation, label)

# Usage
energy_eq = create_labeled_equation(r"E = mc^2", "Mass-energy equivalence")
self.play(FadeIn(energy_eq))
```
  </code>
  <description>Extract repeated patterns into helper functions. Keeps construct() clean and reduces duplication.</description>
</pattern>

<pattern name="Safe Object Handling">
  <code>
```python
# Check object exists before animating
if hasattr(self, 'previous_equation'):
    self.play(FadeOut(self.previous_equation))

# Group cleanup - fade out all mobjects
def clear_scene(self):
    self.play(*[FadeOut(mob) for mob in self.mobjects])

# Z-index for overlapping objects
foreground.set_z_index(1)
background.set_z_index(0)
```
  </code>
  <description>Defensive checks prevent runtime errors. Use z_index for overlapping, explicit cleanup for scene transitions.</description>
</pattern>

<pattern name="LaTeX Best Practices">
  <code>
```python
# Always use raw strings for LaTeX
equation = MathTex(r"E = mc^2")            # Correct
fraction = MathTex(r"\frac{a}{b}")          # Correct
integral = MathTex(r"\int_0^\infty f(x) dx")  # Correct

# WRONG - backslash issues
fraction = MathTex("\frac{a}{b}")  # FAILS

# Multi-part equations for selective coloring
schrodinger = MathTex(
    r"i\hbar\frac{\partial}{\partial t}\Psi",
    r"=",
    r"\hat{H}\Psi"
)
schrodinger[0].set_color(BLUE)
schrodinger[2].set_color(GREEN)

# Mixed text and math
mixed = Tex(r"The energy ", r"$E$", r" equals ", r"$mc^2$")
mixed[1].set_color(BLUE)
mixed[3].set_color(YELLOW)
```
  </code>
  <description>Raw strings prevent LaTeX rendering failures. Split equations into parts for selective styling.</description>
</pattern>

</defensive_patterns>

<common_mistakes>

<mistake name="Simultaneous Collection Animation">
  <wrong>self.play(*[Create(obj) for obj in objects])</wrong>
  <right>self.play(LaggedStartMap(Create, objects, lag_ratio=0.1))</right>
  <why>Staggered timing creates rhythm and guides attention</why>
</mistake>

<mistake name="FadeOut/FadeIn for Related Objects">
  <wrong>
self.play(FadeOut(eq1))
self.play(FadeIn(eq2))
  </wrong>
  <right>self.play(TransformMatchingTex(eq1, eq2))</right>
  <why>Transformations show relationships; replacements break mental models</why>
</mistake>

<mistake name="Static Labels for Moving Objects">
  <wrong>label.next_to(object, UP)  # Called once</wrong>
  <right>label.add_updater(lambda m: m.next_to(object, UP))</right>
  <why>Labels must follow their referents during animation</why>
</mistake>

<mistake name="Smooth Rate Function for Math">
  <wrong>self.play(Create(trajectory), run_time=5)  # Default smooth</wrong>
  <right>self.play(Create(trajectory), rate_func=linear, run_time=5)</right>
  <why>Mathematical time evolution requires linear rate function</why>
</mistake>

<mistake name="No Pauses After Important Content">
  <wrong>
self.play(Write(important_result))
self.play(next_animation)  # No pause
  </wrong>
  <right>
self.play(Write(important_result))
self.wait(1.5)  # Let it sink in
self.play(next_animation)
  </right>
  <why>Pauses allow cognitive processing of important information</why>
</mistake>

</common_mistakes>

<scene_structure_template>
```python
from manim import *

class WellStructuredScene(Scene):
    def construct(self):
        # 1. Setup: Create all objects
        axes = Axes(...)
        graph = axes.plot(...)
        labels = VGroup(...)

        # 2. Initial Display
        self.play(Create(axes))
        self.play(Create(graph), Write(labels))
        self.wait(1)

        # 3. Main Content: Progressive steps with pauses
        for step in steps:
            # One concept per step
            self.play(step_animation, run_time=appropriate_duration)
            self.wait(pause_duration)

        # 4. Highlight/Emphasis
        self.play(Indicate(key_element))
        self.wait(0.5)

        # 5. Resolution/Cleanup
        final_result = MathTex(...)
        self.play(Write(final_result))
        self.wait(2)  # Final pause for comprehension
```
</scene_structure_template>

<thinking_process>
For every animation:
1. Is this creation, transformation, or emphasis?
2. What's the appropriate animation method?
3. Should this be staggered (LaggedStart) or simultaneous?
4. What run_time reflects the importance/complexity?
5. Does this need a pause after? How long?
6. Are colors consistent with established coding?
7. Do labels need updaters to follow moving objects?
8. Is the rate_func appropriate (smooth vs linear)?
</thinking_process>

</skill_content>
