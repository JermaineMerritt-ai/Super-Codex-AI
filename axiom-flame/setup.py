from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="axiom-flame",
    version="1.0.0",
    description="Sacred ceremonial system management for the Super-Codex-AI dominion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Super-Codex-AI",
    author_email="admin@codexdominion.app",
    url="https://github.com/JermaineMerritt-ai/Super-Codex-AI",
    packages=find_packages(),
    package_data={
        "axiom_flame": [
            "packages/**/*",
            "artifacts/**/*",
            "*.md",
            "*.yaml",
            "*.json"
        ]
    },
    include_package_data=True,
    install_requires=[
        "flask>=3.0.0",
        "jsonschema>=4.0.0",
        "requests>=2.25.0",
        "pathlib2>=2.3.0; python_version<'3.4'"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "axiom-flame=axiom_flame:main",
            "axiom=axiom_flame:main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration"
    ],
    python_requires=">=3.8",
    keywords="ceremonial system management api service monitoring",
    project_urls={
        "Bug Reports": "https://github.com/JermaineMerritt-ai/Super-Codex-AI/issues",
        "Source": "https://github.com/JermaineMerritt-ai/Super-Codex-AI",
        "Documentation": "https://github.com/JermaineMerritt-ai/Super-Codex-AI/wiki"
    }
)