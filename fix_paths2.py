# Simple one-time fix
f    = open("app.py", encoding="utf-8")
code = f.read()
f.close()

code = code.replace(
    "UPLOADS_DIR = BASE_DIR / str(UPLOADS_DIR)",
    'UPLOADS_DIR = BASE_DIR / "uploads"'
)
code = code.replace(
    "OUTPUTS_DIR = BASE_DIR / str(OUTPUTS_DIR)",
    'OUTPUTS_DIR = BASE_DIR / "outputs"'
)

open("app.py", "w", encoding="utf-8").write(code)
print("Fixed!")