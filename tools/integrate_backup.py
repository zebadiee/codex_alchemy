import os
import re

ROOT_DIR = os.path.expanduser("~/codex_alchemy")
TARGET_FILES = []

# 1. Walk codex_alchemy to find .py files in routes and CLI
for subdir, _, files in os.walk(ROOT_DIR):
    for file in files:
        if file.endswith(".py") and ("routes" in subdir or "cli" in subdir):
            TARGET_FILES.append(os.path.join(subdir, file))

# 2. Define logic to insert backup import and call
def patch_file(path):
    with open(path, "r") as f:
        lines = f.readlines()

    modified = False
    already_imported = any("backup_after_major_ritual" in line for line in lines)

    if not already_imported:
        for i, line in enumerate(lines):
            if line.startswith("from") or line.startswith("import"):
                continue
            lines.insert(i, "from routes.backup_utils import backup_after_major_ritual\n")
            modified = True
            break

    # Inject call before return statements inside def blocks
    new_lines = []
    inside_func = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("def ") or stripped.startswith("async def "):
            inside_func = True

        if inside_func and stripped.startswith("return") and "backup_after_major_ritual()" not in new_lines[-1]:
            indent = re.match(r"\s*", line).group()
            new_lines.append(f"{indent}backup_after_major_ritual()\n")
            modified = True

        new_lines.append(line)

    if modified:
        backup_path = path + ".bak"
        os.rename(path, backup_path)
        with open(path, "w") as f:
            f.writelines(new_lines)
        print(f"✅ Patched: {path} (backup saved as .bak)")
    else:
        print(f"⚠️ Skipped (already patched or no changes): {path}")

# 3. Execute
for target in TARGET_FILES:
    patch_file(target)

