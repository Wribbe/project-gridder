from setuptools import setup

setup(
    name="gridder",
    author="Stefan Eng",
    version="0.0.1",
    install_requires=[
        "pillow",
    ],
    entry_points = {
        "console_scripts": [
            'gridder=gridder.app:run'
        ],
    },
)
