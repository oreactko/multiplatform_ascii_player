import os
import py_compile
def get_py_files(root="."):
    py_files = []
    root = os.path.abspath(root)

    for dirpath, dirnames, filenames in os.walk(root):
        # bỏ qua .venv
        dirnames[:] = [d for d in dirnames if d != ".venv"]

        for f in filenames:
            if f.endswith(".py"):
                full_path = os.path.join(dirpath, f)
                rel_path = os.path.relpath(full_path, root)
                py_files.append(rel_path)

    return py_files


files = get_py_files()
for f in files:
    py_compile.compile(f,doraise=True)