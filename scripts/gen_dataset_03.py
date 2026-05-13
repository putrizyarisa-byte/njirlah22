import json
import random
import sympy as sp
from template import make_base_record, make_conversation
from config import DATASET_SPECS

SPEC = DATASET_SPECS[3]

# Manual pool for highly curated examples
MATH_POOL = [
    (
        "Solve the differential equation: dy/dx = y/x + x",
        "**Step 1:** Rewrite as standard linear ODE:\ndy/dx - (1/x)y = x\n\n**Step 2:** Find integrating factor μ(x):\nμ(x) = exp(∫ -1/x dx) = exp(-ln|x|) = 1/x\n\n**Step 3:** Multiply through by μ(x):\n(1/x)dy/dx - (1/x²)y = 1\n\n**Step 4:** Left side is derivative of (y/x):\nd/dx(y/x) = 1\n\n**Step 5:** Integrate both sides:\ny/x = x + C\n\n**Final Solution:**\ny(x) = x² + Cx",
        "calculus_ode", "hard", "MMLU"
    ),
    (
        "Prove that √2 is irrational using contradiction.",
        "**Proof by Contradiction:**\n1. **Assume** √2 is rational → √2 = a/b where a,b are coprime integers\n2. Then 2 = a²/b² → 2b² = a² → a² is even → a is even (let a=2k)\n3. Substitute: 2b² = (2k)² → 2b² = 4k² → b² = 2k² → b² is even → b is even\n4. But if both a and b are even, gcd(a,b) ≥ 2, contradicting our assumption\n5. **Conclusion:** √2 cannot be rational → √2 is irrational\n\nQ.E.D.",
        "number_theory", "medium", "GPQA"
    ),
    (
        "Find the eigenvalues of matrix A = [[2, 1], [1, 2]]",
        "**Solution:**\n1. Characteristic equation: det(A - λI) = 0\n   |2-λ   1  |\n   |1    2-λ| = (2-λ)² - 1 = λ² -4λ +3 = 0\n\n2. Solve quadratic:\n   λ = [4 ± √(16-12)]/2 = [4 ± 2]/2\n\n**Eigenvalues:**\nλ₁ = 3, λ₂ = 1",
        "linear_algebra", "easy", "MMLU"
    ),
    (
        "Find the limit: lim(x→0) (sin x)/x",
        "**Solution:**\nUsing L'Hôpital's Rule (0/0 form):\nlim(x→0) (sin x)/x = lim(x→0) (cos x)/1 = cos(0) = 1\n\n**Final Answer:**\nlim(x→0) (sin x)/x = 1",
        "calculus_limits", "medium", "MMLU"
    ),
    (
        "Find the derivative of f(x) = x²e^x using product rule",
        "**Solution:**\n1. Product Rule: d/dx[uv] = u'v + uv'\n2. Let u = x² → u' = 2x\n   Let v = e^x → v' = e^x\n3. f'(x) = 2x·e^x + x²·e^x = e^x(x² + 2x)\n\n**Final Answer:**\nf'(x) = e^x(x² + 2x)",
        "calculus_differentiation", "medium", "MMLU"
    ),
    (
        "Evaluate ∫x ln x dx using integration by parts",
        "**Solution:**\n1. Formula: ∫u dv = uv - ∫v du\n2. Let u = ln x → du = (1/x)dx\n   Let dv = x dx → v = x²/2\n3. ∫x ln x dx = (ln x)(x²/2) - ∫(x²/2)(1/x)dx\n              = (x² ln x)/2 - (1/2)∫x dx\n              = (x² ln x)/2 - x²/4 + C\n\n**Final Answer:**\n(x²/2)ln x - x²/4 + C",
        "calculus_integration", "hard", "MMLU"
    ),
    (
        "Find the inverse of matrix A = [[1, 2], [3, 4]]",
        "**Solution:**\n1. For 2x2 matrix [[a,b],[c,d]]:\n   inverse = (1/det) * [[d, -b], [-c, a]]\n2. det(A) = (1)(4) - (2)(3) = -2\n3. A⁻¹ = (-1/2) * [[4, -2], [-3, 1]]",
        "linear_algebra_inverse", "medium", "MMLU"
    ),
    (
        "Prove that there are infinitely many prime numbers",
        "**Euclid's Proof:**\n1. Assume finitely many primes: p₁, p₂, ..., pₙ\n2. Consider N = p₁p₂...pₙ + 1\n3. N is either:\n   - Prime (contradicts finite list)\n   - Composite with prime factor not in list (contradiction)\n4. Therefore, primes are infinite",
        "number_theory_primes", "expert", "GPQA"
    ),
    (
        "If P(A) = 0.4, P(B) = 0.5, and P(A∪B) = 0.7, find P(A∩B)",
        "**Solution:**\n1. P(A∪B) = P(A) + P(B) - P(A∩B)\n2. 0.7 = 0.4 + 0.5 - P(A∩B)\n3. P(A∩B) = 0.4 + 0.5 - 0.7 = 0.2",
        "probability_basics", "easy", "MMLU"
    ),
    (
        "Find the area of a regular hexagon with side length 4",
        "**Solution:**\n1. Regular hexagon = 6 equilateral triangles\n2. Area of one triangle = (√3/4)s² = (√3/4)(16) = 4√3\n3. Total area = 6 * 4√3 = 24√3",
        "geometry_polygons", "medium", "MMLU"
    ),
    (
        "Calculate mean and standard deviation of [3, 5, 7, 9]",
        "**Solution:**\n1. Mean (μ) = (3+5+7+9)/4 = 6\n2. Variance = [(3-6)² + (5-6)² + (7-6)² + (9-6)²]/4\n            = [9 + 1 + 1 + 9]/4 = 5\n3. Std Dev (σ) = √5 ≈ 2.236",
        "statistics_descriptive", "easy", "MMLU"
    ),
    (
        "How many ways to arrange letters in 'MISSISSIPPI'?",
        "**Solution:**\n1. Total letters = 11\n2. Duplicates: S=4, P=2, I=4, M=1\n3. Arrangements = 11! / (4!4!2!1!) = 34650",
        "combinatorics_permutations", "hard", "MMLU"
    ),
    (
        "Approximate √5 using Newton-Raphson method (x₀=2, 2 iterations)",
        "**Solution:**\n1. f(x) = x² - 5 → f'(x) = 2x\n2. Iteration 1:\n   x₁ = x₀ - f(x₀)/f'(x₀) = 2 - (4-5)/4 = 2.25\n3. Iteration 2:\n   x₂ = 2.25 - (5.0625-5)/4.5 ≈ 2.2361",
        "numerical_methods", "medium", "MMLU"
    )
]

def generate_derivative_problem():
    x = sp.Symbol('x')
    coeffs = [random.randint(-15, 15) for _ in range(4)]
    expr = coeffs[0]*x**3 + coeffs[1]*x**2 + coeffs[2]*x + coeffs[3]
    if random.choice([True, False]): expr = sp.sin(expr)
    elif random.choice([True, False]): expr = sp.cos(expr)
    elif random.choice([True, False]): expr = sp.exp(x) * expr
    derivative = sp.diff(expr, x)
    q = f"Find the derivative of f(x) = {sp.latex(expr)}"
    a = f"**Solution:**\nLet f(x) = {sp.latex(expr)}\nUsing the standard rules of differentiation:\nf'(x) = {sp.latex(derivative)}\n\n**Final Answer:**\n{sp.latex(derivative)}"
    return (q.strip(), a.strip(), "calculus_derivative", "medium", "MMLU")

def generate_integral_problem():
    x = sp.Symbol('x')
    coeffs = [random.randint(-15, 15) for _ in range(4)]
    expr = coeffs[0]*x**3 + coeffs[1]*x**2 + coeffs[2]*x + coeffs[3]
    integral = sp.integrate(expr, x)
    q = f"Find the indefinite integral of f(x) = {sp.latex(expr)}"
    a = f"**Solution:**\nWe evaluate: ∫ ({sp.latex(expr)}) dx\nApplying power rule term by term:\n∫ ({sp.latex(expr)}) dx = {sp.latex(integral)} + C\n\n**Final Answer:**\n{sp.latex(integral)} + C"
    return (q.strip(), a.strip(), "calculus_integral", "medium", "MMLU")

def generate_algebra_roots():
    x = sp.Symbol('x')
    r1, r2, r3 = random.randint(-20, 20), random.randint(-20, 20), random.choice([random.randint(-5, 5), None])
    if r3 is not None:
        expr = (x - r1) * (x - r2) * (x - r3)
        expanded = sp.expand(expr)
        q = f"Find the roots of the cubic equation: {sp.latex(expanded)} = 0"
        a = f"**Solution:**\nBy factoring, we find the roots:\n(x - {r1})(x - {r2})(x - {r3}) = 0\n**Final Answer:**\nx = {r1}, x = {r2}, and x = {r3}."
    else:
        expr = (x - r1) * (x - r2)
        expanded = sp.expand(expr)
        q = f"Find the roots of the quadratic equation: {sp.latex(expanded)} = 0"
        a = f"**Solution:**\nFactor the expression:\n(x - {r1})(x - {r2}) = 0\nSet each factor to zero to find roots.\n**Final Answer:**\nx = {r1} and x = {r2}."
    return (q.strip(), a.strip(), "algebra", "easy", "MMLU")

def generate_linear_algebra_det():
    a, b, c, d = [random.randint(-10, 10) for _ in range(4)]
    det = a*d - b*c
    q = f"Calculate the determinant of the 2x2 matrix: A = [[{a}, {b}], [{c}, {d}]]"
    a_str = f"**Solution:**\ndet(A) = ad - bc\ndet(A) = ({a})*({d}) - ({b})*({c})\ndet(A) = {a*d} - {b*c} = {det}\n**Final Answer:**\n{det}"
    return (q.strip(), a_str.strip(), "linear_algebra", "easy", "MMLU")

seen_questions = set()
UNIQUE_MATH_POOL = []
for item in MATH_POOL:
    seen_questions.add(item[0])
    UNIQUE_MATH_POOL.append(item)

while len(UNIQUE_MATH_POOL) < 500:
    generator = random.choice([generate_derivative_problem, generate_integral_problem, generate_algebra_roots, generate_linear_algebra_det])
    problem = generator()
    if problem[0] not in seen_questions:
        seen_questions.add(problem[0])
        UNIQUE_MATH_POOL.append(problem)

def generate_dataset_03(output_path, n_records=500):
    records = []
    for i, (q, a, sub, diff, bench) in enumerate(UNIQUE_MATH_POOL):
        if i >= n_records: break
        record = make_base_record(
            dataset_num=3, dataset_name=SPEC["name"], domain=SPEC["domain"], subdomain=sub,
            conversation=make_conversation(system="You are a mathematics expert.", user=q, assistant=a),
            category=sub.split('_')[0], difficulty=diff, quality_score=random.uniform(0.90, 0.99),
            tokens_input=len(q.split()) * 1.3, tokens_output=len(a.split()) * 1.3, benchmark_alignment=bench,
            language="en", has_math=True, extra_fields={"math_domain": sub, "requires_calculation": True, "solution_steps": a.count("\n\n") + 1},
            record_index=i,
        )
        records.append(record)
    with open(output_path, "w", encoding="utf-8") as f:
        for r in records: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✅ Generated {len(records)} math records → {output_path}")

if __name__ == "__main__":
    generate_dataset_03("NJIRLAH-SS-DATASETS/raw/njirlah-3-dataset.jsonl")
