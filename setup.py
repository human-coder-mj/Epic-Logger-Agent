#!/usr/bin/env python3
"""
Setup script for Epic Changelog Agent
"""
from setuptools import setup, find_packages

# Read the README file for long description
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Epic Logger Agent - Transform boring changelogs into epic narratives!"

# Read requirements
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return [
            "python-dotenv>=1.0.0",
            "google-auth>=2.40.3",
            "google-genai>=1.31.0",
            "python-dotenv>=1.0.0", 
            "click>=8.0.0",
            "colorama>=0.4.0",
            "requests>=2.31.0"
        ]

setup(
    name="epic-logger-agent",
    version="1.0.0",
    author="humancodermj",
    description="Transform boring software changelogs into epic theatrical narratives",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/human-coder-mj/Epic-Logger-Agent.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "epiclog=app.main:main",
            "changelog=app.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
