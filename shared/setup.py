from setuptools import setup, find_packages

setup(
    name="shared",
    version="0.1",
    packages=find_packages(),  # Automatically find the `shared` package
    install_requires=[
        "openai",
        "google-api-core",
        "google-cloud-core",
        "google-cloud-storage"
    ],       
)
