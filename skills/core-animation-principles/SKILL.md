---
name: core-animation-principles
description: "Core animation principles and timing for all Manim animations. Always loaded to maintain animation quality and clarity standards."
---

<skill_content>

<overview>
Core animation principles establish the fundamental rules of effective animation. These principles ensure animations are clear, engaging, and mathematically accurate. This skill is ALWAYS loaded because its requirements apply to every animation.

These are not suggestions - they are mandatory safeguards developed from decades of animation expertise and educational design.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Proper Timing and Pacing</name>
  <description>MUST use appropriate timing for all animations. Fast movements should be quick, slow explanations should be deliberate.</description>
  <rationale>Timing is the soul of animation. Poor timing makes animations confusing or boring. Educational animations need time for viewers to process information.</rationale>
  <consequence>Animations feel rushed or sluggish, viewers can't follow the mathematical concepts, educational value is lost</consequence>
</requirement>

<requirement priority="critical">
  <name>Rate Functions: Smooth vs Linear</name>
  <description>MUST choose appropriate rate functions based on context. Use smooth (default) for aesthetic animations, linear for mathematical accuracy</description>
  <rationale>Default smooth rate function (cubic bezier) creates elegant easing. However, when animating mathematical processes (like differential equations, time evolution), linear rate functions preserve the mathematical behavior. Smooth functions mask the actual time evolution.</rationale>
  <consequence>Mathematical animations lose accuracy, or aesthetic animations look mechanical</consequence>
  <guidance>
    - Use smooth (default): For most animations, aesthetic transformations, general movement
    - Use linear: When animating mathematical processes, differential equations, time evolution where accuracy matters
    - Example: Drawing a Lorenz attractor curve should use linear rate_func to match actual time evolution
  </guidance>
</requirement>

<requirement priority="high">
  <name>Scene Composition</name>
  <description>MUST organize elements with clear visual hierarchy. Important elements should be prominent, supporting elements should not distract</description>
  <rationale>Cluttered scenes confuse viewers. Clear hierarchy guides attention to what matters. Educational animations must prioritize clarity over decoration.</rationale>
  <consequence>Viewers can't identify key concepts, animation fails to teach effectively</consequence>
</requirement>

<requirement priority="critical">
  <name>Animation Duration Documentation</name>
  <description>MUST document animation durations and timing decisions with RATIONALE comments</description>
  <rationale>Reproducibility requires understanding timing choices. Future creators need to know why animations are paced this way.</rationale>
  <consequence>Timing decisions are opaque, hard to modify or improve animations</consequence>
</requirement>

<requirement priority="high">
  <name>Consistent Styling</name>
  <description>MUST use consistent colors, fonts, and styles throughout the animation</description>
  <rationale>Consistency creates professional appearance. Inconsistent styling distracts from mathematical content.</rationale>
  <consequence>Animation looks unprofessional, distracts from educational content</consequence>
</requirement>

</mandatory_requirements>

<pedagogical_principles>

<principle name="Show, Don't Tell">
  <description>Demonstrate mathematical concepts through animation, not just text</description>
  <implementation>Use visual transformations, movements, and highlights to illustrate concepts</implementation>
  <rationale>Visual learning is more effective than text alone for mathematical concepts</rationale>
</principle>

<principle name="Progressive Disclosure">
  <description>Reveal information gradually, building complexity step by step</description>
  <implementation>Start simple, add complexity incrementally, let viewers build understanding</implementation>
  <rationale>Overwhelming viewers with all information at once reduces comprehension</rationale>
</principle>

<principle name="Emphasis Through Motion">
  <description>Use motion to draw attention to important elements</description>
  <implementation>Animate key concepts, keep supporting elements static or subtle</implementation>
  <rationale>Motion naturally draws the eye, guides viewer attention</rationale>
</principle>

<principle name="Mathematical Accuracy Over Aesthetics">
  <description>When visualizing mathematical processes, preserve accuracy even if it means less smooth animation</description>
  <implementation>Use linear rate functions for mathematical time evolution, match animation runtime to actual time scales</implementation>
  <rationale>Educational animations must be mathematically correct. Smoothing can mask important mathematical behavior.</rationale>
</principle>

</pedagogical_principles>

<thinking_process>
For EVERY animation:
1. Determine the core mathematical concept to visualize
2. Plan the visual hierarchy (what's most important?)
3. Design timing (how long for each step?)
4. Choose appropriate easing for each movement
5. Ensure consistency in styling
6. Document all timing and design decisions
</thinking_process>

</skill_content>

