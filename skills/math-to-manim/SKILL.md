---
name: math-to-manim
description: "Transform any concept into professional Manim animations using a six-agent reverse knowledge tree pipeline. Use when user asks to create a math animation, animate a mathematical concept, generate Manim code, visualize a topic with animation, explain a concept visually, or mentions reverse knowledge tree or prerequisite discovery."
version: 1.0.0
---

<skill_content>

<overview>
Transform any concept into professional mathematical animations using a six-agent workflow that requires NO training data - only pure LLM reasoning.

Instead of training on example animations, this system recursively asks: **"What must I understand BEFORE this concept?"** This builds pedagogically sound animations that flow naturally from foundation concepts to advanced topics.

Key insight: verbose, specific prompts with exact LaTeX and visual specifications produce dramatically better code than vague descriptions.
</overview>

<when_to_use>
Invoke this workflow when:
- Creating mathematical or scientific animations
- Building educational visualizations with Manim
- Generating code from conceptual explanations
- Needing pedagogically structured content progression
- User mentions "reverse knowledge tree" or "prerequisite discovery"
</when_to_use>

<mandatory_requirements>

<requirement priority="critical">
  <name>Reverse Knowledge Tree Decomposition</name>
  <description>MUST recursively discover prerequisites before generating animations. Ask "What must I understand BEFORE this concept?" until hitting foundation concepts (high school level).</description>
  <rationale>Pedagogically sound animations require proper prerequisite ordering. Viewers need foundational understanding before advanced topics.</rationale>
  <consequence>Animations skip foundational concepts, viewers can't follow the progression</consequence>
</requirement>

<requirement priority="critical">
  <name>Six-Agent Pipeline Execution</name>
  <description>MUST execute all six agents in order: ConceptAnalyzer -> PrerequisiteExplorer -> MathematicalEnricher -> VisualDesigner -> NarrativeComposer -> CodeGenerator</description>
  <rationale>Each agent builds on the previous one's output. Skipping agents produces incomplete or incoherent animations.</rationale>
  <consequence>Animations lack mathematical rigor, visual coherence, or pedagogical structure</consequence>
</requirement>

<requirement priority="critical">
  <name>Verbose Prompt Generation</name>
  <description>MUST generate a 2000+ token verbose prompt with exact LaTeX, colors, positions, and animation timings before code generation</description>
  <rationale>Verbose, specific prompts eliminate ambiguity and produce dramatically better Manim code than vague descriptions.</rationale>
  <consequence>Generated code is incomplete, inconsistent, or requires extensive manual fixing</consequence>
</requirement>

<requirement priority="high">
  <name>Foundation Detection</name>
  <description>MUST stop recursive prerequisite discovery when hitting concepts a high school graduate would understand without further explanation</description>
  <rationale>Prevents infinite recursion and establishes the appropriate starting point for the animation.</rationale>
  <consequence>Tree grows too deep or starts at too basic a level</consequence>
</requirement>

<requirement priority="high">
  <name>Topological Sort for Animation Order</name>
  <description>MUST traverse the knowledge tree from leaves (foundations) to root (target concept) using topological sort</description>
  <rationale>Ensures each concept builds on previously explained ones. Viewers have necessary background before encountering advanced topics.</rationale>
  <consequence>Concepts appear out of order, viewers lack prerequisites for understanding</consequence>
</requirement>

</mandatory_requirements>

<six_agent_pipeline>

<agent name="ConceptAnalyzer" number="1">
  <purpose>Parse user intent to extract core concept and metadata</purpose>
  <output>
    - core_concept: specific topic name
    - domain: physics, math, CS, etc.
    - level: beginner / intermediate / advanced
    - goal: learning objective
  </output>
  <temperature>0.3</temperature>
  <max_tokens>500</max_tokens>
  <example>
```json
{
  "core_concept": "quantum entanglement",
  "domain": "physics/quantum mechanics",
  "level": "intermediate",
  "goal": "Understand how entangled particles maintain correlation across distances"
}
```
  </example>
</agent>

<agent name="PrerequisiteExplorer" number="2">
  <purpose>Recursively build knowledge tree (the key innovation)</purpose>
  <process>
    1. Ask: "What are the prerequisites for [concept]?"
    2. For each prerequisite, recursively ask the same question
    3. Stop when hitting foundation concepts (high school level)
    4. Build DAG structure with depth tracking (max depth 3-4)
  </process>
  <foundation_examples>
    Foundation (stop here): velocity, distance, time, acceleration, force, mass, energy, waves, frequency, wavelength, numbers, addition, multiplication, basic geometry, functions, graphs
    Non-foundation (keep exploring): Lorentz transformations, gauge theory, differential geometry, tensor calculus, quantum operators, Hilbert spaces
  </foundation_examples>
  <temperature>0.0 (foundation detection) / 0.3 (discovery)</temperature>
  <max_tokens>500</max_tokens>
  <example>
```
quantum tunneling (depth 0)
├─ wave-particle duality (depth 1)
│   ├─ de Broglie wavelength (depth 2) [FOUNDATION]
│   └─ Heisenberg uncertainty principle (depth 2)
│       └─ wave function (depth 3) [FOUNDATION]
├─ Schrödinger equation (depth 1)
│   ├─ wave function (depth 2) [FOUNDATION]
│   └─ potential energy (depth 2) [FOUNDATION]
└─ potential barriers (depth 1) [FOUNDATION]
```
  </example>
</agent>

<agent name="MathematicalEnricher" number="3">
  <purpose>Add mathematical content to each node in the tree</purpose>
  <output>
    - equations: 2-5 LaTeX formulas (Manim-compatible, double backslashes)
    - definitions: symbol-to-meaning mappings
    - interpretation: what equations represent
    - example: worked calculation with numbers
  </output>
  <temperature>0.3</temperature>
  <max_tokens>1500</max_tokens>
  <rules>
    - Use Manim-compatible LaTeX (double backslashes: \\frac, \\sum)
    - Include units where appropriate
    - Adjust complexity to the concept level
  </rules>
</agent>

<agent name="VisualDesigner" number="4">
  <purpose>Design visual specifications for each concept</purpose>
  <output>
    - elements: visual objects to create (graphs, 3D objects, diagrams)
    - colors: Manim color constants (BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, WHITE)
    - animations: sequence (FadeIn, Create, Transform, Write)
    - transitions: how to connect to previous concept
    - camera_movement: camera instructions (or "none")
    - layout: spatial arrangement description
    - duration: estimated seconds (15-30 per concept)
  </output>
  <temperature>0.5</temperature>
  <max_tokens>1500</max_tokens>
</agent>

<agent name="NarrativeComposer" number="5">
  <purpose>Walk tree from foundation to target, generating scene descriptions</purpose>
  <process>
    1. Topologically sort nodes (foundations first)
    2. Generate 200-300 word segment per concept
    3. Include exact LaTeX, colors, animations, positions
    4. Stitch into 2000+ token verbose prompt
  </process>
  <temperature>0.7</temperature>
  <max_tokens>1500</max_tokens>
  <segment_structure>
    - Timestamp header (e.g., "0:00 - 0:15")
    - Opening action (start with a verb: "Begin by fading in...")
    - Equation display with exact LaTeX and positioning
    - Visual elements with Manim class, color, and position
    - Animation sequence in order with durations
    - Transition hook to next scene
  </segment_structure>
</agent>

<agent name="CodeGenerator" number="6">
  <purpose>Generate working Manim Community Edition Python code</purpose>
  <requirements>
    - Use Manim Community Edition (manim, not manimlib)
    - Import: from manim import *
    - Scene class (or ThreeDScene for 3D content)
    - Raw strings for LaTeX: r"$\\frac{a}{b}$"
    - All visual elements, colors, animations from prompt
    - Runnable with: manim -pql file.py SceneName
  </requirements>
  <temperature>0.3</temperature>
  <max_tokens>8000</max_tokens>
</agent>

</six_agent_pipeline>

<color_palette_guidelines>

| Element Type | Recommended Color |
|--------------|-------------------|
| Primary equations | BLUE |
| Secondary equations | YELLOW |
| Axes/grids | WHITE or GREY |
| Graphs/curves | YELLOW, GREEN |
| Labels | GREEN |
| Highlights | GOLD or ORANGE |
| Warnings/errors | RED |
| Success/completion | GREEN |

</color_palette_guidelines>

<timing_guidelines>

| Content Type | Duration |
|--------------|----------|
| Simple equation display | 2-3 seconds |
| Complex equation with explanation | 4-5 seconds |
| Graph/visualization creation | 3-4 seconds |
| Transition between concepts | 1-2 seconds |
| Pause for comprehension | 1 second |
| Complete scene | 15-30 seconds |

</timing_guidelines>

<workflow_quick_start>

For immediate use, follow this simplified pattern:

1. **Parse**: Extract the core concept from user input
2. **Discover**: Build prerequisite tree (depth 3-4)
3. **Enrich**: Add math and visual specs to each node
4. **Compose**: Generate verbose prompt (2000+ tokens)
5. **Generate**: Produce working Manim code

</workflow_quick_start>

<output_files>

The pipeline generates:
- `{concept}_prompt.txt` - Verbose prompt
- `{concept}_tree.json` - Knowledge tree structure
- `{concept}_animation.py` - Manim Python code
- `{concept}_result.json` - Complete metadata

</output_files>

<additional_resources>

- `references/reverse-knowledge-tree.md` - Detailed algorithm with data structures and caching
- `references/agent-system-prompts.md` - Complete prompts for all six agents
- `references/verbose-prompt-format.md` - Full prompt template with examples
- `examples/pythagorean-theorem/` - Complete workflow example

</additional_resources>

<common_pitfalls>

1. **Vague descriptions**: "Show the equation" -> "Display r'$E=mc^2$' using MathTex() in BLUE at TOP"
2. **Missing positions**: Always specify where elements appear
3. **Unclear timing**: Include duration for each animation
4. **No transitions**: Explicitly describe how scenes connect
5. **Inconsistent colors**: Define palette and stick to it
6. **Missing LaTeX escaping**: Use raw strings with double backslashes

</common_pitfalls>

<thinking_process>
When transforming a concept to animation:
1. What is the user trying to understand? (ConceptAnalyzer)
2. What must be understood BEFORE this? (PrerequisiteExplorer)
3. What are the key equations and definitions? (MathematicalEnricher)
4. How should each concept look visually? (VisualDesigner)
5. What is the scene-by-scene narrative? (NarrativeComposer)
6. Does the generated code run and implement the prompt? (CodeGenerator)
</thinking_process>

</skill_content>
