from setuptools import setup, find_packages


setup(
    description="Message Queue Tools for flask project",
    author="Linewalks",
    author_email="jindex2411@linewalks.com",
    url="https://github.com/linewalks/dasima",
    license="Linewalks",
    python_requires=">=3.6",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "Flask",
        "kombu"
    ],
    setup_requires=["pytest-runner"],
    test_suite="tests",
    tests_require=["pytest"],
    packages=find_packages(exclude=["tests*"])
)
