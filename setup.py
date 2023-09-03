from setuptools import setup, find_packages

from pybox import __version__

setup(
    name="pybox",
    version=__version__,
    description="A Python library for making common things easier and faster such as creating Chat UIs with Gradio or testing LLMs on predefined questions.",
    license="Apache License 2.0",

    url="https://github.com/beratcmn/pybox",
    author="Berat Çimen",
    author_email="beratcmn@hotmail.com",

    packages=find_packages(),

    install_requires=[
        "gradio",
        "pandas",
        "numpy",
        "matplotlib"
    ],
)
