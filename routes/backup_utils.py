# routes/backup_utils.py

import subprocess
import datetime
import os

def backup_after_major_ritual():
    vault_dir = os.path.expanduser("~/codex_backup")
    commit_msg = f"[AutoBackup] Ritual backup {datetime.datetime.now().isoformat()}"
    try:
        subprocess.run(["git", "add", "."], cwd=vault_dir, check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=vault_dir, check=True)
        subprocess.run(["git", "push"], cwd=vault_dir, check=True)
        print(f"[SUCCESS] Backup complete: {commit_msg}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git command failed: {e}")
    except Exception as e:
        print(f"[ERROR] Backup failed: {e}")

