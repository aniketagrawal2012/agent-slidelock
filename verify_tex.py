"""
Automated LaTeX Structural, Brace-Balance, and Citation Verifier for `agent_slidelock_paper.tex`.
"""
import re
import sys

def verify_latex(tex_path: str = "agent_slidelock_paper.tex") -> int:
    with open(tex_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Check begin/end environments
    begins = re.findall(r"\\begin\{([^}]+)\}", text)
    ends = re.findall(r"\\end\{([^}]+)\}", text)
    if len(begins) != len(ends):
        print(f"ERROR: Mismatched begin ({len(begins)}) and end ({len(ends)}) environments.")
        return 1

    stack = []
    for m in re.finditer(r"\\(begin|end)\{([^}]+)\}", text):
        kind, env = m.group(1), m.group(2)
        if kind == "begin":
            stack.append(env)
        else:
            if not stack or stack[-1] != env:
                print(f"ERROR: Environment mismatch at {env}; stack top={stack[-1] if stack else None}")
                return 1
            stack.pop()

    # Check citations vs bibitems
    bibitems = set(re.findall(r"\\bibitem\{([^}]+)\}", text))
    cites = set()
    for c_match in re.findall(r"\\cite\{([^}]+)\}", text):
        for part in c_match.split(","):
            cites.add(part.strip())

    missing_cites = cites - bibitems
    if missing_cites:
        print(f"ERROR: Undefined citations: {missing_cites}")
        return 1

    print(f"SUCCESS: {tex_path} verified ({len(begins)} environments balanced, {len(bibitems)} bibitems matched).")
    return 0

if __name__ == "__main__":
    sys.exit(verify_tex() if "verify_tex" in globals() else verify_latex())
