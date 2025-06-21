import subprocess
def share_backend():
    subprocess.call(["ngrok", "http", "8000"])
