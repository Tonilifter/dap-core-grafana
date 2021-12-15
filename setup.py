import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dap-core-scc-api",
    version="1.14.0",
    author="Repsol Data Analytics Platform",
    description="Platform SCC API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://repsol-digital-team.visualstudio.com/DAPlatform01/_git/dap-core-scc-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "werkzeug==0.16.1",
        "flask-restplus==0.13.0",
        "Flask==1.1.1"
    ]
)
