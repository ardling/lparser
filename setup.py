import setuptools

name = "lparser"

setuptools.setup(
    name=name,
    description="lamblda parser",
    author="Michael Ovsiannikov",
    author_email="ardling@gmail.com",
    license="http://unlicense.org",
    keywords="asyncio moex iss",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=["aiohttp"],
)
