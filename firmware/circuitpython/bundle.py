import os
import shutil
from dotenv import load_dotenv
import requests
import zipfile

load_dotenv()

# You can specify the directory for circuitpy library bundle 
# - downloaded from: https://circuitpython.org/libraries
# - this project uses the version 7.X bundle!!!
# - should point to the 'lib' directory within the library bundle
cpy_lib_root = os.getenv("CIRCUITPY_LIBRARY_BUNDLE_ROOT")

# If cpy_lib_root is NOT provided, the script will attempt to download the following archive from github
library_archive_file = "adafruit-circuitpython-bundle-7.x-mpy-20221101"
downloaded = False

def download_cpy_bundle():
    global downloaded
    if not downloaded:
        r = requests.get('https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20221101/' + library_archive_file + ".zip")
        with open("cpy_zip.zip", "wb+") as cpy_zip:
            cpy_zip.write(r.content)
            with zipfile.ZipFile(cpy_zip) as local_zip:
                local_zip.extractall()
        downloaded = True

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
        download_cpy_bundle()
        cpy_lib_root = os.path.join(library_archive_file, "lib")

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

if downloaded:
    shutil.rmtree(library_archive_file)

print("CircuitPython bundle complete.")
