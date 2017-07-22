from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tfvardoc',
    version='0.1.1',
    description='Terraform Documentation Generator/Sync',
    long_description=long_description,
    url='https://github.com/mazubieta/tf-vardoc',
    author='Manuel Zubieta',
    author_email='mazubieta@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='terraform devops documentation',
    packages=find_packages(exclude=['example', 'docs', 'test']),
    install_requires=['Parsley','Jinja2'],

    entry_points={
        'console_scripts': [
            'tfvardoc=tfvardoc:main',
        ],
    },
)
