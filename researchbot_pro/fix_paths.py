"""
Professional Path Fixer for app.py
Run once → Fixes all path issues
"""

from pathlib import Path

app_path = Path("app.py")
content  = app_path.read_text(encoding="utf-8")

# ── Step 1: Fix save_report function ─────────────────
old_save = '''def save_report(content: str, prefix: str = "report") -> str:
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"outputs/{prefix}_{ts}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path'''

new_save = '''BASE_DIR    = Path(__file__).parent
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"
UPLOADS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)


def save_report(content: str, prefix: str = "report") -> str:
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = OUTPUTS_DIR / f"{prefix}_{ts}.md"
    path.write_text(content, encoding="utf-8")
    return str(path)'''

# ── Step 2: Fix uploads folder creation ──────────────
old_mkdir = '''Path("uploads").mkdir(exist_ok=True)
Path("outputs").mkdir(exist_ok=True)'''

new_mkdir = '''# Paths defined below in save_report section'''

# ── Step 3: All replacements ──────────────────────────
replacements = [
    # Fix mkdir
    (old_mkdir, new_mkdir),

    # Fix save_report
    (old_save, new_save),

    # Fix file manager paths
    (
        'reports = sorted(Path("outputs").glob("*.md"), reverse=True)',
        'reports = sorted(OUTPUTS_DIR.glob("*.md"), reverse=True)'
    ),
    (
        'reports = sorted(Path("outputs").glob("*.md"), reverse=True) if output_dir.exists() else []',
        'reports = sorted(OUTPUTS_DIR.glob("*.md"), reverse=True) if OUTPUTS_DIR.exists() else []'
    ),
    (
        'uploads = list(Path("uploads").glob("*"))',
        'uploads = list(UPLOADS_DIR.glob("*"))'
    ),
    (
        'output_dir = Path("outputs")\n    reports    = list(output_dir.glob("*.md")) if output_dir.exists() else []',
        'reports = list(OUTPUTS_DIR.glob("*.md")) if OUTPUTS_DIR.exists() else []'
    ),
    (
        'output_dir = Path(config.OUTPUT_DIR)\n        if output_dir.exists():',
        'if OUTPUTS_DIR.exists():'
    ),
    (
        'reports = list(output_dir.glob("*.md"))',
        'reports = list(OUTPUTS_DIR.glob("*.md"))'
    ),

    # Fix upload save paths
    (
        'save_path = Path("uploads") / uploaded.name',
        'save_path = UPLOADS_DIR / uploaded.name'
    ),
    (
        'save_path = Path("uploads") / image_file.name',
        'save_path = UPLOADS_DIR / image_file.name'
    ),
    (
        'save_path = Path("uploads") / doc_file.name',
        'save_path = UPLOADS_DIR / doc_file.name'
    ),

    # Fix report path display
    (
        'path = save_report(result, prefix)\n        st.success(f"',
        'saved_path = save_report(result, prefix)\n        st.success(f"'
    ),
]

# ── Apply all replacements ───────────────────────────
fixed = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✅ Fixed: {old[:50].strip()}...")
        fixed += 1
    else:
        print(f"⚠️  Not found: {old[:50].strip()}...")

# ── Step 4: Verify no broken paths remain ────────────
issues = [
    'f"outputs/',
    'f"uploads/',
    'str(OUTPUTS_DIR / f"',
    'str(UPLOADS_DIR / f"',
]

print("\n── Checking for remaining issues ──")
for issue in issues:
    count = content.count(issue)
    if count > 0:
        # Fix unclosed brackets
        content = content.replace(
            'str(OUTPUTS_DIR / f"{prefix}_{ts}.md"',
            'str(OUTPUTS_DIR / f"{prefix}_{ts}.md")'
        )
        content = content.replace(
            'str(UPLOADS_DIR / f"{',
            'str(UPLOADS_DIR / "'
        )
        print(f"⚠️  Fixed broken: {issue}")
    else:
        print(f"✅ Clean: {issue}")

# ── Step 5: Write fixed content ──────────────────────
app_path.write_text(content, encoding="utf-8")

# ── Step 6: Syntax check ─────────────────────────────
import py_compile, tempfile, shutil

tmp = Path(tempfile.mktemp(suffix=".py"))
shutil.copy(app_path, tmp)

try:
    py_compile.compile(str(tmp), doraise=True)
    print("\n✅ SYNTAX CHECK PASSED!")
except py_compile.PyCompileError as e:
    print(f"\n❌ SYNTAX ERROR: {e}")
    print("   Open app.py and check the error line")
finally:
    tmp.unlink(missing_ok=True)

print(f"\n{'='*50}")
print(f"✅ Fixed: {fixed} replacements")
print(f"💾 Saved: app.py")
print(f"{'='*50}")
print("Now run: streamlit run app.py")