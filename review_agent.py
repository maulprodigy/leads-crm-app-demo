import os
import sys
from pathlib import Path
import google.genai as genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not set")
    sys.exit(1)

genai.configure(api_key=api_key)

def get_changed_files():
    changed_files = []
    for file in Path(".").rglob("*.py"):
        if ".github" not in str(file) and "review_agent.py" not in str(file):
            changed_files.append(str(file))
    return changed_files[:5]

def review_code_security(files):
    findings = []
    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                code_content = f.read()

            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(
                f"Review this code for security vulnerabilities and code quality issues:\n\n{code_content[:2000]}"
            )
            findings.append(f"## {file_path}\n{response.text}")
        except Exception as e:
            findings.append(f"## {file_path}\nError reviewing file: {str(e)}")
    return findings

def main():
    files = get_changed_files()
    if not files:
        print("No Python files to review")
        return

    findings = review_code_security(files)
    with open("code_review.md", "w") as f:
        f.write("# Code Security Review\n\n")
        for finding in findings:
            f.write(finding + "\n\n")
    print("Security review complete. Results saved to code_review.md")

if __name__ == "__main__":
    main()
