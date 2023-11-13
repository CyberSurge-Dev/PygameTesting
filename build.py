# Created By: Zachary Hoover
# Created Date: 11/7/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
A crude program to run the commands to create an executable for the project.
"""
# --------------------------------------------------------------------------------
# External impots
import os
import PyInstaller.__main__
import shutil

# Set current working directory
path = (__file__[:len(__file__.rpartition('\\')[0])])
print(f"Working Directory: {path}")

# Remove any old build directories
print("Deleting old files...")
try:
    shutil.rmtree(os.path.join(path, "dist"))
except FileNotFoundError:
    print("dist directory did not exist.")
try:
    shutil.rmtree(os.path.join(path, "build"))
except FileNotFoundError:
    print("build directory did not exist.")

# Run pyinstaller script
PyInstaller.__main__.run([
    os.path.join(path, "main.py"),
    '--noconsole'
])

# Remove build directory
try:
    shutil.rmtree(os.path.join(path, "build"))
except FileNotFoundError:
    print("build directory did not exist.")

print("copying data...")
# Copy necessary data to dist/main
shutil.copytree(os.path.join(path, "data"), os.path.join(path, "dist\\main\\data")) # data
shutil.copytree(os.path.join(path, "scripts"), os.path.join(path, "dist\\main\\scripts")) # scripts

# Run executable
os.startfile(os.path.join(path, 'dist\\main\\main.exe'))
