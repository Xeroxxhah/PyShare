from setuptools import setup, find_packages
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.4.1'
DESCRIPTION = 'A python utility to share data on local network'
LONG_DESCRIPTION = 'A python utility to share data on local network'

# Setting up
setup(
    name="PyShare",
    version=VERSION,
    author="Xeroxxhah (Muhammad Nauman Azeem)",
    author_email="xeroxxhah@pm.me",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['tqdm', 'plyer'],
    keywords=['python', 'python3', 'FileSharing', 'PyShare'],
    classifiers=[
        "Development Status :: Running",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
    ],
    entry_points="""
    [console_scripts]
    pyshare=PyShare.PyShare:main
    """,
)