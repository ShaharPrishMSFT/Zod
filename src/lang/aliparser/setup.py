from setuptools import setup, find_packages

setup(
    name="aliparser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "lark>=1.1.5",
    ],
    python_requires=">=3.8",
    description="Parser for AgentLingua DSL",
    author="FormalAI",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
