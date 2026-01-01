---
name: manimo-notebook
description: "Marimo notebook patterns and best practices for Manim animations."
---

<skill_content>

<overview>
Marimo notebooks have specific patterns for organizing Manim code. This skill ensures code follows Marimo conventions and works well in the notebook environment.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>Cell Structure</name>
  <description>MUST use @app.cell decorator for all code cells. Each cell should have a clear purpose</description>
  <rationale>Marimo requires @app.cell decorator. Cells should be organized logically.</rationale>
  <consequence>Code won't work in Marimo, violates notebook structure</consequence>
</requirement>

<requirement priority="high">
  <name>Return Values</name>
  <description>MUST return Scene classes and important objects from cells so they can be used in other cells</description>
  <rationale>Marimo cells need return values to share data. Returning Scene classes allows rendering.</rationale>
  <consequence>Scenes can't be accessed, code can't be reused across cells</consequence>
</requirement>

<requirement priority="high">
  <name>Cell Organization</name>
  <description>MUST organize cells logically: imports first, then scene creation, then rendering logic</description>
  <rationale>Logical organization improves readability and maintainability.</rationale>
  <consequence>Code is hard to follow, difficult to modify</consequence>
</requirement>

<requirement priority="medium">
  <name>Documentation</name>
  <description>MUST include docstrings or markdown cells explaining what each scene does</description>
  <rationale>Documentation helps future creators understand the code.</rationale>
  <consequence>Code is hard to understand and modify</consequence>
</requirement>

</mandatory_requirements>

<patterns>

<pattern name="Basic Scene Cell">
  <code>
```python
@app.cell
def create_scene():
    from manim import *
    
    class MyScene(Scene):
        def construct(self):
            text = Text("Hello!")
            self.play(Write(text))
            self.wait()
    
    return MyScene,
```
  </code>
  <description>Standard pattern: import, define Scene class, return it</description>
</pattern>

<pattern name="Multiple Scenes">
  <code>
```python
@app.cell
def create_scenes():
    from manim import *
    
    class Scene1(Scene):
        def construct(self):
            # First scene logic
            pass
    
    class Scene2(Scene):
        def construct(self):
            # Second scene logic
            pass
    
    return Scene1, Scene2,
```
  </code>
  <description>Return multiple Scene classes for different animations</description>
</pattern>

</patterns>

</skill_content>

