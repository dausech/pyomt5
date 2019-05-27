from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
try:
    with open(path.join(here, 'readme.md'), encoding='utf-8') as f:
        long_description = f.read()
except IOError:
    long_description = 'pyOMT5 - Python Open Metatrader 5 module'

setup(
    name='pyOMT5',
    version='0.0.1',
    author='Paulo Rodrigues',
    author_email='paulorodriguesxv@gmail.com',
    license='MIT',
    description='pyOMT5 - Python Open Metatrader 5 module',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    url='https://github.com/paulorodriguesxv/pyomt5',
    install_requires=['pyzmq', 'pandas'],
    test_requires=[],
    extras_requires={
        'pandas': ['pandas'],
    },
    keywords=['stocks', 'market', 'finance', 'metatrader', 'quotes', 'shares'],
    packages=find_packages(exclude=['tutorial']),
    package_data={
        'pyomt5': [],
    })
