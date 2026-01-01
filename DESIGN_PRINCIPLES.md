# Manimo Design Principles

*Adapted from Inquiro's design principles for mathematical animation*

## Core Philosophy

Good design is not subjective. When we build animation tools for mathematical educators, we can objectively evaluate whether we're solving real problems elegantly. These principles guide every product decision.

## 1. Simplicity: Strip Away Everything That Isn't Truth

**Principle**: A shorter proof is better. Fewer abstractions, less cognitive load, more clarity.

**For Manimo**:
- **No custom JSON notebook format** — Use Marimo's `.py` source files. Python is the interface.
- **No intermediate DSLs** — Animation code should look like animators wrote it, not like framework boilerplate.
- **One agent, not three** — Skills-based single-agent architecture (2 LLM calls) beats multi-agent complexity.
- **Explicit over implicit** — Clear timing, easing, and composition choices.

## 2. Timelessness: Build for 1500 and 2500

**Principle**: Animation principles that work today will work in the future.

**For Manimo**:
- **Animation principles by default** — Timing, easing, composition. These won't become optional.
- **Mathematical accuracy** — Correct scales, proportions, relationships. This is timeless.
- **Marimo over Jupyter** — Reactive execution and Python source files solve problems that will matter.
- **R2 + Modal over ephemeral clouds** — Durable storage + isolated compute is timeless architecture.

## 3. Solve the Right Problem

**Principle**: Focus on what matters.

**For Manimo**:
- **Problem is not "make animations faster"** — It's "make animations mathematically accurate and pedagogically effective."
- **Problem is not "automate all animation"** — It's "handle syntax so creators focus on design and teaching."
- **Problem is not "better autocomplete"** — It's "encode accumulated animation wisdom" (skills framework).

## 4. Suggestive, Not Prescriptive

**Principle**: Skills propose patterns, not complete solutions.

**For Manimo**:
- **Skills propose patterns** — "Here's how to do timing with easing" not "Here's your entire animation."
- **Marimo cells are Lego blocks** — Compose them how you want.
- **Diffs over rewrites** — AI suggests changes; you decide what to accept.

## 5. Hard Problems Force Elegance

**Principle**: Difficult constraints force elegant designs.

**For Manimo**:
- **Mathematical accuracy is hard** — Forces us to use proper coordinate systems, scales, labels.
- **Animation quality is hard** — Forces skills framework instead of generic LLM chat.
- **Video rendering is hard** — Forces optimization, quality settings, format choices.
- **Educational effectiveness is hard** — Forces us to understand animation principles deeply.

## 6. Looks Easy (The Eighth Rewrite)

**Principle**: Great design looks effortless.

**For Manimo**:
- **"Just describe your animation"** — Looks simple. Actually: skills registry, two-pass generation, validation, video rendering, R2 orchestration, Modal sandboxing.
- **Launch notebook → URL in seconds** — Looks instant. Actually: warm containers, minimal images, immediate URL return.
- **"AI that understands animation"** — Looks natural. Actually: curated skills, mandatory compliance, built-in validation.

## 7. Uses Symmetry (Repetition and Recursion)

**Principle**: Nature uses symmetry. So should we.

**For Manimo**:
- **Every cell follows same pattern** — `@app.cell`, docstring, scene creation, return statement.
- **Every skill has same structure** — Problem → Principles → Patterns → Pitfalls.
- **Every animation has same anatomy** — Setup → Create → Animate → Cleanup.

## 8. Resembles Nature (Copy the Best Solutions)

**Principle**: Copy established practice, don't invent new methods.

**For Manimo**:
- **Animation principles from Disney, Pixar** — Timing, easing, composition. Copy established practice.
- **Mathematical visualization standards** — Scales, labels, coordinate systems. Copy established practice.
- **Manim API patterns** — Scene, Mobject, Animation classes. Use the library as designed.

## 9. Redesign is the Design

**Principle**: Experts expect to throw away early work.

**For Manimo**:
- **Version everything** — R2 stores `versions/notebook-timestamp.py`. Never lose work.
- **Diffs over overwrites** — AI proposes changes, you review.
- **Iteration is expected** — "Ask AI" isn't one-shot. It's a conversation with your animation.

## 10. Copy Without Shame (Be Right, Not Original)

**Principle**: The greatest masters are confident enough to take from anyone.

**For Manimo**:
- **Marimo over custom notebooks** — They solved reactivity and reproducibility. Use it.
- **Modal over DIY container orchestration** — They solved isolated compute. Use it.
- **Anthropic's skills pattern** — They solved structured LLM output. Use it.
- **Established animation principles** — Disney, Pixar solved animation. Teach it, don't replace it.

