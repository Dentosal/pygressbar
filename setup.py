from setuptools import setup

setup(
    name="pygressbar",
    version="0.1.0",
    author="Hannes Karppila",
    license="MIT",
    url="https://github.com/Dentosal/pygressbar",
    packages=["pygressbar"],
    package_data={"": ["LICENSE"]},
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Terminals",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ]
)
