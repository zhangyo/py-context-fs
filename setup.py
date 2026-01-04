from setuptools import setup, find_packages

setup(
    name="py-context-fs",
    version="0.1.0",
    description="A Python implementation of the Agentic File System (AFS) pattern",
    author="User", 
    packages=find_packages(),
    install_requires=[
        "tiktoken>=0.3.0",
    ],
    python_requires=">=3.8",
)
