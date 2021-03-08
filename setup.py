import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Tyfa',
    version='0.1',
    scripts=[],
    author="Jairo Lefebre",
    author_email="jairo.lefebre@gmail.com",
    description="Typical testor finding algorithms library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/J41R0/Tyfa",
    packages=setuptools.find_packages(),
    install_requires=[
        'bitarray >= 0.9.3'
    ],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
