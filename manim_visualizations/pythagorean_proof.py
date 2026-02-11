"""
Pythagorean Theorem - Visual Proof via Area Rearrangement

Generated using the Math-To-Manim six-agent pipeline:
  1. ConceptAnalyzer: Pythagorean theorem, geometry, beginner
  2. PrerequisiteExplorer: right triangles, area of square, area conservation (all foundation)
  3. MathematicalEnricher: a² + b² = c², 3-4-5 triangle
  4. VisualDesigner: side-by-side arrangement comparison
  5. NarrativeComposer: Setup → Build → Surprise → Resolution
  6. CodeGenerator: this file

Proof strategy:
  Two arrangements of 4 identical right triangles inside the same (a+b)² square.
  Arrangement 1 leaves a tilted c² square. Arrangement 2 leaves a² + b² squares.
  Same total area minus same triangles → c² = a² + b².

Render:
  manim -pql pythagorean_proof.py PythagoreanProof     # preview
  manim -pqh pythagorean_proof.py PythagoreanProof     # 1080p
"""

from manim import *
import numpy as np

from themed_scene import ThemedScene


class PythagoreanProof(ThemedScene):

    def construct(self):
        t = self.theme

        # 3-4-5 triangle scaled to fit screen (a=1.2, b=1.6, c=2.0)
        a, b = 1.2, 1.6
        s = a + b   # 2.8 — side of the big square
        h = s / 2   # 1.4 — half-side for centering

        self._hook(t)
        self._show_triangle(t, a, b)
        self._show_proof(t, a, b, s, h)
        self._conclude(t)

    # ------------------------------------------------------------------
    # Scene 1: Setup — pose the question (≈8 s)
    # ------------------------------------------------------------------
    def _hook(self, t):
        title = Text("The Pythagorean Theorem", font_size=t.title_size)
        self.play(Write(title), run_time=1.5)
        self.wait(1)

        eq = MathTex(r"a^2", r"+", r"b^2", r"=", r"c^2", font_size=56)
        eq[0].set_color(t.primary)
        eq[2].set_color(t.accent)
        eq[4].set_color(t.tertiary)

        self.play(FadeOut(title, shift=0.3 * UP), FadeIn(eq, shift=0.3 * UP))
        self.wait(1)

        why = Text("Why?", font_size=40, color=t.accent2)
        why.next_to(eq, DOWN, buff=0.5)
        self.play(FadeIn(why))
        self.wait(1.5)  # let curiosity build

        self.play(FadeOut(eq), FadeOut(why))

    # ------------------------------------------------------------------
    # Scene 2: Foundation — introduce the right triangle (≈8 s)
    # ------------------------------------------------------------------
    def _show_triangle(self, t, a, b):
        tri = Polygon(
            ORIGIN, b * RIGHT, b * RIGHT + a * UP,
            stroke_color=t.foreground, stroke_width=t.axis_stroke_width,
            fill_color=t.primary, fill_opacity=0.4,
        )
        tri.move_to(ORIGIN)
        verts = tri.get_vertices()

        # Right-angle marker at vertex 1
        sz = 0.15
        v = verts[1]
        ra = VMobject(stroke_width=1.5, color=t.foreground)
        ra.set_points_as_corners([v + sz * UP, v + sz * (UP + LEFT), v + sz * LEFT])

        # Side labels (geometry before symbols)
        a_lab = MathTex("a", color=t.primary, font_size=32)
        a_lab.next_to((verts[1] + verts[2]) / 2, RIGHT, buff=0.15)

        b_lab = MathTex("b", color=t.accent, font_size=32)
        b_lab.next_to((verts[0] + verts[1]) / 2, DOWN, buff=0.15)

        c_lab = MathTex("c", color=t.tertiary, font_size=32)
        c_lab.next_to((verts[0] + verts[2]) / 2, UL, buff=0.15)

        self.play(Create(tri), run_time=1.5)
        self.play(FadeIn(ra), run_time=0.5)
        self.play(
            LaggedStart(Write(b_lab), Write(a_lab), Write(c_lab), lag_ratio=0.3),
            run_time=1.5,
        )
        self.wait(1.5)  # let viewer absorb
        self.play(FadeOut(VGroup(tri, ra, a_lab, b_lab, c_lab)), run_time=0.8)

    # ------------------------------------------------------------------
    # Scene 3-4: Build — two arrangements side-by-side (≈20 s)
    # ------------------------------------------------------------------
    def _show_proof(self, t, a, b, s, h):
        left_x = -3.2
        right_x = 3.2
        vert_shift = 1.0 * UP  # shift diagrams up to leave room for equations

        # ---- LEFT: Arrangement 1 — tilted c² square in center --------
        o1 = Square(side_length=s, stroke_color=t.foreground, stroke_width=t.axis_stroke_width)
        o1.shift(left_x * RIGHT + vert_shift)

        t1_polys = VGroup(
            Polygon([-h, -h, 0], [-h + b, -h, 0], [-h, -h + a, 0]),
            Polygon([-h + b, -h, 0], [h, -h, 0], [h, -h + b, 0]),
            Polygon([h, -h + b, 0], [h, h, 0], [h - b, h, 0]),
            Polygon([h - b, h, 0], [-h, h, 0], [-h, -h + a, 0]),
        )
        for tri in t1_polys:
            tri.set_stroke(t.foreground, 1.5).set_fill(t.primary, 0.5)
        t1_polys.shift(left_x * RIGHT + vert_shift)

        inner = Polygon(
            [-h, -h + a, 0], [-h + b, -h, 0], [h, -h + b, 0], [h - b, h, 0],
            stroke_color=t.tertiary, stroke_width=2.5,
            fill_color=t.tertiary, fill_opacity=0.25,
        )
        inner.shift(left_x * RIGHT + vert_shift)

        c_lab = MathTex(r"c^2", color=t.tertiary, font_size=t.body_size)
        c_lab.move_to(inner.get_center())

        head1 = Text("Arrangement 1", font_size=22, color=t.muted)
        head1.next_to(o1, UP, buff=0.25)

        # ---- RIGHT: Arrangement 2 — a² and b² squares ----------------
        mx = -h + b   # vertical divider x
        my = -h + a   # horizontal divider y

        o2 = Square(side_length=s, stroke_color=t.foreground, stroke_width=t.axis_stroke_width)
        o2.shift(right_x * RIGHT + vert_shift)

        t2_polys = VGroup(
            Polygon([-h, -h, 0], [mx, -h, 0], [mx, my, 0]),
            Polygon([-h, -h, 0], [mx, my, 0], [-h, my, 0]),
            Polygon([mx, my, 0], [h, my, 0], [h, h, 0]),
            Polygon([mx, my, 0], [h, h, 0], [mx, h, 0]),
        )
        for tri in t2_polys:
            tri.set_stroke(t.foreground, 1.5).set_fill(t.primary, 0.5)
        t2_polys.shift(right_x * RIGHT + vert_shift)

        sq_a = Polygon(
            [mx, -h, 0], [h, -h, 0], [h, my, 0], [mx, my, 0],
            stroke_color=t.primary, stroke_width=2.5,
            fill_color=t.primary, fill_opacity=0.25,
        )
        sq_a.shift(right_x * RIGHT + vert_shift)

        sq_b = Polygon(
            [-h, my, 0], [mx, my, 0], [mx, h, 0], [-h, h, 0],
            stroke_color=t.accent, stroke_width=2.5,
            fill_color=t.accent, fill_opacity=0.25,
        )
        sq_b.shift(right_x * RIGHT + vert_shift)

        a_lab = MathTex(r"a^2", color=t.primary, font_size=t.label_size)
        a_lab.move_to(sq_a.get_center())

        b_lab = MathTex(r"b^2", color=t.accent, font_size=t.label_size)
        b_lab.move_to(sq_b.get_center())

        head2 = Text("Arrangement 2", font_size=22, color=t.muted)
        head2.next_to(o2, UP, buff=0.25)

        # ---- Animate left arrangement ----
        self.play(Create(o1), FadeIn(head1), run_time=1)
        self.play(
            LaggedStart(*[Create(tri) for tri in t1_polys], lag_ratio=0.15),
            run_time=1.5,
        )
        self.play(Create(inner), run_time=1)
        self.wait(0.5)

        # ---- Prove the inner shape is a square with side c ----
        self._prove_inner_is_c_squared(
            t, inner, t1_polys, c_lab, o1, a, b, h, left_x, vert_shift,
        )

        # ---- Animate right arrangement ----
        self.play(Create(o2), FadeIn(head2), run_time=1)
        self.play(
            LaggedStart(*[Create(tri) for tri in t2_polys], lag_ratio=0.15),
            run_time=1.5,
        )
        self.play(Create(sq_a), Create(sq_b), run_time=1)
        self.play(Write(a_lab), Write(b_lab), run_time=0.8)
        self.wait(1)

        # ---- Step-by-step reasoning: WHY the leftover is equal ----

        # Step 1: Both outer squares have the same area
        step1 = MathTex(
            r"\text{Total area}", r"=", r"(a+b)^2",
            font_size=30,
        )
        step1[2][1].set_color(t.primary)   # a
        step1[2][3].set_color(t.accent)    # b
        step1.next_to(VGroup(o1, o2), DOWN, buff=0.35)

        self.play(
            Indicate(o1, color=t.foreground, scale_factor=1.02),
            Indicate(o2, color=t.foreground, scale_factor=1.02),
            run_time=1,
        )
        self.play(Write(step1), run_time=1.2)
        self.wait(0.8)

        # Step 2: Both contain 4 identical triangles
        step2 = MathTex(
            r"\text{4 triangles}", r"=",
            r"4 \cdot \tfrac{1}{2}", r"a", r"b",
            font_size=30,
        )
        step2[3].set_color(t.primary)
        step2[4].set_color(t.accent)
        step2.next_to(step1, DOWN, buff=0.25)

        # Flash all 8 triangles simultaneously to show they match
        self.play(
            *[Indicate(tri, color=t.primary, scale_factor=1.03) for tri in t1_polys],
            *[Indicate(tri, color=t.primary, scale_factor=1.03) for tri in t2_polys],
            run_time=1,
        )
        self.play(Write(step2), run_time=1.2)
        self.wait(0.8)

        # Step 3: Subtract → leftover area must be equal in both
        step3 = MathTex(
            r"\text{Leftover}", r"=",
            r"(a+b)^2", r"-", r"4 \cdot \tfrac{1}{2}", r"a", r"b",
            font_size=30,
        )
        step3[2][1].set_color(t.primary)
        step3[2][3].set_color(t.accent)
        step3[5].set_color(t.primary)
        step3[6].set_color(t.accent)
        step3.next_to(step2, DOWN, buff=0.25)

        self.play(Write(step3), run_time=1.2)
        self.wait(1)

        # Step 4: Show what the leftover IS in each arrangement
        step4 = MathTex(
            r"\underbrace{c^2}_{\text{Arr. 1}}",
            r"=",
            r"\underbrace{a^2 + b^2}_{\text{Arr. 2}}",
            font_size=34,
        )
        step4[0][0:2].set_color(t.tertiary)    # c²
        step4[2][0:2].set_color(t.primary)      # a²
        step4[2][3:5].set_color(t.accent)       # b²
        step4.next_to(step3, DOWN, buff=0.3)

        # Pulse each arrangement's leftover as its side of the equation appears
        self.play(
            Indicate(inner, color=t.tertiary, scale_factor=1.05),
            FadeIn(step4[0]),
            run_time=1.2,
        )
        self.play(FadeIn(step4[1]), run_time=0.4)
        self.play(
            Indicate(sq_a, color=t.primary, scale_factor=1.05),
            Indicate(sq_b, color=t.accent, scale_factor=1.05),
            FadeIn(step4[2]),
            run_time=1.2,
        )
        self.wait(2.5)  # long pause — the "aha" moment

        self.proof_objects = VGroup(
            o1, t1_polys, inner, c_lab, head1,
            o2, t2_polys, sq_a, sq_b, a_lab, b_lab, head2,
            step1, step2, step3, step4,
        )

    # ------------------------------------------------------------------
    # Helper: Prove the inner tilted shape is a square with side c
    # ------------------------------------------------------------------
    def _prove_inner_is_c_squared(self, t, inner, t1_polys, c_lab, o1, a, b, h, left_x, vert_shift):
        offset = np.array([left_x, 0, 0]) + vert_shift

        # --- Step A: Each side is the hypotenuse of a right triangle → length c ---
        tri0 = t1_polys[0]
        hyp_line = Line(
            np.array([-h, -h + a, 0]) + offset,
            np.array([-h + b, -h, 0]) + offset,
            color=t.tertiary, stroke_width=4,
        )
        c_side_label = MathTex("c", color=t.tertiary, font_size=26)
        c_side_label.next_to(hyp_line.get_center(), DR, buff=0.1)

        side_note = MathTex(
            r"\text{Each side} = c \text{ (hypotenuse)}",
            font_size=t.label_size, color=t.tertiary,
        )
        side_note.next_to(o1, DOWN, buff=0.25)

        self.play(
            Indicate(tri0, color=t.primary, scale_factor=1.03),
            Create(hyp_line),
            run_time=1,
        )
        self.play(Write(c_side_label), run_time=0.6)
        self.play(Write(side_note), run_time=1)
        self.wait(1)

        # --- Step B: Each interior angle = 90° ---
        v0 = np.array([-h, -h, 0]) + offset
        v1 = np.array([-h + b, -h, 0]) + offset
        v2 = np.array([-h, -h + a, 0]) + offset

        alpha_label = MathTex(r"\alpha", font_size=t.small_size, color=t.accent2)
        alpha_label.move_to(v2 + np.array([0.25, -0.2, 0]))

        beta_label = MathTex(r"\beta", font_size=t.small_size, color=t.secondary)
        beta_label.move_to(v1 + np.array([-0.2, 0.25, 0]))

        self.play(Write(alpha_label), Write(beta_label), run_time=0.8)
        self.wait(0.5)

        # Show α + β = 90° (since the triangle has a right angle)
        angle_eq1 = MathTex(
            r"\alpha", r"+", r"\beta", r"= 90^\circ",
            font_size=t.label_size,
        )
        angle_eq1[0].set_color(t.accent2)
        angle_eq1[2].set_color(t.secondary)
        angle_eq1.next_to(side_note, DOWN, buff=0.2)

        self.play(Write(angle_eq1), run_time=1)
        self.wait(0.8)

        # Show the vertex angle: at each inner vertex, the angle = 180° - α - β = 90°
        angle_eq2 = MathTex(
            r"\text{Inner angle}", r"=",
            r"180^\circ", r"-", r"\alpha", r"-", r"\beta",
            r"= 90^\circ",
            font_size=t.label_size,
        )
        angle_eq2[4].set_color(t.accent2)
        angle_eq2[6].set_color(t.secondary)
        angle_eq2.next_to(angle_eq1, DOWN, buff=0.2)

        self.play(Write(angle_eq2), run_time=1.2)
        self.wait(1)

        # --- Step C: Conclude → it's a square with area c² ---
        conclusion = MathTex(
            r"\Rightarrow", r"\text{square with area } c^2",
            font_size=26, color=t.tertiary,
        )
        conclusion.next_to(angle_eq2, DOWN, buff=0.2)

        self.play(
            Indicate(inner, color=t.tertiary, scale_factor=1.05),
            Write(conclusion),
            run_time=1.2,
        )
        self.play(Write(c_lab), run_time=0.6)
        self.wait(1.5)

        # Clean up the sub-proof annotations
        sub_proof = VGroup(
            hyp_line, c_side_label, side_note,
            alpha_label, beta_label,
            angle_eq1, angle_eq2, conclusion,
        )
        self.play(FadeOut(sub_proof), run_time=0.8)

    # ------------------------------------------------------------------
    # Scene 5: Resolution — final statement (≈5 s)
    # ------------------------------------------------------------------
    def _conclude(self, t):
        self.play(FadeOut(self.proof_objects), run_time=1)

        final = MathTex(r"a^2", r"+", r"b^2", r"=", r"c^2", font_size=72)
        final[0].set_color(t.primary)
        final[2].set_color(t.accent)
        final[4].set_color(t.tertiary)

        box = SurroundingRectangle(final, color=t.accent2, buff=0.3, stroke_width=t.axis_stroke_width)

        self.play(Write(final), run_time=1.5)
        self.play(Create(box), run_time=0.8)

        qed = MathTex(r"\blacksquare", font_size=32)
        qed.next_to(box, DR, buff=0.15)
        self.play(FadeIn(qed))
        self.wait(2)
