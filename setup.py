import os
import sys

from setuptools import find_packages
from setuptools import setup


VERSION = ("0.0.3")

readme = os.path.join(os.path.dirname(__file__), "README.rst")

requires = [
    "alembic",
]


setup(
    name="alem",
    version=VERSION,
    description="A revision wrapper of alembic",
    long_description=open(readme).read(),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Database :: Front-Ends",
    ],
    keywords="SQLAlchemy migrations alembic",
    author="Leon Huayra",
    author_email="hffilwlqm@gmail.com",
    url="https://github.com/Asphaltt/alem.py",
    license="MIT",
    packages=["alem"],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={"console_scripts": ["alem = alem.alem:main"]},
)
