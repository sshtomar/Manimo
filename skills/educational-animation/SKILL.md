---
name: educational-animation
description: "Pedagogical design principles for effective educational animations, incorporating 3Blue1Brown storytelling techniques."
---

<skill_content>

<overview>
Educational animations must balance mathematical accuracy with pedagogical effectiveness. This skill ensures animations teach effectively while maintaining rigor, incorporating narrative storytelling techniques from 3Blue1Brown.

The goal: viewers should UNDERSTAND, not just SEE.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Learning Objectives</name>
  <description>MUST clearly identify what viewers should learn. Animation should have a clear educational goal</description>
  <rationale>Without clear learning objectives, animations lack focus. Viewers need to know what they're supposed to understand.</rationale>
  <consequence>Animation lacks focus, viewers don't know what to learn, educational value is unclear</consequence>
</requirement>

<requirement priority="critical">
  <name>Geometry Before Symbols</name>
  <description>MUST show geometric/visual representation before introducing symbolic notation. Viewers see WHAT before reading WHAT IT'S CALLED.</description>
  <rationale>Visual learning precedes symbolic understanding. The formula becomes meaningful only after geometric intuition exists.</rationale>
  <consequence>Viewers memorize symbols without understanding meaning</consequence>
  <example>Show Riemann rectangles filling area, THEN introduce integral notation</example>
</requirement>

<requirement priority="critical">
  <name>Progressive Complexity</name>
  <description>MUST build complexity gradually. Each animation step introduces exactly ONE new idea while maintaining previous context.</description>
  <rationale>Cognitive load management. Viewers need time to absorb each concept before adding complexity.</rationale>
  <consequence>Viewers are overwhelmed, can't follow the progression, learning is reduced</consequence>
  <technique>Use Transform/TransformMatchingTex to evolve content rather than replacing it</technique>
</requirement>

<requirement priority="high">
  <name>Highlight Key Concepts</name>
  <description>MUST use visual emphasis (color, motion, size, opacity) to highlight key mathematical concepts</description>
  <rationale>Visual emphasis guides attention. Without it, viewers don't know what's important.</rationale>
  <consequence>Viewers miss key concepts, animation fails to teach effectively</consequence>
  <technique>Use opacity 0.2-0.5 for context, full opacity for focus</technique>
</requirement>

<requirement priority="critical">
  <name>Mathematical Correctness</name>
  <description>MUST ensure all mathematical statements and visualizations are correct</description>
  <rationale>Incorrect mathematics teaches wrong concepts. Accuracy is non-negotiable.</rationale>
  <consequence>Viewers learn incorrect mathematics, animation misleads</consequence>
</requirement>

<requirement priority="high">
  <name>Preserve Mathematical Behavior in Animation</name>
  <description>MUST use linear rate functions and accurate time scales when animating mathematical processes to preserve their actual behavior</description>
  <rationale>Mathematical processes have inherent time evolution. Smoothing can mask important behavior.</rationale>
  <consequence>Viewers misunderstand the actual mathematical behavior, learn incorrect concepts</consequence>
</requirement>

</mandatory_requirements>

<storytelling_structure>

<phase name="Setup - Create Curiosity">
  <description>Establish the question or puzzle. Make viewers want to know the answer.</description>
  <techniques>
    - Show a surprising result without explanation ("This equals pi. Why?")
    - Pose a question visually (display a pattern, ask what comes next)
    - Show the end state, then rewind ("Let's see how we got here")
    - Use a concrete example before abstraction
  </techniques>
  <timing>Keep setup brief (10-20% of total time). Build curiosity, don't exhaust it.</timing>
</phase>

<phase name="Build - Progressive Understanding">
  <description>Build complexity incrementally. Each step adds exactly one concept.</description>
  <techniques>
    - One concept per animation sequence
    - Transform rather than replace (viewers track evolution)
    - Build visual stakes: "Will this pattern continue?"
    - Use LaggedStart to guide attention through collections
    - Maintain context with reduced opacity elements
  </techniques>
  <timing>This is the main content (60-70% of total time). Don't rush.</timing>
</phase>

<phase name="Surprise - Strategic Reveals">
  <description>Create moments of insight with well-timed reveals.</description>
  <techniques>
    - Long pause before revealing surprising results
    - Numerical precision reveals: = pi, then approx 0.9999999pi
    - "Plateau shrink" in iterative visualizations
    - Zoom out to reveal unexpected pattern
  </techniques>
  <timing>Brief but impactful. Let revelations breathe.</timing>
</phase>

<phase name="Resolution - Connect Understanding">
  <description>Tie everything together. Connect back to the original question.</description>
  <techniques>
    - Show the unifying formula/principle
    - Zoom out to see full pattern
    - Return to the original question with new understanding
    - Preview where this leads next
  </techniques>
  <timing>Satisfying conclusion (10-15% of total time).</timing>
</phase>

</storytelling_structure>

<pedagogical_patterns>

<pattern name="Show, Then Explain">
  <description>First show the visual phenomenon, then add labels and explanations</description>
  <implementation>
    1. Animate the mathematical behavior (no labels yet)
    2. Pause to let viewers observe
    3. Add labels, equations, annotations
    4. Connect visual to symbolic
  </implementation>
  <rationale>Visual first engages curiosity. Explanation then provides framework for understanding.</rationale>
</pattern>

<pattern name="Compare and Contrast">
  <description>Show multiple examples side by side to illustrate differences</description>
  <implementation>
    1. Create synchronized visualizations
    2. Use consistent color coding across both
    3. Animate them together so differences are obvious
    4. Highlight the specific differences
  </implementation>
  <rationale>Comparison builds discrimination. Viewers understand what something IS by seeing what it ISN'T.</rationale>
</pattern>

<pattern name="Build Up Complexity">
  <description>Start simple, add layers of complexity</description>
  <implementation>
    1. Begin with simplest case (n=1, x=0, etc.)
    2. Animate transformation to slightly more complex
    3. Continue building (use Transform, not FadeIn/FadeOut)
    4. Each step is learnable because it's small
  </implementation>
  <rationale>Incremental building matches how understanding develops. Big jumps lose viewers.</rationale>
</pattern>

<pattern name="Concrete to Abstract">
  <description>Start with specific examples, generalize to abstract principle</description>
  <implementation>
    1. Show specific numerical example (e.g., 3^2 + 4^2 = 5^2)
    2. Show another example
    3. Highlight pattern
    4. Introduce general notation (a^2 + b^2 = c^2)
  </implementation>
  <rationale>Abstraction is meaningful only after concrete grounding. Examples first.</rationale>
</pattern>

<pattern name="Use Color to Distinguish, Not Decorate">
  <description>Color serves mathematical purpose, not just aesthetics</description>
  <implementation>
    - Same mathematical entity = same color everywhere
    - Use color_gradient() for collections of similar objects
    - t2c={"x": BLUE, "y": YELLOW} in MathTex
    - Contrasting colors for contrasting concepts
  </implementation>
  <rationale>Color creates instant recognition. Decorative color confuses; functional color clarifies.</rationale>
</pattern>

<pattern name="Strategic Pauses">
  <description>Pauses are pedagogical tools, not dead time</description>
  <implementation>
    - Long pause (1-2s) after surprising results
    - Medium pause (0.5-1s) after completing a step
    - Short pause (0.25s) between mechanical steps
    - AVOID: rushing through without pauses
  </implementation>
  <rationale>Pauses allow cognitive processing. Without them, viewers can't absorb what they've seen.</rationale>
</pattern>

</pedagogical_patterns>

<common_mistakes>

<mistake name="Explaining Before Showing">
  <wrong>First write the formula, then show what it means</wrong>
  <right>First animate the phenomenon, then introduce notation</right>
  <why>Formulas are meaningful only after visual intuition exists</why>
</mistake>

<mistake name="Too Much at Once">
  <wrong>Show complete complex diagram immediately</wrong>
  <right>Build diagram piece by piece, pausing at each step</right>
  <why>Cognitive overload prevents learning</why>
</mistake>

<mistake name="No Visual Hierarchy">
  <wrong>All elements at same opacity and prominence</wrong>
  <right>Focus elements at full opacity, context at 20-50%</right>
  <why>Viewers need guidance on what's important</why>
</mistake>

<mistake name="Replacing Instead of Transforming">
  <wrong>FadeOut old equation, FadeIn new equation</wrong>
  <right>TransformMatchingTex to evolve the equation</right>
  <why>Transformations show relationships; replacements break mental models</why>
</mistake>

</common_mistakes>

<thinking_process>
For every educational animation:
1. What is the ONE core insight viewers should gain?
2. What visual representation makes this intuitive? (geometry before symbols)
3. What's the simplest starting point?
4. What sequence of small steps leads to the full concept?
5. Where are the "aha moments" that need emphasis?
6. What should be highlighted vs. background context?
7. How long should viewers have to process each step?
</thinking_process>

</skill_content>
