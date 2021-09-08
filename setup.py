import os
import subprocess

from setuptools import setup, find_packages

current_file_path = os.path.abspath(os.path.dirname(__file__))


def get_readme():
    readme_file_path = os.path.join(current_file_path, "README.md")
    with open(readme_file_path, "r", encoding="utf-8") as f:
        return f.read()


def get_version():
    version_file_path = os.path.join(current_file_path, "version.txt")
    with open(version_file_path, "r", encoding="utf-8") as f:
        version = f.read().strip()

    try:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("ascii").strip()
    except Exception:  # pylint: disable=broad-except
        sha = "Unknown"

    if os.getenv("SPACY_LANGUAGE_DETECTION_RELEASE_BUILD") != "1":
        version += ".dev1"
        if sha != "Unknown":
            version += "+" + sha[:7]
    return version


def write_version_python_file(version):
    version_python_file = os.path.join(current_file_path, "spacy_language_detection", "version.py")
    with open(version_python_file, "w", encoding="utf-8") as f:
        f.write(f"__version__ = {repr(version)}\n")


def main():
    readme = get_readme()

    version = get_version()
    print("Building version", version)
    print("Building version", version)
    write_version_python_file(version)

    packages = find_packages()
    setup(
        name="spacy-language-detection",
        version=version,
        author="David Beauchemin",
        author_email="david.beauchemin.5@ulaval.ca",
        url="https://github.com/davebulaval/spacy-language-detection",
        download_url="https://github.com/davebulaval/spacy-language-detection/archive/v" + version + ".zip",
        license="LGPLv3",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ],
        packages=packages,
        install_requires=["spacy>=3.0.0", 'langdetect==1.0.9'],
        python_requires=">=3.7",
        description="Fully customizable language detection for spaCy pipeline",
        long_description=readme,
        long_description_content_type="text/markdown"
    )


if __name__ == "__main__":
    main()
