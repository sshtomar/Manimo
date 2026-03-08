# Mathematical Art: Curated Research

A comprehensive collection of the best replicable mathematical art projects, repositories, notebooks, and tools.

---

## Top-Tier Projects (Start Here)

### 1. Manim -- Mathematical Animation Engine (3Blue1Brown)
- **Repo**: [3b1b/manim](https://github.com/3b1b/manim) | [ManimCommunity/manim](https://github.com/ManimCommunity/manim)
- **Language**: Python
- **Concepts**: Arbitrary mathematical animations -- transforms, graphs, geometry, calculus
- **Replicability**: `pip install manim`. Thousands of community examples. The [3b1b/videos](https://github.com/3b1b/videos) repo has source for all 3Blue1Brown videos.
- The gold standard for mathematical animation.

### 2. marcusvolz/mathart -- Mathematical Art in R
- **Repo**: [marcusvolz/mathart](https://github.com/marcusvolz/mathart)
- **Language**: R
- **Concepts**: Parametric equations, harmonographs, shell curves, Lissajous forms, knots, rose curves
- One of the most polished dedicated math-art libraries. Produces elegant, minimalist line art suitable for gallery display.

### 3. Reaction-Diffusion Playground
- **Repo**: [jasonwebb/reaction-diffusion-playground](https://github.com/jasonwebb/reaction-diffusion-playground)
- **Language**: JavaScript / WebGL
- **Concepts**: Gray-Scott reaction-diffusion, Turing patterns
- Live browser demo with parameter sliders. Exceptional organic, Turing-pattern visuals in real time.

### 4. Inigo Quilez -- Mathematical Shader Art
- **Site**: [iquilezles.org/articles](https://iquilezles.org/articles/)
- **Platform**: GLSL / [Shadertoy](https://www.shadertoy.com)
- **Concepts**: Domain warping, FBM, signed distance fields, Voronoi noise, raymarching
- Considered one of the greatest shader artists. His techniques underpin most modern procedural art.

---

## By Category

## Fractals

### 2D Fractals
| Project | Language | Notes |
|---------|----------|-------|
| [jonnyhyman/Chaos](https://github.com/jonnyhyman/Chaos) | Python | Made for Veritasium. Reveals the Mandelbrot set hidden beneath the bifurcation diagram. |
| [rytheranderson/pyfracgen](https://github.com/rytheranderson/pyfracgen) | Python | Mandelbrot, Julia, Buddhabrot sets with custom coloring. Clean API. |
| [sauxpa/Fractal](https://github.com/sauxpa/Fractal) | Python (Jupyter) | Burning Ship, chaos game, Julia, quaternion Julia sets (4D to 3D projection). |
| [mk12/chaos](https://github.com/mk12/chaos) | C | Julia sets, Mandelbrot, Tricorn. Fast and lightweight. |
| [pedrotrschneider/shader-fractals](https://github.com/pedrotrschneider/shader-fractals) | GLSL | GPU-accelerated 2D/3D fractals (Sierpinski, Julia, Koch, Mandelbulb). |
| [mattsaccount364/FractalShark](https://github.com/mattsaccount364/FractalShark) | C++/CUDA | Extreme deep-zoom Mandelbrot with GPU acceleration. |
| [koenderks/aRtsy](https://koenderks.github.io/aRtsy/) | R | Mandelbrot, Julia, Multibrot, Burning Ship, flow fields, cellular automata. One-liner art with `canvas_*()` functions. |

### 3D Fractals
| Project | Language | Notes |
|---------|----------|-------|
| [buddhi1980/mandelbulber2](https://github.com/buddhi1980/mandelbulber2) | C++/Qt | The most feature-complete open-source 3D fractal explorer. |
| [thargor6/mb3d](https://github.com/thargor6/mb3d) | Delphi | Classic Mandelbulb 3D with massive community and shared parameter files. |
| [AstroKriel/Mandelbulb](https://github.com/AstroKriel/Mandelbulb) | Python | Ray-marching Mandelbulb renderer. Clean, educational implementation. |

---

## Strange Attractors & Chaos Theory

| Project | Language | Notes |
|---------|----------|-------|
| [vdesmond/attractors](https://github.com/vdesmond/attractors) | Python | 20+ attractors (Lorenz, Rossler, Chen, Halvorsen). `pip install attractors`. |
| [jonnyhyman/Chaos](https://github.com/jonnyhyman/Chaos) | Python | Cobweb plots, bifurcation diagrams, Mandelbrot-bifurcation connection. |
| [gboeing/lorenz-system](https://github.com/gboeing/lorenz-system) | Python (Jupyter) | Lorenz system model and animation in notebook format. |
| [xIvqn/chaos-theory](https://github.com/xIvqn/chaos-theory) | C++/OpenGL | Interactive Lorenz Attractor with real-time 3D rotation. |
| [DorsaRoh/Chaos-Theory](https://github.com/DorsaRoh/Chaos-Theory) | Python | Configurable chaos systems: trajectories, logistic maps, bifurcation. |

---

## Fourier Series Drawing

| Project | Language | Notes |
|---------|----------|-------|
| [shiffman/Fourier-Drawings](https://github.com/shiffman/Fourier-Drawings) | JavaScript/p5.js | Daniel Shiffman's epicycle drawings. Companion to Coding Train video. |
| [Grzetan/ImageToFourierSeries](https://github.com/Grzetan/ImageToFourierSeries) | Python | Full pipeline: edge detection, point sorting, DFT, epicycle animation. |
| [skyzh/fourier-transform-drawing](https://github.com/skyzh/fourier-transform-drawing) | JavaScript | SVG-to-epicycles workflow, inspired by 3Blue1Brown. |
| [trozler/myFourierEpicycles](https://github.com/trozler/myFourierEpicycles) | JavaScript | Draw freehand and see the decomposition. Interactive + educational. |

---

## L-Systems (Lindenmayer Systems)

| Project | Language | Notes |
|---------|----------|-------|
| [arendsee/lsystems](https://github.com/arendsee/lsystems) | Haskell | Context-dependent, parameterized, stochastic L-systems. |
| [miaisakovic/l-system-drawings](https://github.com/miaisakovic/l-system-drawings) | Python | Beginner-friendly turtle graphics L-systems. |
| [FrancescoGradi/L-System-Trees](https://github.com/FrancescoGradi/L-System-Trees) | JavaScript/Three.js | 3D procedural trees and botanical forms in real time. |
| [cormullion/Lindenmayer.jl](https://github.com/cormullion/Lindenmayer.jl) | Julia | Fast recursive graphics with Luxor.jl. |
| [taylorlapeyre/l-system-art](https://github.com/taylorlapeyre/l-system-art) | JavaScript | Browser-based L-system rendering via canvas. |

---

## Space-Filling Curves

| Project | Language | Notes |
|---------|----------|-------|
| [google/hilbert](https://github.com/google/hilbert) | Go | Google's production-quality Hilbert/Peano curve library. |
| [jakubcerveny/gilbert](https://github.com/jakubcerveny/gilbert) | Python/C | Generalized Hilbert curves for non-power-of-two rectangular domains. |
| [timotius02/Hilbert-Curve-Rendering](https://github.com/timotius02/Hilbert-Curve-Rendering) | JavaScript | Image drawing with Hilbert curves, order interpolation. |
| [stanislavfort/hilbert-curves](https://github.com/stanislavfort/hilbert-curves) | Python | 3D Hilbert curves via L-systems and turtle graphics. |

---

## Penrose Tilings & Quasiperiodic Patterns

| Project | Language | Notes |
|---------|----------|-------|
| [aatishb/patterncollider](https://github.com/aatishb/patterncollider) | JavaScript | Interactive de Bruijn multigrid tool for Penrose tilings. |
| [JesusFreke/pynrose](https://github.com/JesusFreke/pynrose) | Python | P3 Penrose tiling via de Bruijn method. |
| [xnx/penrose](https://github.com/xnx/penrose) | Python | `pip install`-able Penrose tiling generator. |
| [apaleyes/penrose-tiling](https://github.com/apaleyes/penrose-tiling) | JavaScript | Zero-dependency triangle decomposition approach. |
| [JesusFreke/ptgen](https://github.com/JesusFreke/ptgen) | Go | SVG output designed for CNC milling/engraving. |

---

## Hyperbolic Geometry

| Project | Language | Notes |
|---------|----------|-------|
| [looeee/hyperbolic-tiling](https://github.com/looeee/hyperbolic-tiling) | JavaScript | EscherSketch -- Escher Circle Limit-inspired tilings. |
| [soma-arc/HyperbolicTessellator](https://github.com/soma-arc/HyperbolicTessellator) | JavaScript/WebGL | Tessellates webcam video in hyperbolic plane. |
| [cduck/hyperbolic](https://github.com/cduck/hyperbolic) | Python | Clean API for programmatic hyperbolic geometry, SVG output. |
| [skociu/hyperbolic-tessellation](https://github.com/skociu/hyperbolic-tessellation) | Python | Poincare disk model tessellations. |
| [dmishin/hyperbolic-ca-simulator](https://github.com/dmishin/hyperbolic-ca-simulator) | JavaScript | Cellular automata on hyperbolic plane -- mesmerizing patterns. |

---

## Reaction-Diffusion

| Project | Language | Notes |
|---------|----------|-------|
| [jasonwebb/reaction-diffusion-playground](https://github.com/jasonwebb/reaction-diffusion-playground) | JavaScript/WebGL | Live browser demo with sliders. Real-time Turing patterns. |
| [colejd/Reaction-Diffusion-ThreeJS](https://github.com/colejd/Reaction-Diffusion-ThreeJS) | JavaScript/Three.js | GPU-accelerated, mobile-friendly. |
| [benmaier/reaction-diffusion](https://github.com/benmaier/reaction-diffusion) | Python (Jupyter) | Tutorial notebook with animation generation. |

---

## Flow Fields & Noise Art

| Project | Language | Notes |
|---------|----------|-------|
| [mkfreeman/flowFields](https://github.com/mkfreeman/flowFields) | JavaScript | Perlin noise particle trails create painterly compositions. |
| [timpyrkov/procedural-art](https://github.com/timpyrkov/procedural-art) | Python | Perlin noise producing water caustics, marble, wood textures. |
| [Sighack](https://sighack.com/post/getting-creative-with-perlin-noise-fields) | Processing (Java) | 25 distinct gallery-quality designs from one Perlin noise algorithm. |

---

## Parametric Surfaces

| Project | Language | Notes |
|---------|----------|-------|
| [cx20/webgl-parametric-surface-examples](https://github.com/cx20/webgl-parametric-surface-examples) | JavaScript/WebGL | Same surface in 10+ frameworks (three.js, p5.js, Babylon.js). |
| [elfnor/blender_XYZ_surface_presets](https://github.com/elfnor/blender_XYZ_surface_presets) | Python/Blender | Parametric surface library for Blender. |
| [joh/texture-surface](https://github.com/joh/texture-surface) | OpenSCAD | Bump-mapped parametric surfaces for 3D printing. |

---

## Generative Art Frameworks

| Project | Language | Notes |
|---------|----------|-------|
| [martinmcbride/generativepy](https://github.com/martinmcbride/generativepy) | Python | Batteries-included for math-art beginners. |
| [qiray/MathArtist](https://github.com/qiray/MathArtist) | Python | Expression trees map (x,y) to colors -- surprising emergent images. |
| [koenderks/aRtsy](https://koenderks.github.io/aRtsy/) | R | One-liner generative art with `canvas_*()` functions. |
| [mattdesl/workshop-generative-art](https://github.com/mattdesl/workshop-generative-art) | JavaScript | Professional creative coding workshop materials. |

---

## Spirograph & Curves

| Project | Language | Notes |
|---------|----------|-------|
| [seedcode/SpirographN](https://github.com/seedcode/SpirographN) | JavaScript | N-rotor spirograph (beyond classic 2-circle). |
| [ddeveloper72/spirographs-py](https://github.com/ddeveloper72/spirographs-py) | Python | Parametric spirograph with turtle graphics. |

---

## Computational Origami

| Project | Language | Notes |
|---------|----------|-------|
| [bugfolder/TreeMaker](https://github.com/bugfolder/treemaker) | C++ | Robert J. Lang's TreeMaker 5.0 -- foundational tool that launched computational origami. Used by NASA for solar array folds. |

---

## Shader Art & GPU Math

| Resource | Notes |
|----------|-------|
| [iquilezles.org](https://iquilezles.org/) | SDF functions, procedural palettes, mathematical paintings. The most important resource for shader art. |
| [Shadertoy fractal collection](https://www.shadertoy.com/results?query=tag%3Dfractal) | Hundreds of real-time browser-editable fractal shaders. |
| [The Book of Shaders](https://thebookofshaders.com/14/) | Interactive textbook for GLSL with fractals chapter. |
| [dfranx/SHADERed](https://github.com/dfranx/SHADERed) | Lightweight shader IDE with visual debugger. |

---

## Courses & Workshops

| Course | Institution | Notes |
|--------|-------------|-------|
| [yue-sun/generative-art](https://github.com/yue-sun/generative-art) | Harvard | "Intro to Generative Art and Scientific Visualization" -- math equations, physical systems, algorithmic patterns. |
| [gvarnavi/generative-art-iap](https://github.com/gvarnavi/generative-art-iap) | MIT | IAP workshop on generative art at the math-aesthetics intersection. |

---

## Curated Lists & Meta-Resources

| List | Notes |
|------|-------|
| [terkelg/awesome-creative-coding](https://github.com/terkelg/awesome-creative-coding) | The definitive curated list. Covers frameworks, tools, artists, learning resources. |
| [ubavic/awesome-interactive-math](https://github.com/ubavic/awesome-interactive-math) | Tools for interactive mathematical explorables (CindyJS, MathBox, p5.js, JSXGraph). |
| [rossant/awesome-math](https://github.com/rossant/awesome-math) | Broad math resources including Bridges conference on math-art. |
| [GitHub Topics: math-art](https://github.com/topics/math-art) | Community-tagged topic page. |

---

## Notable Creative Coders

- **Daniel Shiffman** ([The Coding Train](https://thecodingtrain.com/)) -- Fourier drawings, Nature of Code, hundreds of math-art challenges
- **Inigo Quilez** ([iquilezles.org](https://iquilezles.org/)) -- Co-creator of Shadertoy, mathematical paintings in pure GLSL
- **Matt DesLauriers** ([mattdesl](https://github.com/mattdesl)) -- Framework author for generative artwork in JavaScript/canvas/WebGL

---

## Platforms for Interactive Math Art

- **[Observable HQ](https://observablehq.com/)** -- Reactive JavaScript notebooks, perfect for parametric math art
- **[Shadertoy](https://www.shadertoy.com/)** -- Browser-based GLSL shader editor with massive community
- **[MathBox](https://christopherchudzicki.github.io/MathBox-Demos/parametric_surfaces_3D.html)** -- Presentation-quality 3D math visualizations in the browser
