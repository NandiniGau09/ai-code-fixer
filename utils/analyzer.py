import subprocess
import tempfile
import ast
import re


def run_pylint(code):

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".py",
            mode="w",
            encoding="utf-8"
        ) as f:

            f.write(code)
            temp_file = f.name

        result = subprocess.run(
            ["python", "-m", "pylint", temp_file],
            capture_output=True,
            text=True
        )

        return parse_pylint_output(
            result.stdout
        )

    except Exception as e:

        return [
            f"Analysis error: {str(e)}"
        ]


def parse_pylint_output(output):

    issues = []

    for line in output.splitlines():

        if (
            ":" in line and
            "rated" not in line.lower()
        ):

            cleaned_line = line.strip()

            if cleaned_line:

                issues.append(
                    cleaned_line
                )

    return issues[:15]


def extract_error_lines(issues):

    lines = set()

    patterns = [
        r"line\s+(\d+)",
        r":(\d+):"
    ]

    for issue in issues:

        for pattern in patterns:

            matches = re.findall(
                pattern,
                issue,
                re.IGNORECASE
            )

            for match in matches:

                try:
                    lines.add(
                        int(match)
                    )

                except ValueError:
                    pass

    return sorted(lines)


def check_code_style(code):

    issues = []

    lines = code.splitlines()

    for i, line in enumerate(
        lines,
        start=1
    ):

        if len(line) > 100:

            issues.append(
                f"Line {i}: Long line detected"
            )

        if (
            "TODO" in line or
            "FIXME" in line
        ):

            issues.append(
                f"Line {i}: TODO/FIXME found"
            )

        lower_line = line.lower()

        if (
            "password =" in lower_line or
            "api_key =" in lower_line or
            "secret =" in lower_line
        ):

            issues.append(
                f"Line {i}: Possible hardcoded secret"
            )

    return issues


def detect_duplicate_lines(code):

    issues = []

    lines = [
        line.strip()
        for line in code.splitlines()
        if line.strip()
    ]

    seen = set()

    for line in lines:

        if line in seen:

            issues.append(
                f"Duplicate code detected: {line}"
            )

        seen.add(line)

    return issues


def analyze_complexity(tree):

    complexity = 0

    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.If,
                ast.For,
                ast.While,
                ast.Try,
                ast.FunctionDef
            )
        ):

            complexity += 1

    return complexity


def calculate_quality_score(
    issues,
    complexity
):

    score = 100

    score -= len(issues) * 4
    score -= complexity * 2

    if score < 0:
        score = 0

    return score


def check_ast(tree):

    issues = []

    for node in ast.walk(tree):

        if isinstance(
            node,
            ast.Global
        ):

            issues.append(
                "Avoid using global variables"
            )

        elif isinstance(
            node,
            ast.Pass
        ):

            issues.append(
                "Avoid unnecessary pass statements"
            )

        elif isinstance(
            node,
            ast.ExceptHandler
        ):

            issues.append(
                "Empty except block detected"
            )

        elif isinstance(
            node,
            ast.FunctionDef
        ):

            if len(node.body) > 30:

                issues.append(
                    f"Function '{node.name}' is too large"
                )

        elif isinstance(
            node,
            ast.Call
        ):

            if isinstance(
                node.func,
                ast.Name
            ):

                if node.func.id in [
                    "eval",
                    "exec"
                ]:

                    issues.append(
                        f"Avoid using {node.func.id}()"
                    )

            elif isinstance(
                node.func,
                ast.Attribute
            ):

                if (
                    node.func.attr
                    == "system"
                ):

                    issues.append(
                        "Avoid using os.system()"
                    )

        elif isinstance(
            node,
            ast.For
        ):

            for child in ast.walk(node):

                if (
                    child != node and
                    isinstance(
                        child,
                        ast.For
                    )
                ):

                    issues.append(
                        "Nested loops detected"
                    )

    return issues


def analyze_code(code):

    issues = run_pylint(code)

    complexity = 0

    try:

        tree = ast.parse(code)

        issues.extend(
            check_ast(tree)
        )

        issues.extend(
            check_code_style(code)
        )

        issues.extend(
            detect_duplicate_lines(code)
        )

        complexity = analyze_complexity(
            tree
        )

        if complexity > 10:

            issues.append(
                "High code complexity detected"
            )

    except SyntaxError as e:

        issues.insert(
            0,
            f"Syntax Error: {str(e)}"
        )

    error_lines = extract_error_lines(
        issues
    )

    quality_score = calculate_quality_score(
        issues,
        complexity
    )

    quality_metrics = get_quality_metrics(
    issues,
    complexity
)

    return (
    issues,
    error_lines,
    quality_score,
    quality_metrics
)


def detect_language(code):

    if (
        "def " in code or
        "import " in code or
        "print(" in code
    ):

        return "python"

    elif (
        "public class" in code or
        "System.out.println" in code
    ):

        return "java"

    elif (
        "#include" in code or
        "cout <<" in code
    ):

        return "cpp"

    elif (
        "function " in code or
        "console.log" in code
    ):

        return "javascript"

    return "unknown"

def get_quality_metrics(
    issues,
    complexity
):

    maintainability = max(
        0,
        100 - (len(issues) * 3)
    )

    security = 100

    for issue in issues:

        lower = issue.lower()

        if (
            "eval" in lower or
            "exec" in lower or
            "os.system" in lower
        ):

            security -= 20

    readability = max(
        0,
        100 - (len(issues) * 2)
    )

    performance = max(
        0,
        100 - complexity * 4
    )

    complexity_score = max(
        0,
        100 - complexity * 5
    )

    return {

        "maintainability":
        maintainability,

        "security":
        security,

        "readability":
        readability,

        "performance":
        performance,

        "complexity":
        complexity_score
    }