import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="hushbugger",
    version="0.0.1",
    author="HushBugger",
    author_email="hushbugger@posteo.net",
    description="A silent alternative to debugging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HushBugger/hushbugger",
    py_modules=["hushbugger"],
    license="ISC",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: ISC License (ISCL)",
    ],
)
