import os
import fnmatch

def find_artifacts(name, base):
    found = []
    base = os.path.expanduser(base)
    for root, dirs, files in os.walk(base):
        for f in fnmatch.filter(files, f"*{name}*"):
            found.append(os.path.join(root, f))
    return found 