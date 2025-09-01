#!/usr/bin/env python3
"""
Setup script pour Arkalia Quest
Force l'utilisation de pip au lieu de Poetry
"""

from setuptools import find_packages, setup

# Lire requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = [
        line.strip() for line in f if line.strip() and not line.startswith("#")
    ]

setup(
    name="arkalia-quest",
    version="3.0.0",
    description="Jeu éducatif immersif avec IA émotionnelle LUNA",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Équipe Arkalia",
    author_email="contact@arkalia-quest.com",
    url="https://github.com/arkalia-luna-system/arkalia-quest",
    packages=find_packages(include=["core*", "engines*", "utils*"]),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    entry_points={
        "console_scripts": [
            "arkalia-quest=app:main",
        ],
    },
)
