---
name: educational-animation
description: "Pedagogical design principles for effective educational animations."
---

<skill_content>

<overview>
Educational animations must balance mathematical accuracy with pedagogical effectiveness. This skill ensures animations teach effectively while maintaining rigor.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Learning Objectives</name>
  <description>MUST clearly identify what viewers should learn. Animation should have a clear educational goal</description>
  <rationale>Without clear learning objectives, animations lack focus. Viewers need to know what they're supposed to understand.</rationale>
  <consequence>Animation lacks focus, viewers don't know what to learn, educational value is unclear</consequence>
</requirement>

<requirement priority="high">
  <name>Progressive Complexity</name>
  <description>MUST build complexity gradually. Start with simple concepts, add complexity step by step</description>
  <rationale>Viewers need to build understanding incrementally. Overwhelming complexity reduces learning.</rationale>
  <consequence>Viewers are overwhelmed, can't follow the progression, learning is reduced</consequence>
</requirement>

<requirement priority="high">
  <name>Highlight Key Concepts</name>
  <description>MUST use visual emphasis (color, motion, size) to highlight key mathematical concepts</description>
  <rationale>Visual emphasis guides attention. Without it, viewers don't know what's important.</rationale>
  <consequence>Viewers miss key concepts, animation fails to teach effectively</consequence>
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
  <rationale>Mathematical processes have inherent time evolution. Smoothing can mask important behavior. For educational value, viewers must see how the mathematics actually behaves.</rationale>
  <consequence>Viewers misunderstand the actual mathematical behavior, learn incorrect concepts about how systems evolve</consequence>
</requirement>

</mandatory_requirements>

<pedagogical_patterns>

<pattern name="Show, Then Explain">
  <description>First show the visual, then explain what it means</description>
  <implementation>Animate the mathematical concept, then add labels and explanations</implementation>
  <rationale>Visual first engages viewers, explanation then provides understanding</rationale>
</pattern>

<pattern name="Compare and Contrast">
  <description>Show multiple examples side by side to illustrate differences</description>
  <implementation>Create multiple visualizations, animate them together, highlight differences</implementation>
  <rationale>Comparison helps viewers understand distinctions and relationships</rationale>
</pattern>

<pattern name="Build Up Complexity">
  <description>Start simple, add layers of complexity</description>
  <implementation>Begin with basic concept, animate additions that add complexity</implementation>
  <rationale>Incremental building helps viewers understand how complexity emerges</rationale>
</pattern>

<pattern name="Show Mathematical Process, Then Explain">
  <description>First visualize the mathematical process accurately, then add explanations and labels</description>
  <implementation>Animate the core mathematical visualization (e.g., differential equation solution), then add equations, labels, and annotations</implementation>
  <rationale>Viewers first see what's happening, then understand why. This follows Grant's workflow of building the visualization first, then adding context.</rationale>
</pattern>

<pattern name="Use Color to Distinguish, Not Decorate">
  <description>Use color gradients to distinguish similar elements (e.g., multiple trajectories), not just for decoration</description>
  <implementation>When showing multiple similar objects, use color_gradient() to create visual distinction. Choose colors that are both aesthetically pleasing and functionally distinct.</implementation>
  <rationale>Color should serve a purpose. Multiple trajectories need visual distinction. Color gradients provide both distinction and aesthetic appeal.</rationale>
</pattern>

</pedagogical_patterns>

</skill_content>

