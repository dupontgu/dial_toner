import os
import shutil
from dotenv import load_dotenv

load_dotenv()

# You must specify the directory for circuitpy library bundle 
# - downloaded from: https://circuitpython.org/libraries
# - this project uses the version 7.X bundle!!!
# - should point to the 'lib' directory within the library bundle
cpy_lib_root = os.getenv("CIRCUITPY_LIBRARY_BUNDLE_ROOT")

for bundle in ["basic", "ultra"]:
    path = os.path.join('bundle', bundle)
    # copy all common files to bundle output dir
    shutil.copytree("common", path, dirs_exist_ok=True)
    # copy all bundle-specific files to bundle output dir
    shutil.copytree(bundle, path, dirs_exist_ok=True)

    # create combined list of common and bundle-specific dependencies
    deps = []
    for f in [os.path.join("common", "common_dependencies.txt"), os.path.join(bundle, 'dependencies.txt')]:
        with open(f) as f_open:
            deps = deps + f_open.readlines()

    lib_path = os.path.join(path, "lib")
    os.makedirs(lib_path, exist_ok=True)

    if cpy_lib_root is None:
        with open(os.path.join(lib_path, "README.txt"), "w+") as f_open:
            f_open.write("You will need to copy the following CircuitPython libraries into this directory:\n\n")
            f_open.writelines(deps)
            f_open.write("\n\nTo download these libraries, visit: https://circuitpython.org/libraries and download the bundle for version 7.x.\n")
            f_open.write("If the library ends in '/', you should copy the entire directory.\n")
        continue

    # copy all dependencies into bundle output dir
    for dep_line in deps:
        dep = dep_line.strip()
        dep_path = os.path.join(cpy_lib_root, dep)
        if os.path.isdir(dep_path):
            shutil.copytree(dep_path, os.path.join(lib_path, dep), dirs_exist_ok=True)
        else:
            dest_path = os.path.join(lib_path, dep)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(dep_path, dest_path)

print("CircuitPython bundle complete.")
