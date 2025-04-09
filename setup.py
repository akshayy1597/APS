"""
from setuptools import find_packages,setup  #find_packages is used to find all the packages in the directory
from typing import List 

REQUIREMENT_FILE_NAME="requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements()->List[str]:  
    
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
    
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list


setup(
    name="sensor",
    version="0.0.2",
    author="Akshay",
    author_email="akshayykatageri@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements(), 
)
"""



from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    with open('requirements.txt') as f:
        requirements = f.readlines()
        requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("-e")]
    return requirements

setup(
    name="sensor",
    version="0.0.1",
    author="Akshayy",
    packages=find_packages(),
    install_requires=get_requirements()
)
