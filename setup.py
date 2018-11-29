from setuptools import setup, find_packages

__version__ = "0.1.0"

requirements = []
cyphers = [
    "md5=killbrute.cyphers.all:MD5Cypher",
    "sha224=killbrute.cyphers.all:SHA224Cypher",
    "none=killbrute.cyphers.all:NoCypher",
    "zip=killbrute.cyphers.all:ZipCypher",
]

setup(
    name='killbrute',
    version=__version__,
    description="Brute forcing hacking tool",
    # long_description=open("README.rst").read(),
    license="MIT",
    author="Elran Shefer",
    author_email="elran777@gmail.com",
    # url="https://github.com/IamShobe/killbrute",
    keywords="brute forcing password cracking",
    install_requires=requirements,
    python_requires="~=2.7.0",
    entry_points={
        "console_scripts": [
            "killbrute = killbrute.cli:main"
        ],
        "killbrute.cyphers": cyphers
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={'': ['*.xls', '*.xsd', '*.json', '*.css', '*.xml', '*.rst']},
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
)