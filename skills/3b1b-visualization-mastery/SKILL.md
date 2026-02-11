---
name: 3b1b-visualization-mastery
description: "Master-level visualization principles derived from 3Blue1Brown's videos. Use when creating publication-quality mathematical animations that prioritize pedagogy and visual clarity."
---

<skill_content>

<overview>
This skill encodes the visualization philosophy and techniques used by Grant Sanderson (3Blue1Brown) - the gold standard for mathematical animation. These principles were extracted from analyzing 3+ years of production code in the 3b1b/videos repository (2022-2025).

The core insight: **Every animation choice serves pedagogy.** Visual beauty emerges from mathematical clarity, not the reverse.

Apply this skill when you want to create animations that truly teach, not just demonstrate.
</overview>

<philosophy>
<principle name="Geometry Before Symbols">
  <description>Show the geometric meaning first, then connect to notation. Viewers should SEE what's happening before they READ what it means.</description>
  <implementation>Animate Riemann rectangles before integral symbols. Show vector arrows before coordinate notation. Fill areas before writing area formulas.</implementation>
  <rationale>Visual learning precedes symbolic understanding. The symbol becomes meaningful only after viewers have geometric intuition.</rationale>
</principle>

<principle name="Progressive Disclosure">
  <description>Never show everything at once. Each animation step introduces exactly ONE new idea while maintaining previous context.</description>
  <implementation>Use TransformMatchingTex() to evolve equations step-by-step. Build complexity incrementally. Let viewers absorb before adding more.</implementation>
  <rationale>Cognitive load management. Overwhelming viewers with all information at once reduces comprehension.</rationale>
</principle>

<principle name="Transformation Over Replacement">
  <description>Morph objects into new forms rather than fade-and-replace. This shows relationships and maintains visual continuity.</description>
  <implementation>
    - TransformFromCopy() for creating derived objects
    - TransformMatchingShapes() for structural changes
    - MoveToTarget() for position/scale changes
    - AVOID: FadeOut() then FadeIn() for related objects
  </implementation>
  <rationale>Viewers track transformations. Replacements break mental models. Showing "this becomes that" is more powerful than "here's something new."</rationale>
</principle>

<principle name="Multiple Synchronized Representations">
  <description>Show the same concept in 2-3 different ways simultaneously: algebraic formula + geometric visualization + numerical example.</description>
  <implementation>
    - Root plane + coefficient plane (polynomial videos)
    - Discrete bars + continuous curves (convolutions)
    - Time domain + frequency domain (Fourier)
  </implementation>
  <rationale>Different representations serve different intuitions. When they update together, viewers build deeper understanding.</rationale>
</principle>
</philosophy>

<mandatory_requirements>

<requirement priority="critical">
  <name>Consistent Color Coding Across Representations</name>
  <description>MUST assign consistent colors to mathematical roles across all representations. Same color = same mathematical entity.</description>
  <rationale>Color creates instant recognition. If x is BLUE in the formula, it must be BLUE in the graph, the vector, and the numerical display.</rationale>
  <consequence>Viewers can't track connections between representations, defeating the purpose of multiple views</consequence>
  <standard_palette>
    - First operand/input: BLUE
    - Second operand: YELLOW or TEAL
    - Output/result: contrasting color (often GREEN or RED)
    - Parameters: RED (amplitude), GOLD (frequency), PINK (phase)
    - Use t2c={"x": BLUE, "y": YELLOW} in MathTex for consistency
  </standard_palette>
</requirement>

<requirement priority="critical">
  <name>Strategic Animation Rhythm</name>
  <description>MUST stagger animations using LaggedStart() with appropriate lag_ratio. MUST pause strategically after important reveals.</description>
  <rationale>Rhythm guides attention. Staggered animations create visual flow. Pauses allow processing of surprising information.</rationale>
  <consequence>Animations feel rushed or chaotic, viewers miss key insights</consequence>
  <guidance>
    - lag_ratio=0.01-0.1: Dense information, many similar objects
    - lag_ratio=0.3-0.5: Sequential steps with dependencies
    - lag_ratio=0.7: Strong separation between steps
    - Long self.wait() after surprising results
    - Short self.wait(0.25) after mechanical steps
  </guidance>
</requirement>

<requirement priority="critical">
  <name>Frame Control for Narrative Focus</name>
  <description>MUST use frame/camera control to direct attention. Zoom in on details. Pan to follow action. Reorient for 3D understanding.</description>
  <rationale>Camera is the viewer's eye. Control it intentionally to guide attention and reveal structure.</rationale>
  <consequence>Viewers miss important details, 3D structures are confusing</consequence>
  <patterns>
    - frame.animate.move_to(object) to center on focus
    - frame.animate.scale(0.5) to zoom in on detail
    - frame.animate.reorient(theta, phi) for 3D perspective changes
    - Start 2D, rotate into 3D when needed
  </patterns>
</requirement>

<requirement priority="high">
  <name>Visual Hierarchy Through Opacity</name>
  <description>MUST use opacity to establish visual hierarchy. Important elements: full opacity. Supporting context: reduced opacity (20-50%).</description>
  <rationale>Not everything is equally important. Reduced opacity keeps context visible without competing for attention.</rationale>
  <consequence>Cluttered visuals where everything competes for attention</consequence>
</requirement>

<requirement priority="high">
  <name>Labels That Follow</name>
  <description>MUST use updaters to keep labels attached to moving objects. Text should stay perpendicular to camera in 3D.</description>
  <rationale>Floating labels disconnect from their referents. Labels must maintain spatial relationship with objects.</rationale>
  <implementation>
    label.add_updater(lambda m: m.next_to(object, direction))
    always.set_perpendicular_to_camera(self.frame) # for 3D
  </implementation>
</requirement>

</mandatory_requirements>

<animation_patterns>

<pattern name="LaggedStartMap for Collections">
  <code>
```python
# Stagger animations across a collection of objects
self.play(LaggedStartMap(FadeIn, group_of_objects, lag_ratio=0.1))
self.play(LaggedStartMap(Create, curves, lag_ratio=0.05))
```
  </code>
  <description>Animate multiple similar objects with staggered timing. Creates visual rhythm and guides attention through the collection.</description>
</pattern>

<pattern name="TransformMatchingTex for Equation Evolution">
  <code>
```python
# Equations EVOLVE, they don't replace
eq1 = MathTex(r"{{ e^x }} = {{ 1 }} + {{ x }} + {{ \frac{x^2}{2!} }}")
eq2 = MathTex(r"{{ e^{-x^2} }} = {{ 1 }} - {{ x^2 }} + {{ \frac{x^4}{2!} }}")

self.play(TransformMatchingTex(eq1, eq2))
```
  </code>
  <description>Use double braces {{ }} to mark parts that should match. Viewers see the equation transform, building understanding of the relationship.</description>
</pattern>

<pattern name="Synchronized Multi-View Updates">
  <code>
```python
# Two planes that update together
root_tracker = ValueTracker(1)

def update_root_dot(dot):
    r = root_tracker.get_value()
    dot.move_to(root_plane.n2p(r))

def update_coef_dot(dot):
    r = root_tracker.get_value()
    # coefficients depend on roots
    dot.move_to(coef_plane.n2p(-r))

root_dot.add_updater(update_root_dot)
coef_dot.add_updater(update_coef_dot)

# Now when root_tracker changes, BOTH update
self.play(root_tracker.animate.set_value(2), run_time=2)
```
  </code>
  <description>Multiple representations that stay synchronized through shared ValueTrackers and updaters.</description>
</pattern>

<pattern name="Progressive Complexity Build">
  <code>
```python
# Start simple, add complexity
self.play(Create(base_graph))
self.wait(1)  # Let it sink in

self.play(Write(first_annotation))
self.wait(0.5)

self.play(
    FadeIn(secondary_elements, opacity=0.3),  # Lower opacity for context
    Write(more_labels)
)

# Finally show the complex result
self.play(
    Transform(simple_curve, complex_curve),
    run_time=2
)
```
  </code>
  <description>Build from simple to complex. Each step adds ONE layer. Context elements get reduced opacity.</description>
</pattern>

<pattern name="Tracers for Motion History">
  <code>
```python
dot = Dot(color=BLUE)
tracer = TracedPath(dot.get_center, stroke_color=BLUE, stroke_width=2)

self.add(tracer, dot)
self.play(MoveAlongPath(dot, curve), run_time=3)
```
  </code>
  <description>Show where something has been. Essential for building intuition about trajectories and paths.</description>
</pattern>

<pattern name="Numerical Precision Reveals">
  <code>
```python
# Build suspense with increasing precision
results = ["= \\pi", "= 3.14159...", "\\approx 0.9999999998529\\pi"]

for result in results:
    new_eq = MathTex(base + result)
    self.play(Transform(equation, new_eq))
    self.wait(1)  # Let viewers notice the pattern
```
  </code>
  <description>Reveal numerical precision gradually. Creates "detective story" effect where pattern emerges.</description>
</pattern>

<pattern name="Scale Navigation with Nested Zooms">
  <code>
```python
# Navigate from small to large scale
self.play(frame.animate.move_to(detail_point).scale(0.3), run_time=2)
self.wait(1)  # Examine detail

# Pull back to see context
self.play(frame.animate.move_to(ORIGIN).scale(3), run_time=2)
```
  </code>
  <description>Navigate between scales using frame control. Essential for relating local detail to global structure.</description>
</pattern>

</animation_patterns>

<storytelling_structure>

<phase name="Setup">
  <description>Establish the question or puzzle. Make viewers curious.</description>
  <techniques>
    - Show a surprising result without explanation
    - Pose a question visually
    - Display the end state, then ask "how did we get here?"
  </techniques>
</phase>

<phase name="Build">
  <description>Progressive complexity with visual stakes. Each step adds understanding.</description>
  <techniques>
    - One concept per animation step
    - Transform rather than replace
    - Build suspense: "Will it work for this case too?"
  </techniques>
</phase>

<phase name="Surprise">
  <description>Strategic reveals of unexpected results.</description>
  <techniques>
    - Long pause before revealing
    - Numerical precision reveals (= pi, then ≈ 0.999999pi)
    - "Plateau shrink" effect in iterative visualizations
  </techniques>
</phase>

<phase name="Resolution">
  <description>Connect back to deeper understanding.</description>
  <techniques>
    - Show the formula that explains everything
    - Zoom out to see the pattern
    - Relate back to the original question
  </techniques>
</phase>

</storytelling_structure>

<common_mistakes>

<mistake name="Fade-Replace Instead of Transform">
  <wrong>self.play(FadeOut(old_eq)); self.play(FadeIn(new_eq))</wrong>
  <right>self.play(TransformMatchingTex(old_eq, new_eq))</right>
  <why>Transformations show relationships. Replacements break mental models.</why>
</mistake>

<mistake name="Everything at Full Opacity">
  <wrong>All elements at opacity=1.0</wrong>
  <right>Primary focus: 1.0, Supporting context: 0.2-0.5</right>
  <why>Visual hierarchy guides attention. Not everything is equally important.</why>
</mistake>

<mistake name="Static Labels for Moving Objects">
  <wrong>label.next_to(object, UP) # Called once</wrong>
  <right>label.add_updater(lambda m: m.next_to(object, UP))</right>
  <why>Labels must follow their referents during animation.</why>
</mistake>

<mistake name="Simultaneous Everything">
  <wrong>self.play(Create(obj1), Create(obj2), Create(obj3), ...)</wrong>
  <right>self.play(LaggedStartMap(Create, objects, lag_ratio=0.1))</right>
  <why>Staggered timing creates rhythm and guides attention.</why>
</mistake>

<mistake name="Inconsistent Colors">
  <wrong>x is BLUE in formula, RED in graph</wrong>
  <right>x is BLUE everywhere, always</right>
  <why>Color consistency enables instant recognition across representations.</why>
</mistake>

</common_mistakes>

<thinking_process>
Before creating any visualization, ask:
1. What is the ONE core insight I want viewers to understand?
2. What geometric representation makes this intuitive?
3. How can I build up to this incrementally?
4. What should be emphasized vs. background context?
5. Where are the "surprise" moments that need pauses?
6. What transformations show the relationships between concepts?
7. Is my color coding consistent across all representations?
8. Have I used frame control to guide attention?
</thinking_process>

</skill_content>
