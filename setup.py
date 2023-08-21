#!/usr/bin/env python3
from setuptools import find_packages
from setuptools import setup
from src.qa_tool import 

#Si tienes un readme
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="talkdocument",
    version="0.0.0",
    description="This project allows you to ask questions related to a document provided through the use of LLM",
    author="Damian Gil",
    author_email="damianvegasgenil@hotmail.com",
    packages=find_packages(),
    scripts=[],
    )