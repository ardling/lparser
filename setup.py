import setuptools

name = "lparser"

setuptools.setup(
    name=name,
    description="lamblda parser",
    author="Michael Ovsiannikov",
    author_email="ardling@gmail.com",
    license="GPLv3",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[
        'parsec'
    ],
    extras_require={
        'testing': [
            'pytest>=5.0.0',
            'pytest-coverage'
        ]
    }
)
