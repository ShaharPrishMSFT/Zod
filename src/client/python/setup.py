from setuptools import setup, find_packages

setup(
    name="FormalAiSdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "litellm",
    ],
    author="FormalAI",
    description="Python SDK for FormalAI",
    python_requires=">=3.8",
)
