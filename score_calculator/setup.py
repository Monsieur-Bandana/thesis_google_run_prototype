from setuptools import setup, find_packages

setup(
    name="score_calculator",
    version="0.1",
    author="Nicolas W",
    packages=find_packages(),
    install_requires=[
        "openai",
        "google-api-core",
        "google-cloud-core",
        "google-cloud-storage",
    ],       
)
