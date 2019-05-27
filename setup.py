import sys
import os
from setuptools import setup, find_packages
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open('README.md', 'r', 'utf-8') as f:
        readme = f.read()
except IOError:
    readme = 'pyOMT5 - Python Open Metatrader 5 module'

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

setup(
    name='pyOMT5',
    version='0.0.23',
    author='Paulo Rodrigues',
    author_email='paulorodriguesxv@gmail.com',
    license='MIT',
    description='pyOMT5 - Python Open Metatrader 5 module',
    long_description='pyOMT5 - Python Open Metatrader 5 module',
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    url='https://github.com/paulorodriguesxv/pyomt5',
    install_requires=['pyzmq', 'pandas'],
    tests_require=[],
    extras_require={
        'pandas': ['pandas'],
    },
    keywords=['stocks', 'market', 'finance', 'metatrader', 'quotes', 'shares'],
    packages=find_packages(exclude=['tutorial']),
    package_data={
        'pyomt5': [],
    })
