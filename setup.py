import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="dhttpfs",
    version="0.0.0",
    install_requires=[],
    description="HTTP server that decrypts served files on the fly",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/goncalopp/dhttpfs",
    packages=setuptools.find_packages(),
    tests_require=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
