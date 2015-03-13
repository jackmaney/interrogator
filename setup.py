import setuptools

from interrogator._version import __version__

try:
    with open("README.rst") as f:
        long_description = f.read()
except IOError:
    long_description = ""

try:
    with open("requirements.txt") as f:
        requirements = [x for x in [y.strip() for y in f.readlines()] if x]
except IOError:
    requirements = []

setuptools.setup(
    name="interrogator",
    license="MIT",
    author="Jack Maney",
    author_email="jackmaney@gmail.com",
    url="https://github.com/jackmaney/interrogator.git",
    version=__version__,
    install_requires=requirements,
    packages=setuptools.find_packages(),
    long_description=long_description,
    include_package_data=True,
    description="Populating and asking a nested series of questions populated by a YAML config file."
)
