'''
Created on Jun. 6, 2019

@author: KJNETHER
'''
import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()
    
with open('requirements.txt') as f:
    requires =f.read().splitlines()


setuptools.setup(
    name="ckanext-bcdc-apitests",
    version="0.0.1",
    author="Kevin Netherton",
    author_email="kevin.netherton@gov.bc.ca",
    description="API testing for BC Data Catalog",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bcgov/bcdc-test",
    packages=setuptools.find_packages(),
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    install_requires=requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Testing",
        "Operating System :: OS Independent",
    ],
)