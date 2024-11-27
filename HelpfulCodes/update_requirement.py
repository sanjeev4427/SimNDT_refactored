import subprocess

# List of specified libraries
libraries = [
    "cffi",
    "Cython",
    "matplotlib",
    "numpy",
    "opencv-python",
    "Pillow",
    "pyopencl",
    "PyOpenGL",
    "PySide",
    "pytools",
    "scipy"
]

# Get the list of installed packages
process = subprocess.Popen(["pip", "freeze"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
installed_packages = stdout.decode().splitlines()

# Filter the installed packages to include only the specified libraries
filtered_packages = [pkg for pkg in installed_packages if any(pkg.startswith(lib) for lib in libraries)]

# Write the filtered packages to requirements.txt
with open("requirements.txt", "w") as f:
    for pkg in filtered_packages:
        f.write(pkg + "\n")

# Write all installed packages to all_requirements.txt
with open("all_requirements.txt", "w") as f:
    for pkg in installed_packages:
        f.write(pkg + "\n")

print("requirements.txt has been updated with specified libraries.")
print("all_requirements.txt has been updated with all installed libraries.")