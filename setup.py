from setuptools import setup, find_packages

setup(
    name="mutils",
    version="1.0.0",
    packages=find_packages(),
    author="Fitzgera1d",
    description="Personal Utility Set",
    url="https://github.com/Fitzgera1d/mutils",
    install_requires=open("requirements.txt").read().splitlines(),
)