from setuptools import setup, find_packages

from pybox import __version__

setup(
    name="pybox",
    version=__version__,

    url="https://github.com/beratcmn/pybox",
    author="Berat Çimen",
    author_email="beratcmn@hotmail.com",

    packages=find_packages(),

    install_requires=[
        "gradio",
    ],
)
