from setuptools import setup, find_packages

setup(
    name="codex_alchemy",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "codex-alchemy=main:main",
        ],
    },
)

