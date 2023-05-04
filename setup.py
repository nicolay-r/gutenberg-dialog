from setuptools import (
    setup,
    find_packages,
)


def get_requirements(filenames):
    r_total = []
    for filename in filenames:
        with open(filename) as f:
            r_local = f.read().splitlines()
            r_total.extend(r_local)
    return r_total

setup(
    name='gutenberg-dialog',
    version='0.0.1',
    description='',
    classifiers=[],
    keywords='natural language processing',
    packages=find_packages(),
    install_requires=get_requirements(['requirements.txt']),
)
