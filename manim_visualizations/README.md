# Manim Mathematical Visualizations

Beautiful animated visualizations of mathematical concepts using Manim (Mathematical Animation Engine), inspired by 3Blue1Brown's visual style.

## Categories

### 1. Linear Transformations
- Matrix multiplication interpretations
- Basis vector transformations
- Composition of transformations
- Shear, rotation, and other common transforms

### 2. Calculus Visualizations
- Animated function plotting
- Tangent lines and derivatives
- Secant → tangent limit definition
- Riemann sums → definite integrals
- Fundamental Theorem of Calculus

### 3. Pythagorean Theorem Proofs
- Bhaskara's "Behold!" proof
- Classic rearrangement proof
- Area-based proof
- Euclid's similar triangles proof
- Garfield's trapezoid proof

## Prerequisites

### 1. LaTeX (Required for mathematical typesetting)

**macOS:**
```bash
# Option 1: Full MacTeX (4GB+)
brew install --cask mactex

# Option 2: BasicTeX (minimal, ~100MB)
brew install --cask basictex
# After installation, restart terminal and run:
sudo tlmgr update --self
sudo tlmgr install standalone preview doublestroke relsize fundus-calligra wasysym physics dvisvgm.aarch64-darwin rsfs wasy jknapltx
```

**Ubuntu/Debian:**
```bash
sudo apt-get install texlive-full
```

### 2. System dependencies

**macOS:**
```bash
brew install cairo pango ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install libcairo2-dev libpango1.0-dev ffmpeg
```

## Installation

```bash
cd manim_visualizations
uv sync
```

## Usage

### Interactive Marimo Notebook

```bash
uv run marimo edit notebook.py
```

### Command Line

```bash
# List all available scenes
uv run python render.py --list

# Render a specific scene
uv run python render.py linear BasisVectorTransformation
uv run python render.py calculus TangentLineDerivative
uv run python render.py pythag BhaskaraProof

# Render with higher quality
uv run python render.py linear BasisVectorTransformation --quality m  # 720p
uv run python render.py linear BasisVectorTransformation --quality h  # 1080p

# Render all scenes in a category
uv run python render.py --all linear
uv run python render.py --all calculus
uv run python render.py --all pythag
```

### Direct Manim Commands

```bash
# Low quality (fast preview)
uv run manim -ql linear_transformations.py LinearTransformationIntro

# Medium quality
uv run manim -qm calculus_visualizations.py TangentLineDerivative

# High quality with preview
uv run manim -qh -p pythagorean_proofs.py BhaskaraProof

# Render all scenes in a file
uv run manim -ql -a linear_transformations.py
```

## Scene Reference

### Linear Transformations (`linear_transformations.py`)

| Scene | Description |
|-------|-------------|
| `LinearTransformationIntro` | Watch the 2D plane transform under a matrix |
| `BasisVectorTransformation` | Matrix columns = transformed basis vectors |
| `MatrixMultiplicationAsComposition` | AB = apply B, then A |
| `DotProductInterpretation` | Row × Column = Dot Product |
| `ShearTransformation` | Shear matrix visualization |
| `RotationTransformation` | 45° rotation in action |
| `AllTransformations` | Gallery of common transformations |

### Calculus (`calculus_visualizations.py`)

| Scene | Description |
|-------|-------------|
| `FunctionPlotAnimation` | Watch functions get drawn |
| `TangentLineDerivative` | Moving tangent shows derivative value |
| `SecantToTangent` | Limit definition of derivative |
| `RiemannSumsToIntegral` | n → ∞, rectangles → exact area |
| `DerivativeIntegralRelation` | Fundamental Theorem of Calculus |
| `AreaAccumulation` | ∫f(t)dt as accumulated area |
| `PowerRuleDerivative` | d/dx[x^n] = nx^(n-1) |

### Pythagorean Theorem (`pythagorean_proofs.py`)

| Scene | Description |
|-------|-------------|
| `PythagoreanIntro` | Introduction to a² + b² = c² |
| `BhaskaraProof` | "Behold!" - dissection into 4 triangles + inner square |
| `RearrangementProof` | Two (a+b)² squares, same triangles, different arrangement |
| `AreaBasedProof` | Squares on each side of the triangle |
| `EuclideanProof` | Similar triangles from altitude to hypotenuse |
| `PresidentialProof` | James Garfield's trapezoid proof (1876) |
| `AnimatedProofSummary` | Quick animated summary |

## Output

Rendered videos are saved to `media/videos/<module_name>/<quality>/`:
- `480p15/` - Low quality (15 fps)
- `720p30/` - Medium quality (30 fps)
- `1080p60/` - High quality (60 fps)

## Customization

Edit the Python files to customize:
- Triangle dimensions in Pythagorean proofs
- Matrix values in linear transformation examples
- Function definitions in calculus visualizations
- Colors, speeds, and animation timings

## Credits

- [Manim Community Edition](https://www.manim.community/)
- Inspired by [3Blue1Brown](https://www.3blue1brown.com/)
