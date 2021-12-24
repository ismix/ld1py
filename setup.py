import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ld1py',
    version='0.0.4',
    author='LD1 Labs',
    author_email='info@ld1labs.com',
    description='Common python utilities for LD1 Labs projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ismix/ld1py',
    project_urls={
        "Bug Tracker": "https://github.com/ismix/ld1py/issues"
    },
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['requests'],
)
