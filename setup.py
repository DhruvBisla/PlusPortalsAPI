from setuptools import setup, find_packages
import re
import os

def get_version(package):
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)

def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()

setup(
    name="plusportals",
    version=get_version("plusportals"),
    url="https://github.com/DhruvBisla/PlusPortalsAPI",
    license="MIT",
    author="Dhruv Bisla",
    author_email="bisladhruv@gmail.com",
    description="A reverse engineered API PlusPortals",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['api', 'reverse-engineered', 'plusportals', 'plusportalsapi'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    requires = ['requests','lxml'],
    install_requires=['requests','lxml'],
    zip_safe=False,
)
